# Merging custom and attelo sources
# For great justice

# Python 2

import classify as cs

fcustom = '../res/custom.tab'
fmerge = '../res/merge.tab'
frel = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-06-04/socl-season1.relations.csv'

t_c, t_r = (cs.TabData(f) for f in (fcustom, frel))
t_c.newmerge(t_r, ('id_DU1','id_DU2'))
t_c.save(fmerge)
