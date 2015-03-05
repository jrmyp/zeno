""" Configuration for bypass """

# CSV data folder
# As targeted by irit-stac gather
tab_src = '/home/perret/Master/Stac/TMP/2015-02-10T0856/eval-2015-02-10T0905'

# CSV rewriting destination
tab_tgt = '/home/perret/Data/csv'

# Folder with all matrices
# As created by matrices.py
# mat_src = '/home/perret/Tests/probs/2015-02-10T0856'  # No win no fake
mat_src = '/home/perret/Tests/probs/2015-02-26T0251'  # Filtered fake

# Folder with SCIP result files
ilp_src = '/home/perret/Data/ilp'

# Output folder
out_tgt = '/home/perret/Tests/report'

# Stac path
stac_path = '/home/perret/Master/Stac'

# classifiers = ('bayes', 'maxent')
classifiers = ('maxent',)

# Fakeroot usage
# fakeroot = False
fakeroot = True
