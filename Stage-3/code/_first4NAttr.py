import sys

N = int(sys.argv[2])

with open(sys.argv[1]) as fr:
  for line in fr:
    data = line.strip().split()
    print ' '.join(data[0:4*N] + [data[-1]])

