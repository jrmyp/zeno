# Quick random baseline for paper

from __future__ import print_function
import sys
import os
import re
import random

import annodata as ad
from collections import defaultdict

sroot = '/home/arthur/These/Master/Stac/data/socl-season1'
oracle_nc = 62

def get_commitments(s, clist):
    """ Get all commitment resources for a given Segment """
    return dict((c.Resource, (c.Lower_bound, c.Upper_bound))
        for c in clist if (s in c))

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
                        a.gen_full_struct()
                        a.commitments = list(u for u in a.units if u.type == 'Commitment')
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

c = 0
ct = 0
cr = defaultdict(int)
tr = []
ci = defaultdict(int)
ti = []
tmag = []
for a in all_anno.values():
    c += len(a.turns)
    for t in a.turns:
        cm = get_commitments(t, a.commitments)
        if cm:
            ct += 1
            tmag.append(len(cm))
            for k,v in cm.items():
                cr[k] += 1
                tr.append(k)
                ci[v] += 1
                ti.append(v)

print(c, ct)
print(cr)
print(ci)
print('===')

cid = 0
xr = xi = xc = 0
for tm in tmag:
    r = set(tr[cid:cid+tm])
    i = set(ti[cid:cid+tm])
    rtm = random.choice(tmag)
    rr = set(random.choice(tr) for k in range(rtm))
    ri = set(random.choice(ti) for k in range(rtm))
    xr += int(r == rr)
    xi += int(i == ri)
    xc += int(i == ri and r == rr)
    cid += tm

#~ for r, i in zip(tr, ti):
    #~ rr = random.choice(tr)
    #~ ri = random.choice(ti)
    #~ xr += int(r == rr)
    #~ xi += int(i == ri)
    #~ xc += int(i == ri and r == rr)

print(len(tmag), xr, xi, xc)
