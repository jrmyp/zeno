""" Harness script for bypass

Shall be destroyed by attelo
"""

# TODO : be able to select classification run (not just latest)
    # Probably by asking in config...
    # Mmmh wait, this is linked to print-probs. Check this

from __future__ import print_function

import os
import config as cfg
import decoding as dcd
import report as rpt
from collections import defaultdict

join = os.path.join

RELS = 'Acknowledgement:Alternation:Background:Clarification_question:Comment:Conditional:Continuation:Contrast:Correction:Elaboration:Explanation:Narration:Parallel:Q-Elab:Question-answer_pair:Result:UNRELATED'.split(':')

for c_name in cfg.classifiers:
    ilp_tgt = join(cfg.out_tgt, 'ilp')
    conll_tgt = join(cfg.out_tgt, 'conll')
    logs_tgt = join(cfg.out_tgt, 'logs')
    if not os.path.isdir(ilp_tgt):
        os.makedirs(ilp_tgt)
    if not os.path.isdir(conll_tgt):
        os.makedirs(conll_tgt)
    if not os.path.isdir(logs_tgt):
        os.makedirs(logs_tgt)

    ref_src = join(cfg.mat_src, c_name, 'ref')
    pred_src = join(cfg.mat_src, c_name, 'pred')
    mst_src = join(cfg.mat_src, c_name, 'mst')
    msdag_src = join(cfg.mat_src, c_name, 'msdag')
    
    dialogues = set()
    for f_name in os.listdir(ref_src):
        dialogues.add(f_name.split('.')[0])

    ldia = len(dialogues)
    dia_count = defaultdict(int)
    scores = defaultdict(list)
    tris = dict()
    for i_dia, dialogue in enumerate(dialogues):
        print('({0:4}/{1:4}) Processing {2:20}\r'.format(
            i_dia+1, ldia, dialogue), end='')
        
        # Skip if ILP decoding is absent
        ilp_src = join(cfg.ilp_src, dialogue+'.output')
        if not os.path.exists(ilp_src):
            # print('ILP unknown : {0}'.format(dialogue))
            continue

        # Reference triplets
        tris['ref'], _ = dcd.mat_to_tri(join(ref_src, dialogue+'.rel.dat'))
        tris['mst'], _ = dcd.mat_to_tri(join(mst_src, dialogue+'.rel.dat'))
        tris['msdag'], _ = dcd.mat_to_tri(join(msdag_src, dialogue+'.rel.dat'))

        # Retrieve ILP decoding results
        d = dcd.Data()
        d.rels, order = dcd.mat_to_map(join(msdag_src, dialogue+'.rel.dat'))
        d.ilp_path = ilp_src
        tris['ilp'] = dcd.d_ilp(d)
        if not tris['ilp']:
            # print('Empty solution {0}'.format(dialogue))
            tris['ilp'] = tris['mst']

        # MST++ decoding
        d.base, _ = dcd.mat_to_map(join(mst_src, dialogue+'.rel.dat'))
        d.full, _ = dcd.mat_to_tsr(join(pred_src, dialogue+'.rel.dat'))
        d.irels = (RELS.index('Question-answer_pair'),
                    RELS.index('Acknowledgement'))
        for xt in [float(s+1)/10 for s in range(1,4)]:
            for xd in [s+1 for s in range(1,4)]:
                label = 'mst++ p{0:.1f} w{1}'.format(xt, xd)
                tris[label] = dcd.d_mst_plus(d, xt, xd)
        
        # ILP triplets
        # with open(join(ilp_tgt, dialogue+'.rel'), 'w') as tgt:
            # for i, j, k in tris['ilp']:
                # print(' '.join((order[i], order[j], RELS[k])), file=tgt)

        # CONLL output (for graphs)
        mout = 'mst++ p0.2 w3'
        game = dialogue.split('_')[0]
        subgame = '_'.join(dialogue.split('_')[:2])
        with open(join(conll_tgt, game+'.conll'), 'a') as tgt:
            tgt.write(rpt.tri_to_conll(tris[mout], dialogue, order, RELS))
        # dia_count[subgame] += 1
        # with open(join(logs_tgt, subgame+'.txt'), 'a') as tgt:
            # tgt.write('Graph n.{0} -- {1} units -- {2}\n'.format(
                # dia_count[subgame], len(d.base), dialogue))
        
        # Baselines
        d.prob, _ = dcd.mat_to_map(join(pred_src, dialogue+'.attach.dat'),
            True, True)
        d.rels, _ = dcd.mat_to_map(join(pred_src, dialogue+'.rel.dat'),
            False, True)
        tris['last'] = dcd.d_last(d)
        tris['local'] = dcd.d_local(d)

        # Remove first unit (fake root)
        if cfg.fakeroot:
            for method in tris:
                oldtri = tris[method]
                tris[method] = list((u,v,r) for u,v,r in oldtri
                    if u>0 and v>0)

        for method, tri in tris.items():
            scores[method].append(rpt.doc_score(tris['ref'], tri))

    print()
    print(rpt.score_line())
    for deco in sorted(scores):
        print(rpt.score_line(scores[deco], deco))
