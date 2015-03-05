""" ILP handler/parser """

import re

def parse_pairs(fn):
    r = re.compile('x#(\d+)#(\d+)')
    pairs = []
    t_flag = False
    with open(fn) as f:
        for line in f:
            if line.startswith('objective value'):
                # Start of triplets
                t_flag = True
                continue
            if not t_flag:
                # Not reached triplets yet
                continue
            m = r.match(line)
            if not m:
                # End of triplets
                break
            si, sj = m.groups()
            pairs.append((int(si)-1, int(sj)-1))
    return pairs
