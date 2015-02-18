# Testing new feat extractor, yay.
# Python 3

# I'm sensing doom. I fear it's slow.
# But it has to work, or else I'm doomed

# TODO : Sync with classify !
#   Done, but do a switch-a-roo 2/3 for speed ?

import re
#~ import featnew as fg
import fset_t as fg
#~ import classify as cs
import annodata as ad
from itertools import chain, repeat

def custom(featdef, idata, name):
    """ Create custom table !
        featdef : feature info as list(name, d/c, meta/class)
        idata : instances (same order af featdef of course)
        name : savefile for custom table
    """
    with open(name, 'w') as f:
        # Header
        for k in range(3):
            f.write('\t'.join([t[k] for t in featdef]) + '\n')
        # Instances
        for r in idata:
            f.write('\t'.join(map(str, r)) + '\n')    

#~ pa = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/unannotated/s1-league1-game1_03.aa'
pa = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/discourse/SILVER/s1-league1-game1_03.aa'
pr = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/unannotated/s1-league1-game1_03.ac'
pp = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/parsed/stanford-corenlp/s1-league1-game1_03.xml'
fres = '../res/custom.tab'

an = ad.Annotations(pa, 'discourse', 's1-league1-game1_03')
an.load_text(pr)
an.load_parsed(pp)
an.gen_full_struct()

sl, pl, ml, cl = fg.pre_features()

def tri(name, suffix=''):
    return (name+suffix, 
            'c' if name in cl else 'd',
            'meta' if name in ml else '')

t_feat = []
#~ for nl, s in ((pl, ''), (sl, '_1'), (sl, '_2')):
for nl, s in ((pl, ''), (sl, '_DU1'), (sl, '_DU2')):
    for n in nl:
        t_feat.append(tri(n,s))

t_data = chain.from_iterable(fg.gen_features(anno, 3) for anno in [an])

custom(t_feat, t_data, fres)
