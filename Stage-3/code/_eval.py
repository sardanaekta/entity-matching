#Usage: python _eval.py <test_json_file> <test_predict_file>

import sys

if len(sys.argv) != 3:
	print 'Invalid number of arguments.'
	print 'Usage: python ' + sys.argv[0] + ' <json_file> <predict_file>'
	exit()

pair_label = dict()
with open(sys.argv[1], 'r') as fj:
    for line in fj:
        line = unicode(line, errors='ignore') #For character which are not utf-8
        data = line.strip().split('?')
        pairId = data[0]
        label = data[5]
        pair_label.update({pairId:label})
    fj.close()

TP = 0
FP = 0
TN = 0
FN = 0
with open(sys.argv[2], 'r') as fp:
    for line in fp:
        line = unicode(line, errors='ignore') #For character which are not utf-8
        data = line.strip().split(', ')
        pairId = data[0]
        label = data[1]
        if label == 'MATCH':
            if pair_label[pairId] == 'MATCH':
                TP = TP + 1
            elif pair_label[pairId] == 'MISMATCH':
                FP = FP + 1
        elif label == 'MISMATCH':
            if pair_label[pairId] == 'MATCH':
                FN = FN + 1
            elif pair_label[pairId] == 'MISMATCH':
                TN = TN + 1
    fp.close()

Acc = 100*(TP+TN)/float(TP+FP+FN+TN)
Pre = 100*(TP)/float(TP+FP)
Rec = 100*(TP)/float(TP+FN)
F1S = 2*(Pre*Rec)/float(Pre+Rec)

print 'Acc\tPre\tRec\tF1S'
print round(Acc,2), '\t', round(Pre,2), '\t', round(Rec,2), '\t', round(F1S,2)

print 'TP\t=> ', TP
print 'FP\t=> ', FP
print 'FN\t=> ', FN
print 'TN\t=> ', TN
print 'TOTAL\t=> ', (TP+FP+FN+TN)
