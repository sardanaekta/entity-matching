import os
import sys
import re
import json
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from py_stringmatching import simfunctions, tokenizers

#Global flag variables
IS_VALIDATION = True
POS_THRESH = 0.55
MIN_KEY_LEN = 5
PARTIAL_KEY = False

if IS_VALIDATION:
	if len(sys.argv) != 3:
		print 'Invalid number of arguments.'
		print 'Usage: python ' + sys.argv[0] + ' <train_file> <json_train_file>'
		exit()
else:
	if len(sys.argv) != 4:
		print 'Invalid number of arguments.'
		print 'Usage: python ' + sys.argv[0] + ' <train_file> <test_file> <json_test_file>'
		exit()

with open(sys.argv[1], 'r') as f:
	length = len(f.readline().strip().split(' '))

#Output filename
filename = sys.argv[0][:sys.argv[0].rfind('.')].replace('_', '') + '_' + sys.argv[1][:sys.argv[1].rfind('.')]
for i in range(2, len(sys.argv)):
	filename = filename + '_' + sys.argv[i]
filename = filename + '.txt'

if IS_VALIDATION:
	#Read
	_data = np.genfromtxt(sys.argv[1], dtype=float, delimiter=' ', skip_header=1, usecols=range(1, length))
	#Seperate features from labels
	X_data = _data[:, range(0, _data.shape[1]-1)]
	y_data = _data[:, _data.shape[1]-1]

	#Set random_state for testing
	X_train, X_test, y_train, y_test, i_train, i_test = train_test_split(X_data, y_data, range(0, len(y_data)), test_size=0.20, random_state=42)
else:
	#Read
	_data = np.genfromtxt(sys.argv[1], dtype=float, delimiter=' ', skip_header=1, usecols=range(1, length))
	#Seperate features from labels
	X_train = _data[:, range(0, _data.shape[1]-1)]
	y_train = _data[:, _data.shape[1]-1]
	i_train = range(0, len(y_train))

	#Read
	X_test = np.genfromtxt(sys.argv[2], dtype=float, delimiter=' ', skip_header=1, usecols=range(1, length-1))
	i_test = range(0, X_test.shape[0])
#ENDIF

classifier = LogisticRegression(C=1e5)

classifier.fit(X_train, y_train)

old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
results = classifier.predict(X_test) #May produce junk output
results_proba = classifier.predict_proba(X_test) #May produce junk output
sys.stdout.close()
sys.stdout = old_stdout

for idx in range(0, len(results)):
	if results_proba[idx][1] < POS_THRESH:
		results[idx] = 0

global products, pairs, pair_ids, actual
products = dict()
pairs = list()
pair_ids = list()
actual = dict()
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
		actual.update({pairId:label})
	fr.close()

symbol_re = re.compile('[^A-Z\d\s]+', re.IGNORECASE)
nonNum_re = re.compile('\D+', re.IGNORECASE)
withoutNum_re = re.compile('\b\D+\b', re.IGNORECASE)
nonWord_re = re.compile('\W+', re.IGNORECASE)
html_re = re.compile('((<[^<]*?>)|(&nbsp))+', re.IGNORECASE)

labels = dict()
labels.update({1:'MATCH'})
labels.update({0:'MISMATCH'})

def setMatchNumKeyField(pair, fields):
	data1 = nonNum_re.sub(' ', str(products[pair[1]])).strip().split()
	if data1:
		for d1 in data1:
			if len(d1) >= MIN_KEY_LEN:
				if PARTIAL_KEY:
					data2 = tokenizers.qgram(d1, MIN_KEY_LEN)
				else:
					data2 = tokenizers.qgram(d1, len(d1))
				for d2 in data2:
					for field in fields:
						try:
							if (d2 in products[pair[0]][field][0]):
								return 1
						except:
							continue
	return 0

def MatchMPN2PN(pair, probab):
	if 'Manufacturer Part Number' in products[pair[0]]:
		MPN = symbol_re.sub('', products[pair[0]]['Manufacturer Part Number'][0])
		PN = products[pair[1]]['Product Name'][0].strip().split()
		for pn in PN:
			if ((MPN in pn) or (pn in MPN)) and (simfunctions.levenshtein(MPN, pn) <= 1):
				#print '>', '-'.join(pair), actual['-'.join(pair)], probab
				return 1
	if 'Manufacturer Part Number' in products[pair[1]]:
		MPN = symbol_re.sub('', products[pair[1]]['Manufacturer Part Number'][0])
		PN = products[pair[0]]['Product Name'][0].strip().split()
		for pn in PN:
			if ((MPN in pn) or (pn in MPN)) and (simfunctions.levenshtein(MPN, pn) <= 1):
				#print '>', '-'.join(pair), actual['-'.join(pair)], probab
				return 1
	return 0

def NewRefurbished(pair, probab):
	if 'refurbished' not in products[pair[0]]['Product Name'][0].lower():
		if 'refurbished' in products[pair[1]]['Product Name'][0].lower():
			#print '<', '-'.join(pair), actual['-'.join(pair)], probab
			return 0
	if 'refurbished' not in products[pair[1]]['Product Name'][0].lower():
		if 'refurbished' in products[pair[0]]['Product Name'][0].lower():
			#print '<', '-'.join(pair), actual['-'.join(pair)], probab
			return 0
	return 1

def matchWord(pair, field):
	if field in products[pair[0]] and field in products[pair[1]]:
		if nonWord_re.sub('', products[pair[0]][field][0]) == nonWord_re.sub('', products[pair[1]][field][0]):
			return True
		return False
	return True

def lessAttributes(pair):
	if (len(products[pair[1]]) < len(products[pair[0]])) and (len(products[pair[1]]) <= 5):
		set1 = set()
		set2 = set()
		for f in products[pair[1]]:
			list1 = symbol_re.sub(' ', html_re.sub(' ', products[pair[0]][f][0])).strip().split()
			list2 = symbol_re.sub(' ', html_re.sub(' ', products[pair[1]][f][0])).strip().split()
			if list1 and list2:
				set1.update(list1)
				set2.update(list2)
		sim_score = simfunctions.overlap_coefficient(set1, set2)
		if sim_score == 1:
			return 1
	return 0

f = open('predict1_' + sys.argv[-2], 'w')
for idx, i in enumerate(i_test):
	f.write(pair_ids[i] + ', ' + labels[results[idx]] + '\n')
f.close()

f = open('predict2_' + sys.argv[-2], 'w')
for idx, i in enumerate(i_test):
	if results[idx] == 0:
		results[idx] = setMatchNumKeyField(pairs[i], ['GTIN', 'UPC'])
	if results[idx] == 0:
		results[idx] = setMatchNumKeyField(pairs[i][::-1], ['GTIN', 'UPC'])
	if results[idx] == 0 and results_proba[idx][1] >= 0.2:
		results[idx] = MatchMPN2PN(pairs[i], results_proba[idx])
	if results[idx] == 1 and results_proba[idx][0] >= 0.2:
		results[idx] = NewRefurbished(pairs[i], results_proba[idx])
	if results[idx] == 0 and results_proba[idx][1] >= 0.45:
		if matchWord(pairs[i], 'Product Long Description'):
			results[idx] = 1
	f.write(pair_ids[i] + ', ' + labels[results[idx]] + '\n')
f.close()

f = open('predict3_' + sys.argv[-2], 'w')
for idx, i in enumerate(i_test):
	if results[idx] == 0:
		results[idx] = setMatchNumKeyField(pairs[i], ['GTIN', 'UPC'])
	if results[idx] == 0:
		results[idx] = setMatchNumKeyField(pairs[i][::-1], ['GTIN', 'UPC'])
	if results[idx] == 0 and results_proba[idx][1] >= 0.2:
		results[idx] = MatchMPN2PN(pairs[i], results_proba[idx])
	if results[idx] == 1 and results_proba[idx][0] >= 0.2:
		results[idx] = NewRefurbished(pairs[i], results_proba[idx])
	if results[idx] == 0 and results_proba[idx][1] >= 0.45:
		if matchWord(pairs[i], 'Product Long Description'):
			results[idx] = 1

	if results[idx] == 0 and (abs(results_proba[idx][0] - results_proba[idx][1]) <= 0.2):
		results[idx] = lessAttributes(pairs[i])
	if results[idx] == 0 and (abs(results_proba[idx][0] - results_proba[idx][1]) <= 0.2):
		results[idx] = lessAttributes(pairs[i][::-1])
	
	f.write(pair_ids[i] + ', ' + labels[results[idx]] + '\n')
f.close()

f = open('probab_' + sys.argv[-2], 'w')
for idx, i in enumerate(i_test):
	f.write(' '.join([str(t) for t in results_proba[idx]]) + '\n')
f.close()
