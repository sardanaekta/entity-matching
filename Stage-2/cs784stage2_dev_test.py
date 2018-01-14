import sys
import random

if(len(sys.argv) != 2):
    print >> sys.stderr, 'Usage: python cs784stage2_dev_test.py sample_350.tsv'

products = dict()
with open(sys.argv[1]) as f:
    next(f) #Skip header
    for line in f:
        data = line.strip().split('\t',3)
        products.update({data[1]:data[3]})
    f.close()

J = random.sample(products, 120)
I = list(set(products) - set(J))

f = open('_dev_set.tsv', 'w')
for p in I:
    f.write(p + '\t' + products[p] + '\n')
f.close()

f = open('_test_set.tsv', 'w')
for p in J:
    f.write(p + '\t' + products[p] + '\n')
f.close()