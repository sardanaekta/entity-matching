import sys
import json
from itertools import groupby
import operator
import pprint
import random
import re
from py_stringmatching import simfunctions,tokenizers

#if(len(sys.argv) != 4):
#   print >> sys.stderr, 'Usage: python cs784stage2.py elec_brand_dic.txt _dev_set.tsv _test_set.tsv'

VALIDATION_RUN = False
VALIDATION_SIZE = 60 #Max 230
ALLOW_PARTIAL = True
IS_DEBUG = False

def DEBUG(debug):
    if IS_DEBUG:
        print debug

#http://stackoverflow.com/a/3313605/1492106
def sublistExists(list1, list2):
    return ''.join(map(str, list1)) in ''.join(map(str, list2))

brands = dict()

with open('elec_brand_dic.txt') as f:
    for line in f:
        line = unicode(line, errors='ignore') #For character which are not utf-8
        data = line.strip().split('\t') #.lower()
        brand = data[0]
        brands.update({data[0]:(brands.get(data[0], 0) + int(data[1]))})
    f.close()

global _dev_set
global _test_set

_dev_set = []
_test_set = []

with open('_dev_set.tsv') as f:
    lines = f.readlines()
    if VALIDATION_RUN:
        if(VALIDATION_SIZE < len(lines)):
            random.shuffle(lines)
        for line in lines[0:VALIDATION_SIZE]:
            data = line.strip().split('\t') #.lower()
            _test_set.append(data)
        lines = lines[VALIDATION_SIZE:]
    f.close()
    for line in lines:
        line = unicode(line, errors='ignore') #For character which are not utf-8
        data = line.strip().split('\t') #.lower()
        _dev_set.append(data)
        for d in data[2:]:
            brands.update({d:(brands.get(d, 0) + 1)})

if not VALIDATION_RUN:
    with open('_test_set.tsv') as f:
        lines = f.readlines()
        f.close()
        for line in lines:
            line = unicode(line, errors='ignore') #For character which are not utf-8
            data = line.strip().split('\t') #.lower()
            _test_set.append(data)

#brands_list = sorted(brands.items(), key=operator.itemgetter(1), reverse=True)
brands_list = sorted(brands.items(), key=lambda x: len(x[0]))

symbol_re = re.compile('[^\\w]+', re.IGNORECASE)
brands_re = []

for brand, count in brands_list:
    brands_re.append(re.compile('\\b' + symbol_re.sub('[^\\w]{0,3}', brand) + '\\b', re.IGNORECASE))

#Heuristics
preposition_re = re.compile('\\bfor|with\\b', re.IGNORECASE)
limitIndex = 50
refurbished_re = re.compile('^Off\s*Lease\s*REFURBISHED\s*', re.IGNORECASE)
CaSe_re = re.compile('^[A-Z]+[a-z]+-?[A-Z]+\\w+\\b')
CASE_re = re.compile('^[A-Z]{5,}\\b') #CAPS, but not A, AN, THE, etc.

brandNames = []
key = 'Brand'
with open ('set_X.txt','r') as f:
    for line in f:
        line = unicode(line, errors='ignore')  # For character which are not utf-8
        data = line.strip().split('?')

        pairId = data[0]
        prod1_id = data[1]
        if (data[2]):
            prod1_json = json.loads(data[2])
        else:
            prod1_json = dict()
        prod2_id = data[3]
        if (data[4]):
            prod2_json = json.loads(data[4])
        else:
            prod2_json = dict()
        label = data[5]

        if (key not in prod1_json.keys() or (not prod1_json['Brand'][0])):
            prod1Brand = None
        else:
            prod1Brand = prod1_json['Brand'][0]
        if (key not in prod2_json.keys() or (not prod2_json['Brand'][0])):
            prod2Brand = None
        else:
            prod2Brand = prod2_json['Brand'][0]
        brandNames.append((prod1Brand, prod2Brand))
    f.close()
#print brandNames[3][1]
#pp = pprint.PrettyPrinter(indent=4)
#sample = random.sample(products, 350)
#print '\n\n\n'
#for s in sample:
   # print s, '\t', products[s]
brandList = []
for item in brandNames:
    #if len(item) is 2:
    #   item.append('')
    try:
        matched1 = CaSe_re.search(item[0]).group(0)
    except:
        matched1 = None
    for idx, brand in enumerate(brands_re):
        if(item[0] == None):
            match = None
        else:
            match = brand.search(item[0])
        if match is not None:
            if matched1 == None:
                matched1 = match.group(0)
            else:
                matchIndex = refurbished_re.sub('', item[0]).index(match.group(0))
                matchedIndex = refurbished_re.sub('', item[0]).index(matched1)
                if matchIndex <= matchedIndex:
                    matched1 = match.group(0)
    if matched1 is None:
        try:
            matched1 = CASE_re.search(item[0]).group(0)
        except:
            matched1 = ' '
    brandList.append([matched1])
#print brandList[0:4]
i = 0
for item in brandNames:
    # if len(item) is 2:
    #   item.append('')
    try:
        matched2 = CaSe_re.search(item[1]).group(0)
    except:
        matched2 = None
    for idx, brand in enumerate(brands_re):
        if (item[1] == None):
            match = None
        else:
            match = brand.search(item[1])
        if match is not None:
            if matched2 == None:
                matched2 = match.group(0)
            else:
                matchIndex = refurbished_re.sub('', item[1]).index(match.group(0))
                matchedIndex = refurbished_re.sub('', item[1]).index(matched2)
                if matchIndex <= matchedIndex:
                    matched2 = match.group(0)
    if matched2 is None:
        try:
            matched2 = CASE_re.search(item[0]).group(0)
        except:
            matched2 = ' '
    brandList[i].append(matched2)
    i = i+1

monge_elkan_measure = []
for pair in brandList:
    measure = simfunctions.monge_elkan(tokenizers.whitespace(pair[0]), tokenizers.whitespace(pair[1]))
    monge_elkan_measure.append(measure)
print monge_elkan_measure