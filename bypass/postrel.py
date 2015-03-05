# Post-processing of rel files to create result matrices

from __future__ import print_function

import sys
import os
import re
from functools import partial
from collections import defaultdict

RELS = ('Acknowledgement', 'Alternation', 'Background',
'Clarification_question', 'Comment', 'Conditional', 'Continuation', 'Contrast',
'Correction', 'Elaboration', 'Explanation', 'Narration', 'Parallel', 'Q-Elab',
'Question-answer_pair', 'Result')

src_dir, ref_dir, out_dir = sys.argv[1:4]
# src_dir contains rel files (post-decoding)
# ref_dir contains dat files (attachment mats)
# out_dir receives dat files (decoding mats)

# WARNING : copied from attelo/cmd/show_probs
def _write_attach_probs(dir_path, prefix, doc_name, probs, order):
    """ Create probability table for attachment"""
    sform = '{0:.2f}' if prefix == 'pred' else '{0}'
    filename = os.path.join(dir_path, prefix,
                        '{0}.attach.dat'.format(doc_name))
    with open(filename, 'w') as f:
        print(':'.join(order), file=f)
        for u in order:
            print(':'.join(sform.format(probs[u][v])
                for v in order), file=f)

# WARNING : copied from attelo/cmd/show_probs
def _write_rel_probs(dir_path, prefix, doc_name, probs, order):
    """ Create probability table for relations """
    sform = '{0:.2f}' if prefix == 'pred' else '{0}'
    filename = os.path.join(dir_path, prefix,
                        '{0}.rel.dat'.format(doc_name))
    with open(filename, 'w') as f:
        print(' '.join(order), file=f)
        print(':'.join(RELS), file=f)
        for u in order:
            print(' '.join(
                    ':'.join(sform.format(probs[u][v][r])
                        for r in RELS)
                    for v in order), file=f)

for fname in os.listdir(src_dir):
    if not fname.endswith('rel'):
        continue
    dname = fname[:-4]
    rpath = os.path.join(ref_dir, dname+'.attach.dat')
    if not os.path.isfile(rpath):
        print('Warning : {0} not found'.format(dname))
        sys.exit()
    with open(rpath) as f:
        line = next(f)
    order = re.split(':', line[:-1])
    tab_attach = defaultdict(lambda:defaultdict(int))
    tab_rel = defaultdict(lambda:defaultdict(lambda:defaultdict(int)))
    fpath = os.path.join(src_dir, fname)
    with open(fpath) as f:
        for line in f:
            r, u, v = re.match('(\S+) \( (\S+) \/ (\S+) \)', line).groups()
            tab_attach[u][v] = 1
            tab_rel[u][v][r] = 1

    _write_attach_probs(out_dir, '', dname, tab_attach, order)
    _write_rel_probs(out_dir, '', dname, tab_rel, order)
