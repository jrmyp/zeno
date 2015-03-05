# Feature selection automaton
# I like when everything is done automatically

import sys
import os
import re
import itertools
import random
import Orange
from collections import defaultdict


f_source = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-04-17/socl-season1.relations.csv'
d_all = Orange.data.Table(f_source)
d_source = d_all.filter({'CLASS':'UNRELATED'}, negate=1)

print('Source loaded')
n_folds = 10
c_grouper = 'dialogue'

# Index of grouping attribute
gi = d_source.domain.index(c_grouper)
# List of group names
gnames = list(set(line[gi].value for line in d_source))
# Generate ramdom fold numbers (equally distributed among groups)
f_inds = list(i%n_folds for i in range(len(gnames)))
random.shuffle(f_inds)
# Dict : group name -> fold number
g_folds = dict(zip(gnames, f_inds))
# List of fold numbers (parallel to d_source)
line_folds = list(g_folds[line[gi].value] for line in d_source)
print('Folds created')

learner = Orange.classification.svm.LinearSVMLearner() # Mauvais mais meilleur
#~ learner = Orange.classification.knn.kNNLearner() # Mauvais mais rapide

feats = set(d_source.domain.features)
nsets = ('lex', 'pdtb', ('is', 'has'))
sets = list(set(f for f in feats if f.name.startswith(k))
    for k in nsets)
    
#~ for sel in itertools.product((0,1), repeat=3):
for sel in [[0,0,0], [0,1,0], [1,1,1]]:
    #~ print 'Removed :', list(itertools.compress(nsets, sel))
    cf = set(feats)
    for s in itertools.compress(sets, sel):
        cf -= s
    cd = Orange.data.Domain(list(cf)+[d_source.domain.class_var])
    ct = Orange.data.Table(cd, d_source)
    
    table = defaultdict(lambda : defaultdict(lambda : 0))
    for i_fold in range(n_folds):
        sys.stdout.write('Training fold {0}/{1}...\r'.format(i_fold+1, n_folds))
        sys.stdout.flush()
        d_train, d_test = (ct.select_ref(line_folds, i_fold, negate=b) for b in (True, False))
        classifier = learner(d_train)
        for line in d_test:
            i, j = (k.value for k in (line.getclass(), classifier(line)))
            table[i][j] += 1
    print

    g_match = sum(table[i][j] for i in table for j in table[i] if i==j)
    labels = list(table.keys())
    sum_pred = dict((l, sum(table[i][l] for i in labels)) for l in labels)
    sum_ref  = dict((l, sum(table[l][j] for j in labels)) for l in labels)
    f_scores = list((l, float(2*table[l][l])/(sum_pred[l]+sum_ref[l]))
                        for l in labels)

    print 'Removed :', list(itertools.compress(nsets, sel))
    print len(cd)
    #~ print cd
    print "Global accuracy : {0}/{1} = {2:.3}".format(g_match, len(d_source), float(g_match)/len(d_source))
    print '= F1 scores by label ='
    for l, s in sorted(f_scores, key=lambda x:x[1],reverse=True):
        print '{0:25}: {1:.3}'.format(l, s)
    print
