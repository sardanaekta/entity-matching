import sys
import json
from itertools import groupby
import operator
import pprint
import random

if(len(sys.argv) != 2):
    print >> sys.stderr, 'Usage: python cs784stage2.py <input.txt>'

products = dict()
#linenum = 0
with open(sys.argv[1]) as f:
    for line in f:
        #linenum = linenum + 1
        #print linenum
        line = unicode(line, errors='ignore') #For character which are not utf-8
        data = line.strip().split('?')

        pairId = data[0]
        prod1_id = data[1]
        if(data[2]):
            prod1_json = json.loads(data[2])
        else:
            prod1_json = dict()
        prod2_id = data[3]
        if(data[4]):
            prod2_json = json.loads(data[4])
        else:
            prod2_json = dict()
        label = data[5]

        if(prod1_id not in products.keys()):
            products.update({prod1_id:prod1_json})
        if(prod2_id not in products.keys()):
            products.update({prod2_id:prod2_json})
    f.close()

#pp = pprint.PrettyPrinter(indent=4)

sample = random.sample(products, 350)
#print '\n\n\n'
for s in sample:
    print s, '\t', products[s]