About the data set
********************
This data set has 20K labeled product pairs from the Electronics domain. Each pair (prod1, prod2) consists of products from two vendors. Out of the 20K pairs, 9930 are matching pairs and 10070 are non-matching pairs. Below is the format in which the file is organized:

+ Each line of the file represents a product pair (prod1, prod2)
+ Each line is of the form: pairId?prod1.id?prod1.json?prod2.id?prod2.json?label
+ note that ? is the delimiter between two fields
+ pairId is a unique string for each pair
+ prod1.id is the ID of prod1; prod2.id is the ID of prod2
+ prod1.json represents details of prod1 in JSON format (which is basically a set of attribute-value pairs); similarly prod2.json is the JSON representation of prod2
+ label is either "MATCH" or "MISMATCH" denoting whether the product pair is matching or not
