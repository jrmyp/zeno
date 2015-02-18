# Report on training

import sys
import os
import annodata as ad
from collections import defaultdict

oracle_nc = 151

sroot = '/home/arthur/These/Master/Stac/data'
seasons = ('pilot', 'socl-season1','socl-season2')
stages = ('GOLD', 'SILVER', 'bronze', 'Bronze', 'BRONZE')

# The great big loop for retrieving all annotations
# Someday, I'll simplify this, there are redundancies...
def g_n():
    # Season loop
    for sname in seasons:
        # Game loop
        for gname in os.listdir(os.path.join(sroot, sname)):
            if gname.startswith(('s1','s2','pilot')):
                p0 = os.path.join(sroot, sname, gname)
                if 'discourse' in os.listdir(p0):
                    p1 = os.path.join(p0, 'discourse')
                    # Stage loop
                    for tname in stages:
                        if tname in os.listdir(p1):
                            p2 = os.path.join(p1, tname)
                            if not os.listdir(p2):
                                continue
                            # Annotation file loop
                            for fname in os.listdir(p2):
                                if fname.endswith('.aa'):
                                    bname = fname[:-3]
                                    a = ad.Annotations(os.path.join(p2, fname))
                                    a.gen_full_struct()
                                    a.load_text(os.path.join(p0, 'unannotated', bname+'.ac'))
                                    #~ a.load_parsed(os.path.join(p0, 'parsed', 'stanford-corenlp', bname+'.xml'))
                                    yield bname, a
                            # Only check first found stage
                            break

all_anno = dict()
for i, pair in enumerate(g_n()):
    n, anno = pair
    all_anno[n] = anno
    print('Loading ({0}/{1}) : {2}\r'.format(i+1, oracle_nc, n), end='')
    sys.stdout.flush()
print('\nAnnotations loaded')
print(set(k.split('_')[0] for k in all_anno.keys()))

rels = defaultdict(list)
with open('../res/pred.tab') as f:
    def sid(e):
        l = e.split('_')
        return tuple('_'.join(pl) for pl in (l[:2], l[3:]))

    for line in f:
        if not line:
            continue
        pr, rr, ui, vi = line[:-1].split('\t')
        if pr == rr:
            continue
        (fn, uid), vid = sid(ui), sid(vi)[1]
        anno = all_anno[fn]
        try:
            ue, ve = (anno.elements[i] for i in (uid, vid))
        except KeyError:
            print('Missing EDU', ui, vi)
            continue
        try:
            rt = next(r for r in ue.inRelation
                if ve in r.args)
        except StopIteration:
            print('Rel not found', ui, vi)
            continue
        
        if rr != rt.type:
            print('Rel mismatch', ui, vi)
            continue
            
        rels[fn].append((pr, rt))
        
def rtext(e):
    if e.type == 'Segment':
        return e.turn.Emitter, e.text
    elif e.type == 'Complex_discourse_unit':
        emits, parts = zip(*list(rtext(arg) for arg in e.args))
        return emits[0], ' '.join(parts)

with open('pred_report.txt', 'w') as f:
    for name, rl in rels.items():
        f.write('== {0} ==\n\n'.format(name))
        for p, r in rl:
            f.write('Reference  : {0}\n'.format(r.type))
            f.write('Prediction : {0}\n'.format(p))
            for e in r.args:
                f.write('> {0} : {1}\n'.format(*rtext(e)))
            f.write('\n')
