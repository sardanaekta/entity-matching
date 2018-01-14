import json
from py_stringmatching import simfunctions,tokenizers

prodNames = []
cosineMeasure = []
with open ('set_X.txt','r') as f:
    for line in f:
        line = unicode(line, errors='ignore')  # For character which are not utf-8
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
        prodNames.append((prod1_json['Product Name'][0], prod2_json['Product Name'][0]))
    f.close()
    for pair in prodNames:
        measure = simfunctions.cosine(tokenizers.whitespace(pair[0]), tokenizers.whitespace(pair[1]))
        cosineMeasure.append(measure)
    print cosineMeasure

