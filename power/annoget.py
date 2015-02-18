# Annotation retriever
# Home of the great big loop

# Todo : arguments, of course

from __future__ import print_function
import sys
import os
import annodata as ad

sroot = '/home/arthur/These/Master/Stac/data'
seasons = ('socl-season1', 'socl-season2', 'pilot')
#~ seasons = ('socl-season1',)
stages = ('GOLD', 'SILVER', 'bronze', 'Bronze', 'BRONZE')
# stages = ('GOLD',)

# GOLD and almost-GOLD games
custom = {'pilot01'}
xcustom = {
    'pilot01',
    'pilot02',
    'pilot03',
    'pilot04',
    's1-league1-game1',
    's1-league1-game2',
    's1-league1-game3',
    's1-league1-game5',
    's1-league2-game1',
    's1-league2-game3'}

full_s = True

# The great big loop for retrieving all annotations
# Someday, I'll simplify this, there are redundancies...
def g_n():
    # Season loop
    for sname in seasons:
        # Game loop
        for gname in os.listdir(os.path.join(sroot, sname)):
            # if gname.startswith(('s1','s2','pilot')):
            if gname in custom:
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
                                    a = ad.Annotations(os.path.join(p2, fname), bname)
                                    if full_s:
                                        a.gen_full_struct()
                                    else:
                                        a.gen_struct()
                                    a.load_text(os.path.join(p0, 'unannotated', bname+'.ac'))
                                    yield bname, a
                            # Only check first found stage
                            break

def gather(fs=True):
    global full_s
    full_s = fs
    all_anno = dict()
    for i, pair in enumerate(g_n()):
        n, anno = pair
        all_anno[n] = anno
        print('Loading ({0}/{1}) : {2:<30}\r'.format(i+1, '???', n), end='')
        #~ sys.stdout.flush()
        #~ break
    print('\nAnnotations loaded')
    return all_anno

