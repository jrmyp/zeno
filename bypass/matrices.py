"""
Script generator for filling matrices
Usage :
  switch to your virtual environment for STAC
  git checkout the correct branch (jrmyp/attelo/print-probs)
  (only the first time) run irit-stac evaluate
  edit the configuration below !
  run 'python matrices.py'
  run 'sh [launch_script]'
"""
from __future__ import print_function

import sys
from os.path import isfile, join
from functools import partial

### CONFIGURATION
# Script that will actually perform the work
launch_script = 'launch.sh'

# Path to your attelo folder
# attelo_path = 'path/to/attelo'
attelo_path = '~/Master/attelo'

# Path to your STAC folder
# stac_path = 'path/to/stac'
stac_path = '~/Master/Stac'

# Path to your desired output folder
# output_path = 'path/to/output'
output_path = '~/Tests/probs'

# Classifiers
# classifiers = ('bayes', 'maxent')
classifiers = ('maxent',)

# Evaluation stamp
# stamp = 'latest'            # Dangerous
# stamp = '2015-02-10T0856'   # No window, no fakeroot
stamp = '2015-02-26T0251'   # No window, filtered, with fakeroot (booyah)

### END CONFIGURATION

p0 = join(attelo_path, 'scripts', 'attelo')
p1 = join(stac_path, 'code', 'parser', 'stac-features.config')
p2 = join(stac_path, 'TMP', stamp, 'scratch-current')
p3 = join(stac_path, 'TMP', stamp, 'eval-current')

if not isfile('postrel.py'):
    print('ABORT : Please copy postrel.py in this directory')
    sys.exit()

with open(launch_script, 'w') as f:
    # Partial fun for f and space
    s_print = partial(print, end=' ', file=f)
    n_print = partial(print, file=f)

    for classif in classifiers:
        p_out = join(output_path, stamp, classif)
        p_out_ref, p_out_pred, p_out_msdag, p_out_mst = (
            join(p_out, name) for name in
            ('ref', 'pred', 'msdag', 'mst'))
        n_print('mkdir -p {0}'.format(p_out_ref))
        n_print('mkdir -p {0}'.format(p_out_pred))
        n_print('mkdir -p {0}'.format(p_out_msdag))
        n_print('mkdir -p {0}'.format(p_out_mst))
        n_print('echo === Classifier : {0} ==='.format(classif))
        
        for i_fold in range(10):
            n_print('echo == Fold : {0} =='.format(i_fold))
            # s_print('{0} show_probs'.format(p0))
            s_print('attelo show_probs'.format(p0))
            s_print('-C {0}'.format(p1))
            p_amod = join(p2, 'fold-{0}'.format(i_fold),
                'all.{0}.attach.model'.format(classif))
            s_print('-A {0}'.format(p_amod))
            p_rmod = join(p2, 'fold-{0}'.format(i_fold),
                'all.{0}.relate.model'.format(classif))
            s_print('-R {0}'.format(p_rmod))
            s_print('-o {0}'.format(p_out))
            p_fold, p_adata, p_rdata = (join(p3, name) for name in
                ('folds-all.json', 'all.edu-pairs.csv', 'all.relations.csv'))
            s_print('--fold-file {0}'.format(p_fold))
            s_print('--fold {0}'.format(i_fold))
            s_print(p_adata)
            s_print(p_rdata)
            n_print()
            # MSDAG matrices
            s_print('python postrel.py')
            p_prel = join(p2, 'fold-{0}'.format(i_fold),
                'output.{0}-msdag'.format(classif))
            s_print(p_prel)
            s_print(p_out_ref)
            s_print(p_out_msdag)
            n_print()
            # MST matrices
            s_print('python postrel.py')
            p_prel = join(p2, 'fold-{0}'.format(i_fold),
                'output.{0}-mst'.format(classif))
            s_print(p_prel)
            s_print(p_out_ref)
            s_print(p_out_mst)
            n_print('\n')
        
