""" Visualize outputs... """

from __future__ import print_function

import os
from os.path import join

import config as cfg

conll_src = join(cfg.out_tgt, 'conll')
ptg_path = join(cfg.stac_path, 'code', 'parser', 'parse-to-glozz')

def expfold(name):
    if name.startswith('pilot'):
        return 'pilot'
    elif name.startswith('s1'):
        return 'socl-season1'
    else:
        return 'socl-season2'

ln_done = set()
with open('visu.sh', 'w') as f:
    nb_parts = len(os.listdir(conll_src))
    for i, name in enumerate(sorted(os.listdir(conll_src))):
        if i >= 1:
            break

        print('echo \({0:3}/{1:3}\) Processing {2}'.format(
            i+1, nb_parts, name), file=f)
        subgame, _ = name.split('.')
        game = subgame.split('_')[0]
        s_unan_path = join(cfg.stac_path, 'data', expfold(game), game, 'unannotated')
        c_anno_path = join(cfg.out_tgt, 'data', game)
        c_disc_path = join(c_anno_path, 'discourse', 'jperret')        
        print('mkdir -p {0}'.format(c_disc_path), file=f)
        print(' '.join((
            ptg_path,
            s_unan_path,     
            join(conll_src, name),
            c_disc_path)), file=f)
        if s_unan_path not in ln_done:
            print(' '.join((
                'ln -s',
                s_unan_path,
                join(c_anno_path, 'unannotated'))), file=f)
        ln_done.add(s_unan_path)
    graph_tgt = join(cfg.out_tgt, 'graph')
    print('\nmkdir -p {0}'.format(graph_tgt), file=f)
    print(' '.join(('stac-util graph',
        join(cfg.out_tgt, 'data'),
        '--output {0}'.format(graph_tgt))), file=f)
