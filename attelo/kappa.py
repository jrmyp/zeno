# Inter-anno kappa

from __future__ import print_function
import sys
import os
import re

import annodata as ad
#~ import classify as cs
from collections import defaultdict
from codecs import open

sroot = '/home/arthur/These/Master/Stac/data/socl-season1'
names_r = ('clay', 'ore', 'wheat', 'wood', 'sheep')

def get_commitments(s, clist):
    """ Get all commitment resources for a given Segment """
    return dict((c.Resource, (c.Lower_bound, c.Upper_bound))
        for c in clist if (s in c))

def compat(p, q):
    pl, ph = p
    ql, qh = q
    return max(pl, ql) <= min(ph, qh)

def g_n():
    """ Iterates on all files annotated with Commitment
        Yields annotation objects
    """
    for gname in os.listdir(sroot):
        if gname != 's1-league1-game1':
            continue
        if gname.startswith('s1'):
            p0 = os.path.join(sroot, gname)
            p1 = os.path.join(p0, 'commitment', 'jperret')
            p2 = os.path.join(p0, 'commitment', 'sa')
            if os.path.isdir(p1) and os.path.isdir(p2):
                for fname in os.listdir(p1):
                    if fname.endswith('.aa'):
                        bname = fname[:-3]
                        #~ if bname == 's1-league1-game2_07':
                            #~ continue
                        a = ad.Annotations(os.path.join(p1, fname))
                        a.load_text(os.path.join(p0, 'unannotated', bname+'.ac'))
                        a.gen_full_struct()
                        a.commitments = list(u for u in a.units if u.type == 'Commitment')
                        a2 = ad.Annotations(os.path.join(p2, fname))
                        a2.load_text(os.path.join(p0, 'unannotated', bname+'.ac'))
                        a2.gen_full_struct()
                        a2.commitments = list(u for u in a2.units if u.type == 'Commitment')
                        yield bname, (a, a2)

all_anno = dict(g_n())
print(set(k.split('_')[0] for k in all_anno))

tot_ok = 0
tot_in = 0
tot_all = 0
tot_zer = 0

for n, pair in all_anno.items():
    nn = n
    ai, aj = pair
    #~ print(get_commitments(ai.commitments[0], ai.commitments))
    #~ print(get_commitments(aj.commitments[0], aj.commitments))
    #~ break
    for ti in ai.turns:
        try:
            tj = aj.elements[ti.id]
        except KeyError:
            print('This is madness !')
            continue
        ci = get_commitments(ti, ai.commitments)
        cj = get_commitments(tj, aj.commitments)
        
        tot_all += 1
        
        if not ci and not cj :
            # Both empty
            tot_zer += 1
            continue

        perfect = True
        for n in names_r:
            if (n in ci) != (n in cj):
                # Resource mismatch : fail
                break
            if (n in ci) and (n in cj):
                if ci[n] == cj[n]:
                    # Perfect match, go on
                    pass
                elif compat(ci[n], cj[n]):
                    perfect = False
                else:
                    # Quantity mismatch : fail
                    print(n, ci[n], cj[n])
                    break                
        else:
            # No break : agreement
            tot_in += 1
            if perfect:
                tot_ok += 1


    
print(tot_ok, tot_in, tot_zer, tot_all)
print('Agree harsh : {0}'.format(float(tot_ok+tot_zer)/tot_all))
print('Agree nice : {0}'.format(float(tot_in+tot_zer)/tot_all))
print()
print(sum(len(a[0].turns) for a in all_anno.values()))
