""" Table management and filtering

I mean, this is all very ad hoc"""

# WARNING : source tables MUST have backward links (else, problems)
# WARNING : features must be in order :
#   CLASS, dialogue, (pair), id_1, (single_1), id_2, (single_2)

from __future__ import print_function

import re
from os.path import join
from itertools import izip
from collections import defaultdict

import config as cfg

corpus = 'all'
att_src_path = join(cfg.tab_src, corpus+'.edu-pairs.csv')
rel_src_path = join(cfg.tab_src, corpus+'.relations.csv')
att_tgt_path = join(cfg.tab_tgt, corpus+'.edu-pairs.csv')
rel_tgt_path = join(cfg.tab_tgt, corpus+'.relations.csv')

# Header info
with open(att_src_path) as f:
    itf = iter(f)
    header, first = next(itf), next(itf)

s_header, s_first = (line.rstrip().split(',')
    for line in (header, first))
names = [tag.split('#')[1] for tag in s_header]
useful = tuple(names.index(n) for n in (
    'dialogue', 'id_DU1', 'id_DU2', 'CLASS', 'same_speaker', 'start_DU1'))
placeholder = []
for name, val in zip(names, s_first):
    if not name.endswith('DU2'):
        if name == 'dialogue':
            pval = val
        elif val in ('True', 'False'):
            pval = 'False'
        elif re.match('\d+', val):
            pval = '0'
        else:
            pval = '__root__'
        placeholder.append(pval)
placeholder = placeholder[2:]

def fakegen(val, idia, lsrc):
    larr = lsrc.rstrip().split(',')
    larr[2:useful[2]] = placeholder
    larr[0] = val
    larr[useful[1]] = idia
    return ','.join(larr)+'\n'

def parse(line):
    if not line:
        return (None, None)
    vals = line.rstrip().split(',')
    return tuple(vals[i] for i in useful)

def process(a_s, r_s, a_t, r_t):
    def dproc(data):
        starts = dict()
        same = dict()
        receivers = set()
        # First pass : collect data
        for (_, uid, vid, att, same_s, usta), _, _ in data:
            starts[uid] = int(usta)
            same[(uid, vid)] = (same_s == 'True')
            if att == 'True':
                receivers.add(vid)
        order = sorted(starts.keys(), key=lambda k:starts[k])
        orderd = dict((u, i) for i, u in enumerate(order))
        # print(len(order), order)
        # Contiguous units with same speaker
        contig, cont_i = dict(), 0
        contig[order[0]] = cont_i
        for i in range(1, len(order)):
            if not same[(order[i-1], order[i])]:
                cont_i += 1
            contig[order[i]] = cont_i
        # print(len(contig), contig)
        # Fake root - Units with no incoming links
        ifake = 'ROOT_'+data[0][0][0]
        fakeleft = set(starts.keys())

        # Second pass : write data
        for (_, uid, vid, _, _, _), line, rline in data:
            if uid in fakeleft:
                is_root = str(uid not in receivers)
                a_t.write(fakegen(is_root, ifake, line))
                r_t.write(fakegen('UNRELATED', ifake, line))
                fakeleft.remove(uid)
            if orderd[uid] > orderd[vid] and contig[uid] != contig[vid]:
                # Skip if backwards and not in same speaker block
                continue
            a_t.write(line)
            r_t.write(rline)
        
    i_s = izip(a_s, r_s)
    next(i_s)
    cdia = None
    cdata = []
    for line, rline in i_s:
        ldata = parse(line)
        # print(ldata)
        if ldata[0] != cdia:
            # New dialogue, process previous
            if cdia is not None:
                dproc(cdata)
            cdata = []
            cdia = ldata[0]
            if ldata[1] is None:
                # EOF
                break
        cdata.append((ldata, line, rline))
        # print(cdia, end='')
        # raw_input()
        
with open(att_src_path) as att_src:
    with open(rel_src_path) as rel_src:
        with open(att_tgt_path, 'w') as att_tgt:
            with open(rel_tgt_path, 'w') as rel_tgt:
                att_tgt.write(header)
                rel_tgt.write(header)
                process(att_src, rel_src, att_tgt, rel_tgt)
