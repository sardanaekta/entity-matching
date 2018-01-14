COMP SCI 784, Spring 2016
Group#25

Members:
- Amrita Roy Chowdhury
- Ekta Sardana
- Roney Michael

Results on set Y: results_reorder_output_unknown_set_Y.txt
- Contains various measures computed on the set-aside set Y after 5 fold cross-validated development and training on set X.
- We used a random forest classifier (RFC) with 100 estimators and the entropy criterion.
- Our feature set includes roughly 585x4 features (based on all possible json fields in set X, computed in 4 different ways each). We noticed that taking only the top 15 most frequent attributes (15x4 features) gave us more or less the same performance, but we decided to keep everything in the mix, since RFCs are known to be highly resistant to overfitting. This means that extra/unnecessary features might yeild no new information or might end up being helpful; the RFC is resiliant enough to handle this on it's own without any special tweaking.
- With the default threshold of 0.5 for the confidence score, we were obtaining precision and recall of 95.xx and 91.xx respectively for 5-fold cross-validation on set X. Since we wanted precision to be slightly higher, we conservatively increased the confidence threshold to 0.55, which is what the output results are based on.
- Five back-to-back experimental runs were conducted on set Y after development was completed and all 5 are reported in the results file.
- Our final average scores for precision, recall and f1 score were 96.05%, 90.19% and 93.03% respectively.

