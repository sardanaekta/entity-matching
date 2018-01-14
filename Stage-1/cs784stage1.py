import sys
import json
from itertools import groupby
import operator
import pprint

if(len(sys.argv) != 2):
    print >> sys.stderr, 'Usage: python cs784stage1.py <input.txt>'

products = dict()
attributes = []
linenum = 0
with open(sys.argv[1]) as f:
    for line in f:
        linenum = linenum + 1
        line = unicode(line.lower(), errors='ignore') #For character which are not utf-8
        data = line.strip().split('?')

        pairId = data[0]
        prod1_id = data[1]
        prod1_json = json.loads(data[2])
        prod2_id = data[3]
        prod2_json = json.loads(data[4])
        label = data[5]

        if(prod1_id not in products.keys()):
            attributes = attributes + prod1_json.keys()
            products.update({prod1_id:prod1_json})
        if(prod2_id not in products.keys()):
            attributes = attributes + prod2_json.keys()
            products.update({prod2_id:prod2_json})
    f.close()

pp = pprint.PrettyPrinter(indent=4)

print 'Total number of (unique) products:', len(products)

attributes.sort()
attributeFreq = dict()
for key, group in groupby(attributes):
    attributeFreq.update({key:len(list(group))})
sortedAttributeFreq = sorted(attributeFreq.items(), key=operator.itemgetter(1), reverse=True)

print 'Total number of (unique) attributes:', len(attributeFreq.keys())
print 'List of all attributes (<attribute>, <count>):'
pp.pprint(sorted(attributeFreq.items(), key=operator.itemgetter(1), reverse=True))
print 'Top 10 attributes (<attribute>, <count>):'
pp.pprint(sortedAttributeFreq[0:10])

topTenAttribute = set([t[0] for t in sortedAttributeFreq[0:10]])

missing = []
attributeVals = dict()
for product in products:
    missing = missing + list(topTenAttribute - set(products[product].keys()))
    for a in topTenAttribute:
        if(a in products[product].keys()):
            if(a not in attributeVals.keys()):
                attributeVals.update({a:[]})
            attributeVals[a] = attributeVals[a] + products[product][a]

print 'Top 10 attributeValsCount (<attribute>, <unique_val_count>):'
attributeValsCount = sorted([(a, len(set(attributeVals[a]))) for a in attributeVals], key=operator.itemgetter(1), reverse=True)
pp.pprint(attributeValsCount)

print 'Top 10 attributeType (<attribute>, <type>):'
attributeType = []
for a in attributeValsCount:
    if len(set(attributeVals[a[0]])) < (attributeFreq[a[0]]/4):
        attributeType.append((a[0], 'categorical'))
    else:
        attributeType.append((a[0], 'textual'))
pp.pprint(attributeType)

missing.sort()
missingFreq = dict()
for key, group in groupby(missing):
    missingFreq.update({key:len(list(group))})
topMissingFreq = sorted(missingFreq.items(), key=operator.itemgetter(1), reverse=True)
topMissingPerc = [(t[0], (100*float(t[1])/len(products))) for t in topMissingFreq]

print 'Missing values (<attribute>, <percentage>):'
pp.pprint(topMissingPerc)

#'''
#Write all top 10 attribute values to files.
for a in attributeVals:
    fw = open('./results/attributes/' + a.replace(':', '') + '.txt', 'w+')
    for i in attributeVals[a]:
        fw.write(i.encode('utf-8') + '\n')
    fw.close()
#'''

#'''
for a, t in attributeType:
    l = attributeVals[a]
    if t is 'textual':
        l = [len(i) for i in l]
    l = dict((i, l.count(i)) for i in l)
    if t is 'textual':
        l = sorted(l.items(), key=operator.itemgetter(0))
    else:
        l = sorted(l.items(), key=operator.itemgetter(1))
    attributeVals.update({a:l})

#Write the histogram data to files.
for a, t in attributeType:
    fw = open('./results/attributes/histograms/' + a.replace(':', '') + '.txt', 'w+')
    for i, c in attributeVals[a]:
        if t is 'textual':
            fw.write(str(i) + '\t' + str(c) + '\n')
        else:
            fw.write(i.encode('utf-8') + '\t' + str(c) + '\n')
    fw.close()
#'''
