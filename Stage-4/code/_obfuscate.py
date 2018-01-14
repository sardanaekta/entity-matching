import sys

with open(sys.argv[1], 'r') as fr:
	i = 1
	for line in fr:
		data = line.strip().split('?')
		data[0] = str(i)
		data[1] = str(i)
		data[3] = str(i)
		print '?'.join(data)
		i = i + 1
	fr.close()
