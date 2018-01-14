#Usage: python _faults.py <debug_file> <json_file>

import sys

fr_file = open(sys.argv[1], 'r')
fr_json = open(sys.argv[2], 'r')
'''
if 'MPN' in sys.argv[1]:
  fr_attr = open(sys.argv[1].split('_', 2)[-1].rsplit('_', 3)[0] + '.txt', 'r')
elif 'RUN' in sys.argv[1]:
  fr_attr = open(sys.argv[1].split('_', 2)[-1].rsplit('_', 2)[0] + '.txt', 'r')
else:
  fr_attr = open(sys.argv[1].split('_', 2)[-1].rsplit('_', 1)[0] + '.txt', 'r')
'''

fw_fp_json = open('json_FP_' + sys.argv[1], 'w')
#fw_fp_attr = open('attr_FP_' + sys.argv[1], 'w')
fw_fn_json = open('json_FN_' + sys.argv[1], 'w')
#fw_fn_attr = open('attr_FN_' + sys.argv[1], 'w')

fr_file.next()
#header = fr_attr.readline()
#fw_fp_attr.write(header)
#fw_fn_attr.write(header)

p_json = fr_json.readlines()
#p_attr = fr_attr.readlines()

for line in fr_file:
  data = line.strip().split()
  if data[1] == '0' and data[2] == '1':
    json = p_json[int(data[0])].split('?')
    json = json[0] + '\n' + '[' + json[2] + ', ' + json[4] + ']\n'
    fw_fp_json.write(json)
    #fw_fp_attr.write(p_attr[int(data[0])])
  elif data[1] == '1' and data[2] == '0':
    json = p_json[int(data[0])].split('?')
    json = json[0] + '\n' + '[' + json[2] + ', ' + json[4] + ']\n'
    fw_fn_json.write(json)
    #fw_fn_attr.write(p_attr[int(data[0])])
  else:
    continue

fr_file.close()
fr_json.close()
#fr_attr.close()
fw_fp_json.close()
#fw_fp_attr.close()
fw_fn_json.close()
#fw_fn_attr.close()
