import sys
import random

if len(sys.argv) != 2:
    print >> sys.stderr, 'Usage: python _sample_X_Y.py <input>'
    exit()

products = dict()
with open(sys.argv[1]) as f:
    products = f.readlines()

random.shuffle(products)

f = open('set_X.txt', 'w')
for p in products[0:10000]:
    f.write(p)
f.close()

f = open('set_Y.txt', 'w')
for p in products[10000:20000]:
    f.write(p)
f.close()
