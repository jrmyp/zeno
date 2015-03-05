# Stats over annotations
# Double-check,triple-check, etc.

import os
import annodata as gd
from collections import defaultdict

sroot = '/home/arthur/These/Master/Stac/data'
seasons = ('socl-season1','socl-season2','pilot')
#~ seasons = ('socl-season1',)
#~ stages = ('SILVER', 'bronze', 'Bronze', 'BRONZE', 'lpetersen', 'hjoseph')
stages = ('SILVER', 'bronze', 'Bronze', 'BRONZE')
#~ seasons = ('socl-season1','pilot')

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
                                    a.gen_turns()
                                    a.load_text(os.path.join(p0, 'unannotated', bname+'.ac'))
                                    a.load_parsed(os.path.join(p0, 'parsed', 'stanford-corenlp', bname+'.xml'))
                                    yield bname, a
                            # Only check first found stage
                            break

# Relation count
counts = defaultdict(lambda : 0)    
for i, pair in enumerate(g_n()):
    n, anno = pair
    print("Annotation file {0}\r".format(i+1), end='')
    for r in anno.relations:
        counts[r.type] += 1
print()
print(sum(counts.values()))
for l, s in sorted(counts.items(), key=lambda x:x[1],reverse=True):
    print('{0:25}: {1}'.format(l, s))

#~ counts = defaultdict(lambda : 0)    
#~ with open('relres.txt', 'w', encoding='utf-8') as f:
    #~ for i, pair in enumerate(g_n()):
        #~ n, anno = pair
        #~ print("Annotation file {0}\r".format(i+1), end='')
        #~ f.write('=== ' + n + ' ===\n')
        #~ for r in anno.relations:
            #~ f.write('= '+ r.type + ' =\n')
            #~ for arg in r.args:
                #~ if arg.type == 'Segment':
                    #~ f.write(arg.type + ' ' + arg.text+'\n')
                    #~ f.write('{0} : {1}\n'.format(arg.turn.Emitter, arg.text))
                #~ elif arg.type == 'Complex_discourse_unit':
                    #~ parts = []
                    #~ emit = ''
                    #~ for sarg in arg.args:
                        #~ if sarg.type == 'Segment':
                            #~ emit = sarg.turn.Emitter
                            #~ parts.append(sarg.text)
                    #~ f.write('{0} (CDU): {1}\n'.format(emit, ' '.join(parts)))        
            #~ f.write('\n')
#~ print()
