import os
import sys
import re
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB

class Logger(object):
  def __init__(self, filename):
    self.terminal = sys.stdout
    self.log = open(filename, 'w')
  
  def write(self, message):
    self.terminal.write(message)
    self.log.write(message)

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print 'Invalid number of arguments.'
  print 'Usage: python _NB.py <input_file> [<filename_suffix>]'
  exit()

with open(sys.argv[1], 'r') as f:
  length = len(f.readline().strip().split(' '))

#Read
_data = np.genfromtxt(sys.argv[1], dtype=float, delimiter=' ', skip_header=1, usecols=range(1, length))

#Output filename
filename = 'NB_' + sys.argv[1][:sys.argv[1].rfind('.')]
for i in range(2, len(sys.argv)):
  filename = filename + '_' + sys.argv[i]
filename = filename + '.txt'
sys.stdout = Logger(filename)

#Seperate features from labels
X_data = _data[:, range(0, _data.shape[1]-1)]
y_data = _data[:, _data.shape[1]-1]

#Set random_state=0 for testing
X_train, X_test, y_train, y_test, i_train, i_test = train_test_split(X_data, y_data, range(0, len(y_data)), test_size=0.20)

classifier = GaussianNB()

classifier.fit(X_train, y_train)

old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
results = classifier.predict(X_test) #May produce junk output
results_proba = classifier.predict_proba(X_test) #May produce junk output
sys.stdout.close()
sys.stdout = old_stdout

results = np.reshape(results, (results.shape[0], 1))
results_proba = np.reshape(results_proba, (results.shape[0], 2))
y_test = np.reshape(y_test, results.shape)

Acc = 100*(results == y_test).sum()/float(len(y_test))
Pre = 100*(np.logical_and(results == 1, y_test == 1)).sum()/float((results == 1).sum())
Rec = 100*(np.logical_and(results == 1, y_test == 1)).sum()/float((y_test == 1).sum())
F1S = 2*(Pre*Rec)/float(Pre+Rec)

print 'Acc\tPre\tRec\tF1S'
print round(Acc,2), '\t', round(Pre,2), '\t', round(Rec,2), '\t', round(F1S,2)

print 'TP\t=> ', (np.array(results == 1) & np.array(y_test == 1)).sum()
print 'FP\t=> ', (np.array(results == 1) & np.array(y_test == 0)).sum()
print 'TN\t=> ', (np.array(results == 0) & np.array(y_test == 0)).sum()
print 'FN\t=> ', (np.array(results == 0) & np.array(y_test == 1)).sum()

f = open('debug_' + filename, 'w')
f.write('INDEX\tACT\tPRE\tNEG_P\tPOS_P')
for idx, y in enumerate(y_test):
  f.write('\n{0:5}'.format(i_test[idx]))
  f.write('\t' + str(int(y_test[idx][0])) + '\t' + str(int(results[idx][0])))
  f.write('\t{0:.3f}'.format(results_proba[idx][0]) + '\t{0:.3f}'.format(results_proba[idx][1]))
f.close()
