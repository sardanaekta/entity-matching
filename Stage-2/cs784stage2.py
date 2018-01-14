import sys
import json
from itertools import groupby
import operator
import pprint
import random
import re

if(len(sys.argv) != 4):
	print >> sys.stderr, 'Usage: python cs784stage2.py elec_brand_dic.txt _dev_set.tsv _test_set.tsv'

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

with open(sys.argv[1]) as f:
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

with open(sys.argv[2]) as f:
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
	with open(sys.argv[3]) as f:
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

TP = 0
FP = 0
TN = 0
FN = 0

for item in _test_set:
	if len(item) is 2:
		item.append('')
	try:
		matched = CaSe_re.search(item[1]).group(0)
	except:
		matched = None
	for idx, brand in enumerate(brands_re):
		match = brand.search(item[1])
		if match is not None:
			if matched == None:
				matched = match.group(0)
			else:
				matchIndex = refurbished_re.sub('', item[1]).index(match.group(0))
				matchedIndex = refurbished_re.sub('', item[1]).index(matched)
				if matchIndex <= matchedIndex:
					matched = match.group(0)
	if matched is None:
		try:
			matched = CASE_re.search(item[1]).group(0)
		except:
			matched = None
	if matched is not None:
		flag = False
		if matched.lower() == item[2].lower():
			flag = True #Exact match with brand options
		else:
			if ALLOW_PARTIAL:
				if sublistExists(symbol_re.split(matched.lower()), [x.lower() for x in symbol_re.split(item[2])]):
					flag = True #Partial brand. E.g.: StarTech for Startech.com, Lenovo for Lenovo ThinkPad
		matchedIndex = item[1].index(matched)
		if matchedIndex > limitIndex:
			#Do not check beyond limit
			matched = None
			flag = False
		prepositionMatch = preposition_re.search(item[1])
		if prepositionMatch is not None:
			prepositionIndex = item[1].index(prepositionMatch.group(0))
			if prepositionIndex < matchedIndex:
				#print '>>>>>>>', prepositionMatch.group(0), matchedIndex, prepositionIndex
				matched = None
				flag = False #Compatibility. E.g.: 6ft A to Mini-B 8pin USB Cable w/ ferrites for Pentax Panasonic Nikon Digital Camera

	if matched is not None:
		if flag == True:
			DEBUG('\n>>' + item[1] + '\n>>' + item[2] + '\n>>' + matched + '\n++')
			TP = TP + 1
		else:
			try:
			    label = item[2]
			except IndexError:
			    label = ''
			DEBUG('\n>>' + item[1] + '\n>>' + label + '\n>>' + matched + '\n-+')
			FP = FP + 1
	else:
		if not item[2]:
			DEBUG('\n>>' + item[1] + '\n>>\n>>\n+-')
			TN = TN + 1
		else:
			DEBUG('\n>>' + item[1] + '\n>>' + item[2] + '\n>>\n--')
			FN = FN + 1

Pre = (100.0 * TP)/(TP + FP)
Rec = (100.0 * TP)/(TP + FN)

print '\nTP\tFP\tTN\tFN'
print str(TP) + '\t' + str(FP) + '\t' + str(TN) + '\t' + str(FN)
print 'Pre:\t' + str(Pre)
print 'Rec:\t' + str(Rec)
