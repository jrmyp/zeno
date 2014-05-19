# I hereby declare war to procrastination, despair & weakness
# Let my work begin, and never stop

from __future__ import print_function
import sys
import os
import random
import Orange
from collections import defaultdict

#~ f_attach = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-04-10/tmp/socl-season1.edu-pairs.csv'
#~ f_source = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-04-10/tmp/socl-season1.relations.csv'
#~ f_attach = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-04-17/socl-season1.edu-pairs.csv'
f_source = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-05-01/socl-season1.relations.csv'
#~ 
d_all = Orange.data.Table(f_source)
d_source = d_all.filter({'CLASS':'UNRELATED'}, negate=1)

#~ f_source = '/home/arthur/These/Data/socl-season1.merged.tab'
#~ f_source = '/home/arthur/These/Data/socl-season1.turns.tab'
#~ d_source = Orange.data.Table(f_source)

print('Source loaded')
n_folds = 10
c_grouper = 'dialogue'

# Index of grouping attribute
gi = d_source.domain.index(c_grouper)
# List of group names
gnames = list(set(line[gi].value for line in d_source))
# Generate random fold numbers (equally distributed among groups)
f_inds = list(i%n_folds for i in range(len(gnames)))
random.shuffle(f_inds)
# Dict : group name -> fold number
g_folds = dict(zip(gnames, f_inds))
# List of fold numbers (parallel to d_source)
line_folds = list(g_folds[line[gi].value] for line in d_source)
print('Folds created')

#~ learner = Orange.classification.bayes.NaiveLearner() # Pire de tous (eh ben)
learner = Orange.classification.svm.LinearSVMLearner() # Mauvais mais meilleur
#~ learner = Orange.classification.svm.MultiClassSVMLearner() # Mauvais mais meilleur
#~ learner = Orange.classification.knn.kNNLearner() # Mauvais mais rapide
#~ learner = Orange.classification.neural.NeuralNetworkLearner() # Can't work : not all numeric
#~ learner = Orange.classification.logreg.LogRegLearner(stepwise_lr=True) # Can't work : not binary

table = defaultdict(lambda : defaultdict(lambda : 0))
for i_fold in range(n_folds):
    print('Training fold {0}/{1}...\r'.format(i_fold+1, n_folds), end='')
    sys.stdout.flush() 
    d_train, d_test = (d_source.select_ref(line_folds, i_fold, negate=b) for b in (True, False))
    classifier = learner(d_train)
    for line in d_test:
        # Standard classification
        i, j = (k.value for k in (line.getclass(), classifier(line)))
        # All-the-same baseline
        #~ i, j = line.getclass().value, 'True'
        # Random baseline
        #~ i, j = line.getclass().value, random.choice(('True', 'False'))
        table[i][j] += 1

print()
for i in table:
    for j in table[i]:
        pass
        #~ print(i, j, table[i][j])

labels = list(table.keys())
sum_pred = dict((l, sum(table[i][l] for i in labels)) for l in labels)
sum_ref  = dict((l, sum(table[l][j] for j in labels)) for l in labels)
f_scores = list((l, float(2*table[l][l])/(sum_pred[l]+sum_ref[l]))
                    for l in labels)
g_match = sum(table[i][j] for i in table for j in table[i] if i==j)
x_match = g_match - table['UNRELATED']['UNRELATED']
x_count = sum(table[i][j] for i in table for j in table[i] if i!='UNRELATED')

print("== File : {0} ==".format(os.path.basename(f_source)))
print("== Method : {0} ==".format(learner.name))
print("Global accuracy : {0}/{1} = {2:.3}".format(g_match, len(d_source), float(g_match)/len(d_source)))
#~ print("Restricted accuracy : {0}/{1} = {2:.3}".format(x_match, x_count, float(x_match)/x_count))

print('= F1 scores by label =')
for l, s in sorted(f_scores, key=lambda x:x[1],reverse=True):
    print('{0:25}: {1:.3}'.format(l, s))

# F1 : 2TP / (2TP+FP+FN)

print('= Reference counts =')
for l, c in sorted(list(sum_ref.items()), key=lambda x:x[1],reverse=True):
    print('{0:25}: {1}'.format(l, c))

