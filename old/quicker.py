# Quicker script with already-built data !

from __future__ import print_function
import sys
import os
import annodata as ad
import classify as cs
from collections import defaultdict

fcomm = '/home/arthur/These/Data/socl-season1.custom-edus.tab'
fmerge = '/home/arthur/These/Data/socl-season1.merged.tab'
fturns = '/home/arthur/These/Data/socl-season1.turns2.tab'
fqap = '/home/arthur/These/Data/socl-season1.qap.tab'
ffinal = '/home/arthur/These/Data/socl-season1.final.tab'

c_t = cs.TabData(fmerge)
pc_t = cs.TabData(fqap)
c_t.merge(pc_t)
c_t.fuse_rows('turn_id')
c_t.save(ffinal)

print(len(set(row['is_commitment'].value == 'True' for row in c_t)))
#~ sys.exit()

#~ ddd = defaultdict(list)
#~ for row in c_t:
    #~ ddd[row['dialogue'].value].append(row['turn_id'].value)
#~ count = defaultdict(int)
#~ for k,v in ddd.items():
    #~ count[len(v)] += 1
    #~ 
#~ print(count)
#~ sys.exit()

#~ s = set(r['turn_id'].value for r in c_t)
#~ print(len(s))
#~ sys.exit()    

c_t = cs.TabData(ffinal)
c_t.new_class('is_commitment')

# Standard training
end_c = cs.Trainer(c_t, 10, 'dialogue')
end_c.evaluate()

# Baseline training
#~ end_c = cs.Trainer(c_t, 10, 'dialogue', baseline=True)
#~ end_c.evaluate()

# Training for various classes
#~ tcl = ['is_commitment', 'is_ore_c', 'is_wheat_c', 'is_clay_c', 'is_wood_c', 'is_sheep_c']
#~ tcl = ['is_commitment']
#~ for tc in tcl:
    #~ c_t = cs.TabData(ffinal)
    #~ c_t.new_class(tc)
    #~ 
    #~ print(c_t.t.domain.class_var.name)
    #~ end_c = cs.Trainer(c_t, 10, 'dialogue', learner='logreg')
    #~ s = end_c.evaluate()

# Multi-training
#~ scores = list()
#~ for k in range(10):
    #~ #~# end_c = cs.Trainer(c_t, 10, 'dialogue', learner='logreg')
    #~ end_c = cs.Trainer(c_t, 10, 'dialogue')
    #~ s = end_c.evaluate(quiet=True)
    #~ scores.append(s['True'])
    #~ print('{0:.3}'.format(s['True']))
    #~ 
#~ print('Mean :')
#~ print('{0:.3}'.format(sum(scores)/10))
