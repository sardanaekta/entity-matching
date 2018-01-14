import sys

if len(sys.argv) != 3:
  print 'python _reorder.py <output_train> <output_test>'
  exit();

with open(sys.argv[1], 'r') as fr:
  header1 = fr.readline().strip().split()
  fr.close()

with open(sys.argv[2], 'r') as fr:
  header2 = fr.readline().strip().split()
  fr.close()

header1_idx2 = list()
for h in header1:
  try:
    header1_idx2.append(header2.index(h))
  except:
    if h != 'Label':
      header1_idx2.append(-1)

with open(sys.argv[2], 'r') as fr:
  fw = open('reorder_' + sys.argv[2], 'w')
  for line in fr:
    data2 = line.strip().split()
    data2_idx1 = list()

    for idx in header1_idx2:
      if idx >= 0:
        data2_idx1.append(data2[idx])
      else:
        data2_idx1.append('0')
    fw.write(' '.join(data2_idx1) + '\n')
  fw.close()
  fr.close()
