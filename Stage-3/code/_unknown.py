import sys

with open(sys.argv[1], 'r') as fr:
	fw = open('unknown_' + sys.argv[1], 'w')
	for line in fr:
		fw.write(line.rsplit('?', 1)[0] + '\n')
	fw.close()
	fr.close()
