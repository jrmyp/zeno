# Annotation evaluation for Attelo data
# Reminder : keep it clean !

# If only I could retrieve triplets
# I would be so happy

import sys
import os
import re
#~ import argparse as ap
import glozzdata as gd
from collections import defaultdict

fullcounts = defaultdict(lambda : defaultdict(lambda : 0))

# candidate : list of (id, id, relation)
# reference : list of (id, id, relation)
def challenge(candidate, reference, counts):
    # Prepare data !
    dR = defaultdict(lambda : defaultdict(lambda : 'UNRELATED'))
    sR = set()
    for i,j,r in reference:
        ii, jj = sorted((i,j))
        dR[ii][jj] = r
        if r != 'UNRELATED':
            # Gather pairs
            sR.add((ii,jj))
    
    for i,j,r in candidate:
        ii, jj = sorted((i,j))
        if r != 'UNRELATED' and (ii,jj) in sR:
            # Confirm : pair seen in candidate
            sR.remove((ii,jj))
            # Store ref-rel & cdt-rel
            counts[dR[ii][jj]][r] += 1
            
    # Left in sR are pairs in reference but not in candidate
    for i,j in sR:
        counts[dR[i][j]]['UNRELATED'] += 1
        
    return counts

# anno : gd.Annotations
def anno_to_triplets(anno):
    return list((r.links[0].id, r.links[1].id, r.type)
                for r in anno.relations))
