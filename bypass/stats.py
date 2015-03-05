""" Very quick, very dirty """

from __future__ import print_function

import re
from os.path import join
from collections import defaultdict

import config as cfg

corpus = 'all'
att_tgt_path = join(cfg.tab_tgt, corpus+'.edu-pairs.csv')

# Header info
with open(att_tgt_path) as f:
    itf = iter(f)
    header, first = next(itf), next(itf)

s_header, s_first = (line.rstrip().split(',')
    for line in (header, first))
names = [tag.split('#')[1] for tag in s_header]
useful = tuple(names.index(n) for n in (
    'dialogue', 'id_DU1', 'CLASS', 'num_tokens_DU1'))

def parse(line):
    if not line:
        return (None, None)
    vals = line.rstrip().split(',')
    return tuple(vals[i] for i in useful)

games = set()
dialogues = set()
wordcount = dict()
npairs = 0
nrels = 0 
with open(att_tgt_path) as f:
    itf = iter(f)
    next(itf)
    for line in itf:
        d = parse(line)
        games.add(d[0].split('_')[0])
        dialogues.add(d[0])
        if not d[1].startswith('ROOT'):
            wordcount[d[1]] = int(d[3])
            npairs += 1
            if d[2]=='True':
                nrels += 1

print('Games', len(games))
print('Dias', len(dialogues))
print('EDUs', len(wordcount))
print('Words', sum(wordcount.values()))
print('Pairs', npairs)
print('Atta', nrels)

"""
Games 36
Dias 1027
EDUs 9888
Words 40829
Pairs 109848
Atta 10181
"""
