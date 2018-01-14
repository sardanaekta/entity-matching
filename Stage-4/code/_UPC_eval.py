all_predicted = dict()
all_actual = dict()

fr = open('predict_output_set_X.txt', 'r')
for line in fr:
	data = line.strip().split(', ')
	all_predicted.update({data[0]:data[1]})
fr.close()

fr = open('UPC_set_X.txt', 'r')
for line in fr:
	data = line.strip().split(', ')
	all_actual.update({data[0]:data[2]})
fr.close()

pIDs = dict()

for pID in all_predicted:
	if pID in all_actual:
		pIDs.update({pID:(all_predicted[pID], all_actual[pID])})

FP = 0
TP = 0
Other = 0
for pID in pIDs:
	if pIDs[pID][0] == 'MISMATCH':
		if pIDs[pID][1] == 'MISMATCH':
			FP = FP + 1
		elif pIDs[pID][1] == 'MATCH':
			TP = TP + 1
		else:
			Other = Other + 1
	else:
		Other = Other + 1
print 'Expected FP increase:', FP
print 'Expected TP increase:', TP
print 'Other:', Other
