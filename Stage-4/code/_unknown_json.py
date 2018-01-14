import sys

with open(sys.argv[1], 'r') as fr:
	for line in fr:
		print line.strip().rsplit('?', 1)[0]
	fr.close()
