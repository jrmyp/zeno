# Stats over annotations
# Double-check,triple-check, etc.

from __future__ import print_function
import sys
import os
import annodata as gd
#~ from codecs import open
from collections import defaultdict

oracle_nc = 93

sroot = '/home/arthur/These/Master/Stac/data'
seasons = ('pilot', 'socl-season1','socl-season2')
#~ seasons = ('socl-season1',)
#~ seasons = ('socl-season1','pilot')
#~ stages = ('SILVER', 'bronze', 'Bronze', 'BRONZE', 'lpetersen', 'hjoseph')
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
                            # Annotation file loop
                            for fname in os.listdir(p2):
                                if fname.endswith('.aa'):
                                    bname = fname[:-3]
                                    a = gd.Annotations(os.path.join(p2, fname))
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

#~ print(sum(len(a.turns) for a in all_anno.values()), 'turns total')
print(set(k.split('_')[0] for k in all_anno.keys()))
 
# Relation count
counts = defaultdict(int)    
for n, anno in all_anno.items():
    for r in anno.relations:
        counts[r.type] += 1
for l, s in sorted(counts.items(), key=lambda x:x[1],reverse=True):
    print('{0:25}: {1}'.format(l, s))
print()

# EDU gap count
#~ counts = defaultdict(int)
#~ scounts = defaultdict(lambda: defaultdict(int))
#~ for n, anno in all_anno.items():
    #~ ls = anno.segments
    #~ def gi(s):
        #~ if s.type == 'Segment':
            #~ return s
        #~ elif s.type == 'Complex_discourse_unit':
            #~ if not s.args:
                #~ print('Anomaly (empty CDU)', n)
            #~ return min((gi(sk) for sk in s.args), key=lambda u:u.startPos)
        #~ else:
            #~ print('Anomaly', s.type, s.oid)
            #~ print(n)
            #~ print(s.text)
    #~ for rel in anno.relations:
        #~ si, sj = rel.args
        #~ gsi, gsj = gi(si), gi(sj)
        #~ dist = abs(ls.index(gsi) - ls.index(gsj))
        #~ if dist == 0 or dist > 50:
            #~ print('Anomaly dist', n)
            #~ print(si.oid, si.text)
            #~ print(sj.oid, sj.text)
        #~ same_em = (gsi.turn.Emitter == gsj.turn.Emitter)
        #~ counts[dist] += 1
        #~ scounts[dist][same_em] += 1
#~ print(dict(counts))
#~ print(sum(counts.values()))
#~ kil = list(scounts.keys())
#~ kjl = [True, False]
#~ print('{0:8}{1:>8}{2:>8}{3:>8}'.format(*([r'']+kjl+['Sum'])))
#~ for ki in kil:
    ## ks = [scounts[ki][kj] for kj in kjl] + [sum(scounts[ki].values())]
    #~ ks = [scounts[ki][kj] for kj in kjl] + [counts[ki]]
    #~ print('{0:8}{1:>8}{2:>8}{3:>8}'.format(*([ki]+ks)))        

# Triplets text-rel-text
rnames = (
    'Question-answer_pair',
    'Comment',
    'Acknowledgement',
    'Continuation',
    'Elaboration',
    'Result',
    'Q-Elab',
    'Contrast',
    'Explanation',
    'Clarification_question',
    'Correction',
    'Parallel',
    'Alternation',
    'Conditional',
    'Narration',
    'Background')

for rn in rnames:
    with open('../lres/lr_{0}.txt'.format(rn), 'w', encoding='utf-8') as f:
        for n, anno in all_anno.items():
            f.write('=== ' + n + ' ===\n')
            for r in anno.relations:
                if r.type != rn:
                    continue
                #~ ##f.write('= '+ r.type + ' =\n')
                for arg in r.args:
                    if arg.type == 'Segment':
                        #~ # f.write(arg.type + ' ' + arg.text+'\n')
                        f.write('{0} : {1}\n'.format(arg.turn.Emitter, arg.text))
                    elif arg.type == 'Complex_discourse_unit':
                        parts = []
                        emit = ''
                        for sarg in arg.args:
                            if sarg.type == 'Segment':
                                emit = sarg.turn.Emitter
                                parts.append(sarg.text)
                        f.write('{0} (CDU): {1}\n'.format(emit, ' '.join(parts)))        
                f.write('\n')
print()
