import re
import os
import sys
import json
from operator import itemgetter
from stop_words import get_stop_words
from py_stringmatching import simfunctions, tokenizers

def DEBUG(debug):
	if IS_DEBUG:
		print debug
	return

def sublistExists(list1, list2):
	return ''.join(map(str, list1)) in ''.join(map(str, list2))

def buildBrandExtractor():
	if os.path.isfile('elec_brand_dic.txt'):
		with open('elec_brand_dic.txt') as f:
			for line in f:
				line = unicode(line, errors='ignore') #For character which are not utf-8
				data = line.strip().split('\t') #.lower()
				brand = data[0]
				brands.update({data[0]:(brands.get(data[0], 0) + int(data[1]))})
			f.close()

	global brands_list, symbol_re, number_re, nonnumber_re, nonAlphaNum_re, brands_re, preposition_re, limitIndex, refurbished_re, CaSe_re, CASE_re

	brands_list = sorted(brands.items(), key=lambda x: len(x[0]))

	symbol_re = re.compile('[^\\w]+', re.IGNORECASE)
	number_re = re.compile('[0-9A-Z]+')
	nonnumber_re = re.compile('[^0-9A-Z][^0-9A-Z]+')
	nonAlphaNum_re = re.compile('[^\\dA-Z]+', re.IGNORECASE)
	brands_re = list()
	for brand, count in brands_list:
		brands_re.append(re.compile('\\b' + symbol_re.sub('[^\\w]{0,3}', brand) + '\\b', re.IGNORECASE))
	#Heuristics
	preposition_re = re.compile('\\bfor|with\\b', re.IGNORECASE)
	limitIndex = 50
	refurbished_re = re.compile('^Off\s*Lease\s*REFURBISHED\s*', re.IGNORECASE)
	CaSe_re = re.compile('^[A-Z]+[a-z]+-?[A-Z]+\\w+\\b')
	CASE_re = re.compile('^[A-Z]{5,}\\b') #CAPS, but not A, AN, THE, etc.

	return

def extractBrand(productName):
	#if not BRAND_EXTRACTOR:
	#	buildBrandExtractor()
	try:
		matched = CaSe_re.search(productName).group(0)
	except:
		matched = None
	try:
		for idx, brand in enumerate(brands_re):
			match = brand.search(productName)
			if match is not None:
				if matched == None:
					matched = match.group(0)
				else:
					matchIndex = refurbished_re.sub('', productName).index(match.group(0))
					matchedIndex = refurbished_re.sub('', productName).index(matched)
					if matchIndex <= matchedIndex:
						matched = match.group(0)
		if matched is None:
			try:
				matched = CASE_re.search(productName).group(0)
			except:
				matched = None
		if matched is not None:
			matchedIndex = refurbished_re.sub('', productName).index(matched)
			if matchedIndex > limitIndex:
				matched = None
		if matched is not None:
			matchedIndex = productName.index(matched)
			prepositionMatch = preposition_re.search(productName)
			if prepositionMatch is not None:
				prepositionIndex = productName.index(prepositionMatch.group(0))
				if prepositionIndex < matchedIndex:
					matched = None
	except:
		print >> sys.stderr, productName
		matched = None
	return matched

def initMain():
	with open(sys.argv[1]) as f:
		inputLines = f.readlines()
		f.close()
	global BRAND_EXTRACTOR, products, attributes, pairs, brands, stop_words
	BRAND_EXTRACTOR = False
	products = dict()
	attribute_counts = dict()
	pairs = list()
	brands = dict()
	stop_words = set()
	stop_words.update(get_stop_words('en'))

	html_re = re.compile('((<[^<]*?>)|(&nbsp))+', re.IGNORECASE)
	junk_re = re.compile('[;]+', re.IGNORECASE)

	for line in inputLines:
		line = unicode(line, errors='ignore') #For character which are not utf-8
		line = junk_re.sub(' ', html_re.sub('', line))
		data = line.strip().split('?')

		pairId = data[0]
		prod1_id = data[1] + '_1'
		if (data[2]):
			prod1_json = json.loads(data[2])
		else:
			prod1_json = dict()
		prod2_id = data[3] + '_2'
		if (data[4]):
			prod2_json = json.loads(data[4])
		else:
			prod2_json = dict()
		products.update({prod1_id:prod1_json})
		products.update({prod2_id:prod2_json})
		pairs.append((prod1_id, prod2_id))
		for k in prod1_json.keys():
			attribute_counts.update({k:(attribute_counts.get(k, 0) + 1)})
		for k in prod2_json.keys():
			attribute_counts.update({k:(attribute_counts.get(k, 0) + 1)})
		if prod1_json.get('Brand', None) is not None:
			brands.update({prod1_json['Brand'][0]:(brands.get(prod1_json['Brand'][0], 0) + 1)})
		if prod2_json.get('Brand', None) is not None:
			brands.update({prod2_json['Brand'][0]:(brands.get(prod2_json['Brand'][0], 0) + 1)})

	attributes = sorted(attribute_counts.items(), key=itemgetter(1), reverse=True)
	attributes = [x[0] for x in attributes]
	return

def updateMPN(product):
	if products[product].get('Manufacturer Part Number', None) is not None:
		mpn = products[product].get('Manufacturer Part Number', None)[0].strip().split()
		if ' ' in mpn:
			for idx in range(0, len(mpn)):
				if mpn[idx] in brands_list:
					mpn[idx] = ''
			mpn = ' '.join(' '.join(mpn).split())
			products[product].update({'Manufacturer Part Number':[mpn]})
	return

def updateBrand(product):
	if products[product].get('Brand', None) is None:
		brand = extractBrand(products[product].get('Product Name', [''])[0])
		if brand is not None:
			products[product].update({'Brand':[brand]})
	return

def updateAllBrands():
	for p in products:
		updateBrand(p)
	return

def delNumber(product, feature):
	featureValue = ''
	if products[product].get(feature, None) is not None:
		featureValue = number_re.sub('', products[product].get(feature)[0])
	return featureValue

def delNonNumber(product, feature):
	featureValue = ''
	if products[product].get(feature, None) is not None:
		featureValue = nonnumber_re.sub(' ', products[product].get(feature)[0]).strip()
	return featureValue

def monge_elkan(pair, feature):
	if feature in products[pair[0]] and feature in products[pair[1]]:
		return simfunctions.monge_elkan(tokenizers.whitespace(products[pair[0]].get(feature, [''])[0].lower()), tokenizers.whitespace(products[pair[1]].get(feature, [''])[0].lower()))
	else:
		return noneValue

def overlap_coefficient(pair, feature):
	if feature in products[pair[0]] and feature in products[pair[1]]:
		val = [products[pair[0]].get(feature, [''])[0].lower(), products[pair[1]].get(feature, [''])[0].lower()]
		val[0] = ' '.join([word for word in val[0].split() if word not in stop_words])
		val[1] = ' '.join([word for word in val[1].split() if word not in stop_words])
		return simfunctions.overlap_coefficient(tokenizers.whitespace(val[0]), tokenizers.whitespace(val[1]))
	else:
		return noneValue

def isDifferentModel_1(pair, feature):
	if feature in products[pair[0]] and feature in products[pair[1]]:
		return simfunctions.overlap_coefficient(tokenizers.qgram(delNumber(pair[0], feature), 3), tokenizers.qgram(delNumber(pair[1], feature), 3))
	else:
		return noneValue

def isDifferentModel_2(pair, feature):
	if feature in products[pair[0]] and feature in products[pair[1]]:
		return simfunctions.overlap_coefficient(tokenizers.qgram(delNonNumber(pair[0], feature), 3), tokenizers.qgram(delNonNumber(pair[1], feature), 3))
	else:
		return noneValue

def getFeatureVector(pair):
	featureVector = list()
	for feature in features:
		featureVector.append('{0:.3f}'.format(monge_elkan(pair, feature)))
		featureVector.append('{0:.3f}'.format(overlap_coefficient(pair, feature)))
		featureVector.append('{0:.3f}'.format(isDifferentModel_1(pair, feature)))
		featureVector.append('{0:.3f}'.format(isDifferentModel_2(pair, feature)))
	return featureVector

def main():
	initMain()
	buildBrandExtractor()

	global features, noneValue
	num_attributes = len(attributes)
	if len(sys.argv) > 2:
		num_attributes = int(sys.argv[2])
	features = attributes[0:num_attributes]
	idx_MPN = features.index('Manufacturer Part Number')
	idx_AC = features.index('Actual Color')
	noneValue = 0
	num_feature_variants = 4 #Edit accordingly
	featureNames = list()
	for feature in features:
		f = symbol_re.sub('', feature)
		for i in range(0, num_feature_variants):
			featureNames.append(f + '_' + str(i))
	print ' '.join(featureNames)
	for pair in pairs:
		updateBrand(pair[0])
		updateBrand(pair[1])
		featureVector = getFeatureVector(pair)

		updateMPN(pair[0])
		updateMPN(pair[1])
		if 'Manufacturer Part Number' in products[pair[0]]:
			if nonAlphaNum_re.sub('', products[pair[0]]['Manufacturer Part Number'][0]).lower() in nonAlphaNum_re.sub('', str(products[pair[1]].values())).lower():
				featureVector[4*idx_MPN + 0] = '1.000'
				featureVector[4*idx_MPN + 1] = '1.000'
				featureVector[4*idx_MPN + 2] = '1.000'
				featureVector[4*idx_MPN + 3] = '1.000'
		elif 'Manufacturer Part Number' in products[pair[1]]:
			if nonAlphaNum_re.sub('', products[pair[1]]['Manufacturer Part Number'][0]).lower() in nonAlphaNum_re.sub('', str(products[pair[0]].values())).lower():
				featureVector[4*idx_MPN + 0] = '1.000'
				featureVector[4*idx_MPN + 1] = '1.000'
				featureVector[4*idx_MPN + 2] = '1.000'
				featureVector[4*idx_MPN + 3] = '1.000'

		if 'Actual Color' in products[pair[0]]:
			if nonAlphaNum_re.sub('', products[pair[0]]['Actual Color'][0]).lower() in nonAlphaNum_re.sub('', str(products[pair[1]].values())).lower():
				featureVector[4*idx_AC + 0] = '1.000'
				featureVector[4*idx_AC + 1] = '1.000'
				featureVector[4*idx_AC + 2] = '1.000'
				featureVector[4*idx_AC + 3] = '1.000'
		elif 'Actual Color' in products[pair[1]]:
			if nonAlphaNum_re.sub('', products[pair[1]]['Actual Color'][0]).lower() in nonAlphaNum_re.sub('', str(products[pair[0]].values())).lower():
				featureVector[4*idx_AC + 0] = '1.000'
				featureVector[4*idx_AC + 1] = '1.000'
				featureVector[4*idx_AC + 2] = '1.000'
				featureVector[4*idx_AC + 3] = '1.000'

		print ' '.join(featureVector)
	return

if __name__ == '__main__':
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print >> sys.stderr, 'Usage: python ' + sys.argv[0] + ' <input> [<num_attributes>]'
		exit()
	global IS_DEBUG
	IS_DEBUG = False
	main()
