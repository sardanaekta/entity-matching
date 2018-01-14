import os
import sys
import re
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier

#Global flag variables
IS_VALIDATION = False

if IS_VALIDATION:
  if len(sys.argv) != 4:
    print 'Invalid number of arguments.'
    print 'Usage: python ' + sys.argv[0] + ' <input_file> <json_input_file> <pos_thresh>'
    exit()
else:
  if len(sys.argv) != 5:
    print 'Invalid number of arguments.'
    print 'Usage: python ' + sys.argv[0] + ' <train_file> <test_file> <json_test_file> <pos_thresh>'
    exit()

pos_thresh = float(sys.argv[-1])

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

  #Set random_state=0 for testing
  X_train, X_test, y_train, y_test, i_train, i_test = train_test_split(X_data, y_data, range(0, len(y_data)), test_size=0.20)
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

classifier = RandomForestClassifier(n_estimators=100, n_jobs=-1, criterion='entropy')

classifier.fit(X_train, y_train)

old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
results = classifier.predict(X_test) #May produce junk output
results_proba = classifier.predict_proba(X_test) #May produce junk output
sys.stdout.close()
sys.stdout = old_stdout

for idx in range(0, len(results)):
  if results_proba[idx][1] < pos_thresh:
    results[idx] = 0

pair_ids = list()
if IS_VALIDATION:
  with open(sys.argv[2], 'r') as fr:
    for line in fr:
      pair_ids.append(line.strip().split('?')[0])
    fr.close()
  f = open('predict_' + sys.argv[1], 'w')
else:
  with open(sys.argv[3], 'r') as fr:
    for line in fr:
      pair_ids.append(line.strip().split('?')[0])
    fr.close()
  f = open('predict_' + sys.argv[2], 'w')

labels = dict()
labels.update({1:'MATCH'})
labels.update({0:'MISMATCH'})
for idx, i in enumerate(i_test):
  f.write(pair_ids[i] + ', ' + labels[results[idx]] + '\n')
f.close()
