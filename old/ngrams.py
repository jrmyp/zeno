# Stats for n-grams
# This is a mess

import os
import annodata as gd
from itertools import chain
from collections import Counter

sroot = '/home/arthur/These/Master/Stac/data'
seasons = ('socl-season1','socl-season2','pilot')
#~ seasons = ('socl-season1','pilot')

g_a = (os.path.join(sroot, sname, name)
        for sname in seasons
        for name in os.listdir(os.path.join(sroot, sname))
        if name.startswith(('s1','s2','pilot')))
        
g_aa = (os.path.join(name, 'parsed','stanford-corenlp')
        for name in g_a
        if 'parsed' in os.listdir(name))

g_b = (os.path.join(src, name)
        for src in g_aa 
        for name in os.listdir(src)
            if name.endswith('.xml')
      )

gg = sorted(list(g_b))
lg = len(gg)    
win = 3
dem = Counter()
for i, name in enumerate(gg):
    print('\r{0}/{1}'.format(i+1, lg), end='')
    pt = gd.ParsedText(name)
    
    for s in pt.sentences():
        ll = [t[1].lower() for t in s if t[1] not in {',','.'}]
        if len(ll) < win:
            #~ continue
            ll = ['']*(win-len(ll))+ll+['']*(win-len(ll))
        else:
            dem[tuple(ll[:win])] += 1
        dem[tuple(ll[-win:])] += 1

print()
for t, v in dem.most_common(50):
    print(v, *t)
