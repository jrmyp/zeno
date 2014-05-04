# Wrapping classification operations
# Cleaner scripting is needed

from __future__ import print_function
import os
import random
import Orange
import valmerger
from collections import defaultdict

class Trainer:
    """ Everything you want for your training needs """
    
    def __init__(self, data, n_folds, grouper=None):
        """ Class initialiser """
        self.data = dtable
        self.n_folds = n_folds
        self.grouper = grouper
        
        if grouper is None:
            lf = list(i%n_folds for i in range(len(dtable)))
            random.shuffle(lf)
            self.line_folds = lf
        else:
            # Index of grouper attribute
            #~ gi = dtable.domain.index(grouper)
            # List of group names
            gnames = list(set(line[grouper].value for line in dtable))
            # Generate random fold numbers (equally distributed among groups)
            f_inds = list(i%n_folds for i in range(len(gnames)))
            random.shuffle(f_inds)
            # Dict : group name -> fold number
            g_folds = dict(zip(gnames, f_inds))
            # List of fold numbers (parallel to d_source)
            self.line_folds = list(g_folds[line[grouper].value] for line in dtable)

        learner = Orange.classification.svm.LinearSVMLearner()
        self.classifiers = dict()
        for i_fold in range(n_folds):
            print('Training fold {0}/{1}...\r'.format(i_fold+1, n_folds), end='')
            sys.stdout.flush() 
            d_train = d_source.select_ref(line_folds, i_fold, negate=True)
            self.classifiers[i_fold] = learner(d_train)
            

class TabData:
    """ Wrapper for Orange.data.Table """
    
    def __init__(self, dsource, copy=False):
        """ Class initialiser """
        if copy:
            self.t = dsource.t
        else:
            self.t = Orange.data.Table(dsource)

    def sel_row(self, *a, **ka):
        """ Filter rows Orange-style """
        self.t = self.t.filter(*a, **ka)
    
    def sel_row_by(self, fun):
        """ Filter rows by function """
        self.t = self.t.select(map(fun, self.t))
        
    def sel_col(self, atts, metas=[], new_class=None):
        """ Filter columns
            atts : attributes (including class) to keep
            metas : meta attributes to keep
            new_class : class name for the new domain
        """
        d = self.t.domain
        nd = Orange.data.Domain(atts, d)
        if new_class is not None:
            nd = Orange.data.Domain(nd, new_class)
        for nmeta in metas:
            nd.add_meta(d.meta_id(nmeta), d.get_meta(nmeta))
        self.t = Orange.data.Table(nd, self.t)

    def merge(self, other, id='id'):
        """ Merge with another table
            other : the other table
            id : row identifier attribute name
            returns lists of non-common ids
        """
        si, ti = (set(r[id].value for r in obj.t) for obj in (self, other))
        sx, tx = list(si-ti), list(ti-si)
        st = self.t.filter_ref({id:sx}, negate=1)
        tt = other.t.filter_ref({id:tx}, negate=1)
        #~ st.save('d1.tab')
        #~ tt.save('d2.tab')
        self.t = Orange.data.Table([st,tt])
        return sx, tx
    
    def tab_header(self):
        """ Create Orange tab header and feature name list """
        def tri(f, tag):
            return (f.name, str(f.var_type)[0].lower(), tag)
        
        d = self.t.domain
        # ff : list of (name, c/d, meta/class/'')
        ff = ([tri(d.class_var, 'class')] +
              [tri(f, 'meta') for f in d.get_metas().values()] +
              [tri(f, '') for f in d.attributes])
        # Header, on 3 lines (Orange tab format)
        h = ''
        for k in range(3):
            h += '\t'.join([t[k] for t in ff]) + '\n'
        # Feature name list, in order
        fl = list(t[0] for t in ff)
        return h, fl

    def fuse_rows(self, grouper, sorter, name=None):
        """ Merge groups of rows
            Return the fused table !
            grouper : row grouping attribute
            sorter : positioning attribute
        """
        tmp = name or 'tmp.tab'
        head, fnames = gen_tab_header(self.t)
        mergers = valmerger.gen_vm(fnames)

        groups = defaultdict(list)
        for r in self.t:
            groups[r[grouper].value].append(r)

        with open(tmp, 'w') as f:
            f.write(head)
            for rl in groups.values():
                # Sort turn rows by position
                rlis = sorted(rl, key=lambda x:x[sorter].value)
                # Collect and apply mergers
                vals = [rlis[0][n].value for n in fnames]
                for r in rlis[1:]:
                    vals = list(m(v,r[n].value) for m,v,i in zip(mergers, vals, fnames))
                f.write('\t'.join(map(str,vals))+'\n')

        return tmpload(tmp, name is None)

def custom(featdef, idata, name=None):
    """ Create custom table ! """
    tmp = name or 'tmp.tab'
    with open(tmp, 'w') as f:
        # Header
        for k in range(3):
            f.write('\t'.join([t[k] for t in featdef]) + '\n')
        # Instances
        for r in idata:
            f.write('\t'.join(map(str, r)) + '\n')
    
    return tmpload(tmp, name is None)

def tmpload(fname, keep=False):
    tab = TabData(fname)
    if not keep:
        try:
            os.remove(fname)
        except OSError:
            print('Please remove {0} manually'.format(fname))

    return tab

