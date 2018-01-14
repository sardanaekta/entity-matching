#Usage: python _reprocess_ActualColor.py <output_file> <json_file>

import sys
import re
import json

fr_attr = open(sys.argv[1], 'r')
fr_json = open(sys.argv[2], 'r')

header = fr_attr.readline().strip().split()
idx_AC_0 = header.index('ActualColor_0')

html_re = re.compile('((<[^<]*?>)|(&nbsp))+', re.IGNORECASE)
junk_re = re.compile('[;]+', re.IGNORECASE)

idx_line = 0
AC_indices = list()
nonAC_re = re.compile('[^\\dA-Z]+', re.IGNORECASE)
for line in fr_json:
	line = unicode(line, errors='ignore') #For character which are not utf-8
	line = junk_re.sub(' ', html_re.sub('', line))
	data = line.strip().split('?')

	if data[2]:
		prod1_json = json.loads(data[2])
	else:
		prod1_json = dict()
	if data[4]:
		prod2_json = json.loads(data[4])
	else:
		prod2_json = dict()

	if 'Actual Color' in prod1_json:
		if nonAC_re.sub('', prod1_json['Actual Color'][0]).lower() in nonAC_re.sub('', data[4]).lower():
			AC_indices.append(idx_line)
	elif 'Actual Color' in prod2_json:
		if nonAC_re.sub('', prod2_json['Actual Color'][0]).lower() in nonAC_re.sub('', data[2]).lower():
			AC_indices.append(idx_line)
	idx_line = idx_line + 1
fr_json.close()

print ' '.join(header)
idx_line = 0
for line in fr_attr:
	line = line.strip().split()
	if idx_line in AC_indices:
		line[idx_AC_0 + 0] = '1.000'
		line[idx_AC_0 + 1] = '1.000'
		line[idx_AC_0 + 2] = '1.000'
		line[idx_AC_0 + 3] = '1.000'
	print ' '.join(line)
	idx_line = idx_line + 1
fr_attr.close()
