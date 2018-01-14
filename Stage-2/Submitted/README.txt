COMP SCI 784, Spring 2016
Group#25

Members:
- Amrita Roy Chowdhury
- Ekta Sardana
- Roney Michael

Golden Data: sample_350.tsv
- The file is in the industry standard tsv format
- The first line indicating the fields and each other line corresponding to 1 instance each.
- A Google sheet is available with the same data for easy viewing, at https://docs.google.com/a/wisc.edu/spreadsheets/d/1f2wqiV1arxHMTC1yOO9egOrbiUGyKTjVmcn3IMvF6_k/
- Format=<sl_no><tab><product_id><tab><product_json><tab><product_name><tab><brand_name>

Development Set, I: _dev_set.tsv
- The file is in the industry standard tsv format
- There is no header line; each on the 230 lines corresponds to a distinct product from the golden data
- Format=<product_id><tab><product_name>(<tab><brand_name>)?

Test Set, J: _test_set.tsv
- The file is in the industry standard tsv format
- There is no header line; each on the 120 lines corresponds to a distinct product from the golden data
- Format=<product_id><tab><product_name>(<tab><brand_name>)?

Code: cs784stage2.py
- Usage=python cs784stage2.py elec_brand_dic.txt _dev_set.tsv _test_set.tsv
- As provided the code will be evaluated against _test_set.tsv
- Four flags are provided (VALIDATION_RUN, VALIDATION_SIZE, ALLOW_PARTIAL & IS_DEBUG) which may be manipulated to run the code for validation trials, to allow partial matching or to debug results; the names for these are self-explanatory.

Report: CS784-Stage2-Group25.pdf
