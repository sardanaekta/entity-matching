import sys

if len(sys.argv) != 3:
	print 'Usage: python ' + sys.argv[0] + ' <predict_file> <json_file>'
	exit();

fr_file = open(sys.argv[1], 'r')
fr_json = open(sys.argv[2], 'r')

fw_fp_json = open('json_FP_' + sys.argv[1], 'w')
fw_fn_json = open('json_FN_' + sys.argv[1], 'w')

p_json = fr_json.readlines()
actual_labels = dict()
pairs = dict()

for p_j in p_json:
	data = p_j.strip().split('?')
	actual_labels.update({data[0]:data[5]})
	pairs.update({data[0]:p_j})

for line in fr_file:
	data = line.strip().split(', ')
	if data[1] == 'MATCH' and actual_labels[data[0]] == 'MISMATCH':
		json = pairs[data[0]].split('?')
		json = json[0] + '\n' + '[' + json[2] + ', ' + json[4] + ']\n'
		fw_fp_json.write(json)
	elif data[1] == 'MISMATCH' and actual_labels[data[0]] == 'MATCH':
		json = pairs[data[0]].split('?')
		json = json[0] + '\n' + '[' + json[2] + ', ' + json[4] + ']\n'
		fw_fn_json.write(json)
	else:
		continue

fr_file.close()
fr_json.close()
fw_fp_json.close()
fw_fn_json.close()
