# Report, more stats...

from __future__ import print_function
import sys
import os
import annodata as ad
import classify as cs
from collections import defaultdict

sroot = '/home/arthur/These/Master/Stac/data/socl-season1'
ffinal = '/home/arthur/These/Data/socl-season1.final.tab'
oracle_nc = 62

#### Load annotations
def g_n():
    """ Iterates on all files annotated with Commitment
        Yields annotation objects
    """
    for gname in os.listdir(sroot):
        if gname.startswith('s1'):
            p0 = os.path.join(sroot, gname)
            p1 = os.path.join(p0, 'commitment', 'jperret')
            if os.path.isdir(p1):
                for fname in os.listdir(p1):
                    if fname.endswith('.aa'):
                        bname = fname[:-3]
                        #~ if bname == 's1-league1-game2_07':
                            #~ continue
                        a = ad.Annotations(os.path.join(p1, fname))
                        a.load_text(os.path.join(p0, 'unannotated', bname+'.ac'))
                        a.gen_struct()
                        yield bname, a

# Without counter
#~ all_anno = dict(g_n())

# With counter
all_anno = dict()
for i, pair in enumerate(g_n()):
    n, anno = pair
    all_anno[n] = anno
    print('Loading ({0}/{1}) : {2}\r'.format(i+1, oracle_nc, n), end='')
    sys.stdout.flush()
print('\nAnnotations loaded')

#~ for a in all_anno.values():
    #~ print(len(a.units))
    #~ print(len(set(u.id for u in a.units if u.type=='Commitment')))

#~ sys.exit()

### Train on data !
c_t = cs.TabData(ffinal)
c_t.new_class('is_commitment')
#~ end_c = cs.Trainer(c_t, 10, 'dialogue', learner='logreg')
end_c = cs.Trainer(c_t, 10, 'dialogue')
end_c.evaluate()

### Create reports...
fnl, fpl = [], []
for pred, row in end_c.pred_rows():
    # False negative case
    if pred.value == 'False' and row.getclass().value == 'True':
        fnl.append(row)
    # False positive case
    if pred.value == 'True' and row.getclass().value == 'False':
        fpl.append(row)

# Display list of instances
def rep(rlis):
    d = defaultdict(list)
    for r in rlis:
        # Turn id == game name + anno turn id
        l = r['turn_id'].value.split('_')
        gn, ti = ('_'.join(pl) for pl in (l[:2], l[2:]))
        try:
            d[gn].append(all_anno[gn].elements[ti])
        except KeyError:
            print(gn, ti)
    ds = sorted(((k,v) for k,v in d.items()), key=lambda x:x[0])
    res = ''
    for n, lis in ds:
        res += '== {0} ==\n'.format(n)
        for t in sorted(lis, key=lambda u:u.startPos):
            res += t.text + '\n'
        res += '\n'
    return res

with open('res/false_pos.txt', 'w') as fp:
    fp.write(rep(fpl))

with open('res/false_neg.txt', 'w') as fn:
    fn.write(rep(fnl))


