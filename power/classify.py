# Wrapping classification operations
# Cleaner scripting was needed

from __future__ import print_function
import sys
import os
import random
import Orange
import valmerger
from collections import defaultdict

# Temporary table savefile
TMP = 'tmp.tab'

class Trainer:
    """ Everything you want for your training needs """
    
    def __init__(self, data, n_folds=10, grouper=None, learner='svm', baseline=False):
        """ Class initialiser
            Builds classifiers for data
            Learner is LinearSVM (reliable, quick and versatile)
            data (TabData): training data
            n_folds (int): number of training folds
            grouper (str): grouping attribute for folds
        """
        self.data = data.t
        self.n_folds = n_folds
        self.grouper = grouper

        # Select learner
        if learner == 'logreg':
            self.learner = Orange.classification.logreg.LogRegLearner(stepwise_lr=True)
        else:
            self.learner = Orange.classification.svm.LinearSVMLearner()
                
        # Do not train if baseline mode
        if baseline:
            return
        
        # Create folds
        if grouper is None:
            lf = list(i%n_folds for i in range(len(self.data)))
            random.shuffle(lf)
            self.line_folds = lf
        else:
            # List of group names
            gnames = list(set(line[grouper].value for line in self.data))
            # Generate random fold numbers (equally distributed among groups)
            f_inds = list(i%n_folds for i in range(len(gnames)))
            random.shuffle(f_inds)
            # Dict : group name -> fold number
            g_folds = dict(zip(gnames, f_inds))
            # Fold selector (parallel to data)
            self.line_folds = list(g_folds[line[grouper].value] for line in self.data)

        self.classifiers = dict()
        for i_fold in range(self.n_folds):
            print('Training fold {0}/{1}...\r'.format(i_fold+1, self.n_folds), end='')
            sys.stdout.flush() 
            d_train = self.data.select_ref(self.line_folds, i_fold, negate=True)
            self.classifiers[i_fold] = self.learner(d_train)
        print('\nTraining complete !')

    def pred_rows(self):
        """ Yields predictions (predicted class, row) """
        for i_fold in range(self.n_folds):
            d_test = self.data.select_ref(self.line_folds, i_fold)
            cls = self.classifiers[i_fold]
            for row in d_test:
                yield cls(row), row
    
    def evaluate(self, title='Results', quiet=False):
        """ Print some statistics about predictions """
        res = defaultdict(lambda : defaultdict(int))
        for pred, row in self.pred_rows():
        #~ for row in self.data:
            i = row.getclass().value
            # Standard classification
            j = pred.value
            # Res name baseline
            #~ j = row['has_res'].value
            # Random baseline
            #~ j = str(random.random() < 452./2201)
            # Clue baseline
            #~ j = str(row['clue_resource'].value == 'True' or row['unclue_resource'].value == 'True')
            res[i][j] += 1

        # Process results
        labels = list(res.keys())
        sum_pred = dict((l, sum(res[i][l] for i in labels)) for l in labels)
        sum_ref  = dict((l, sum(res[l][j] for j in labels)) for l in labels)
        # F1 : 2TP / (2TP+FP+FN)
        f_scores = list((l, float(2*res[l][l])/(sum_pred[l]+sum_ref[l]))
                            for l in labels)
        g_match = sum(res[l][l] for l in labels)

        # Display results
        if not quiet:
            print("== {0} ==".format(title))
            print("== Method : {0} ==".format(self.learner.name))
            print("Global accuracy : {0}/{1} = {2:.3}".format(g_match, len(self.data), float(g_match)/len(self.data)))

            print('= F1 scores by label =')
            for l, s in sorted(f_scores, key=lambda x:x[1],reverse=True):
                print('{0:25}: {1:.3}'.format(l, s))

            print('= Precision and recall =')
            print('{0:25}{1:7}{2:7}'.format('Name', 'Pre', 'Rec'))
            for l in labels:
                print('{0:25}{1:7.3}{2:7.3}'.format(l,
                    float(res[l][l])/sum_pred[l],
                    float(res[l][l])/sum_ref[l]))
            
            print('= Reference counts =')
            for l, c in sorted(list(sum_ref.items()), key=lambda x:x[1],reverse=True):
                print('{0:25}: {1}'.format(l, c))
            
            print('== Confusion matrix ==')
            kl = list(res.keys())
            #~ print('{0:8}{1:>8}{2:>8}'.format(*([r'R\P']+kl)))
            print('\t'.join([r'R\P']+kl))
            for ki in kl:
                #~ ks = [res[ki][kj] for kj in kl]
                #~ print('{0:8}{1:>8}{2:>8}'.format(*([ki]+ks)))
                ks = [str(res[ki][kj]) for kj in kl]
                print('\t'.join([ki]+ks))
                                    
        return dict(f_scores)

class TabData:
    """ Wrapper for Orange.data.Table """
    
    def __init__(self, dsource, copy=False):
        """ Class initialiser """
        if copy:
            self.t = dsource.t
        else:
            self.t = Orange.data.Table(dsource)

    def __iter__(self):
        """ Iterate over the table """
        return iter(self.t)

    def __len__(self):
        """ Length of table """
        return len(self.t)

    def save(self, name):
        """ Save table in file """
        self.t.save(name)
    
    def sel_row(self, *a, **ka):
        """ Filter rows Orange-style """
        self.t = self.t.filter(*a, **ka)
    
    def sel_row_by(self, fun):
        """ Filter rows by function """
        self.t = self.t.select(map(fun, self.t))
        
    def sel_col(self, atts=None, metas=[], new_class=None):
        """ Filter columns
            atts : attributes (including class) to keep (default: all)
            metas : meta attributes to keep (default: none)
            new_class : class name for the new domain (default: previous one)
        """
        nd = d = self.t.domain
        if atts is not None:
            nd = Orange.data.Domain(atts, nd)
        for nmeta in metas:
            nd.add_meta(d.meta_id(nmeta), d.get_meta(nmeta))
        self.t = Orange.data.Table(nd, self.t)
        if new_class is not None:
            self.new_class(new_class)

    def new_class(self, name):
        """ Switch class attribute name """
        nd = Orange.data.Domain(self.t.domain, name)
        nd.add_metas(self.t.domain.get_metas())
        self.t = Orange.data.Table(nd, self.t)

    # Soon deprecated
    def merge(self, other, id='id'):
        """ Merge with another table
            other : the other table
            id : row identifier attribute name
            returns lists of non-common ids
        """
        # Filter out non-common ids
        si, ti = (set(r[id].value for r in obj.t) for obj in (self, other))
        sx, tx = list(si-ti), list(ti-si)
        st = self.t.filter_ref({id:sx}, negate=1)
        tt = other.t.filter_ref({id:tx}, negate=1)
        # Reorder data (same order required for merging)
        st.sort([id])
        tt.sort([id])
        self.t = Orange.data.Table([st,tt])
        return sx, tx
    
    def newmerge(self, other, ids='id'):
        """ Merge with another table
            other : the other table
            ids : row identifier attribute names
            returns lists of non-common ids
        """
        mids = ids if isinstance(ids, tuple) else tuple(ids)
        def uid(r):
            return '#'.join(str(r[i].value) for i in mids)
        si, ti = (set(uid(r) for r in obj.t) for obj in (self, other))
        sx, tx, ci = list(si-ti), list(ti-si), si&ti
        for obj in (self, other):
            obj.sel_row_by(lambda r: uid(r) in ci)
        # Reorder data (same order required for merging)
        self.t.sort(ids)
        other.t.sort(ids)
        self.t = Orange.data.Table([self.t, other.t])
        return sx, tx
    
    
    def tab_header(self):
        """ Create Orange tab header and feature name list """
        def tri(f, tag):
            return (f.name, str(f.var_type)[0].lower(), tag)
        
        d = self.t.domain
        # ff : list of (name, c/d, meta/class/'')
        ff = [tri(d.class_var, 'class')] if d.class_var else []
        ff += ([tri(f, 'meta') for f in d.get_metas().values()] +
               [tri(f, '') for f in d.attributes])
        # Header, on 3 lines (Orange tab format)
        h = ''
        for k in range(3):
            h += '\t'.join([t[k] for t in ff]) + '\n'
        # Feature name list, in order
        fl = list(t[0] for t in ff)
        return h, fl

    def fuse_rows(self, grouper, sort=None):
        """ Merge groups of rows
            Return the fused table !
                TODO : in-place is better
            grouper : row grouping attribute
            sorter : positioning attribute
        """
        sorter = (lambda x:x[sort].value) if sort else (lambda x:0)
        head, fnames = self.tab_header()
        mergers = valmerger.gen_vm(fnames)

        groups = defaultdict(list)
        for r in self.t:
            groups[r[grouper].value].append(r)

        with open(TMP, 'w') as f:
            f.write(head)
            for rl in groups.values():
                # Sort turn rows by position
                rlis = sorted(rl, key=sorter)
                # Collect and apply mergers
                vals = [rlis[0][n].value for n in fnames]
                for r in rlis[1:]:
                    vals = list(m(v,r[n].value) for m,v,n in zip(mergers, vals, fnames))
                f.write('\t'.join(map(str,vals))+'\n')

        self.t = Orange.data.Table(TMP)
        discard(TMP)

def custom(featdef, idata):
    """ Create custom table !
        featdef : feature info as list(name, d/c, meta/class)
        idata : instances (same order af featdef of course)
        name : optional savefile for custom table
    """
    with open(TMP, 'w') as f:
        # Header
        for k in range(3):
            f.write('\t'.join([t[k] for t in featdef]) + '\n')
        # Instances
        for r in idata:
            f.write('\t'.join(map(str, r)) + '\n')
    
    res = TabData(TMP)
    discard(TMP)
    return res

def discard(fname):
    try:
        os.remove(fname)
    except OSError:
        print('Please remove {0} manually'.format(fname))

