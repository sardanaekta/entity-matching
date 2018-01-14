import sys
import json
import time
from urllib2 import urlopen

URL_HEAD = 'http://www.yoopsie.com/query.php?query='
URL_TAIL = '&referer=%2Fquery.php'
LEFT = '"upc">'
RIGHT = '<'

global products, pairs, pair_ids, labels
products = dict()
pairs = list()
pair_ids = list()
labels = list()
with open(sys.argv[-1], 'r') as fr:
	for line in fr:
		line = unicode(line, errors='ignore') #For character which are not utf-8
		data = line.strip().split('?')

		pairId = data[0]
		prod1_id = data[1]
		if (data[2]):
			prod1_json = json.loads(data[2])
		else:
			prod1_json = dict()
		prod2_id = data[3]
		if (data[4]):
			prod2_json = json.loads(data[4])
		else:
			prod2_json = dict()
		label = data[5]

		products.update({prod1_id:prod1_json})
		products.update({prod2_id:prod2_json})
		pairs.append((prod1_id, prod2_id))
		pair_ids.append(pairId)
		labels.append(label)
	fr.close()

def PN2UPC(product):
	PN = product['Product Name'][0].strip()
	URL = URL_HEAD + '+'.join(PN.split()) + URL_TAIL
	wget = urlopen(URL).read()
	try:
		UPC = int(wget[(wget.index(LEFT) + len(LEFT)):wget.find(RIGHT, wget.index(LEFT))].strip())
		UPC = str(UPC)
	except:
		UPC = 'NA'
	return UPC

for idx, pair in enumerate(pairs):
	print pair_ids[idx], PN2UPC(products[pair[0]]), PN2UPC(products[pair[1]]), labels[idx]
	time.sleep(0.5)
