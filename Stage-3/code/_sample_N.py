import sys
import random

if len(sys.argv) != 3:
    print >> sys.stderr, 'Usage: python _sample_N.py <input> <count>'
    exit()

products = dict()
with open(sys.argv[1]) as f:
    products = f.readlines()

products = random.sample(products, int(sys.argv[2]))

f = open(sys.argv[2] + sys.argv[1], 'w')
for p in products:
    f.write(p)
f.close()
