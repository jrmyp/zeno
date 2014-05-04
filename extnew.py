# Testing new feat extractor, yay.
# Python 3

# I'm sensing doom. I fear it's slow.
# But it has to work, or else I'm doomed

# TODO :Convert all to tab format !

import re
import featnew
from itertools import chain
from annodata import Annotations

def to_csv_row(l):
    return ','.join((re.sub(',','COMMA',str(e))
        for e in l)) + '\n'

def fname(n, v, metas):
    if n in metas:
        return 'm#'+n
    try:
        int(v)
        return 'C#'+n
    except ValueError:
        return 'D#'+n
        
pa = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/unannotated/s1-league1-game1_03.aa'
pr = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/unannotated/s1-league1-game1_03.ac'
pp = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/parsed/stanford-corenlp/s1-league1-game1_03.xml'

an = Annotations(pa)
an.load_text(pr)
an.load_parsed(pp)

sl, pl, ml = featnew.pre_features()
fl = pl + [n+'_1' for n in sl] + [n+'_2' for n in sl]

master_gen = chain.from_iterable(featnew.gen_features(anno, 3) for anno in [an])

first_line = next(master_gen)
header = (to_csv_row(fname(n,v,ml) for n,v in zip(fl, first_line)) +
          to_csv_row(first_line))

with open('csv_res.txt', 'w') as f:
    f.write(header)
    for fr in master_gen:
        f.write(to_csv_row(fr))
