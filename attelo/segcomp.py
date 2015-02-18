# Segmentation comparator

import annodata as ad

pa = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/unannotated/s1-league1-game1_03.aa'
pb = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/discourse/SILVER/s1-league1-game1_03.aa'
pr = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/unannotated/s1-league1-game1_03.ac'

aa = ad.Annotations(pa)
aa.load_text(pr)
aa.gen_full_struct()
ab = ad.Annotations(pb)
ab.load_text(pr)
ab.gen_full_struct()

sa, sb = (set(s.id for s in an.segments) for an in (aa, ab))
print(sa-sb)
print(sb-sa)
