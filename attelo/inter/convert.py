# Converter from jperret_2 to jperret
# Search and replace, really

import sys
import os
import re

bpath = sys.argv[1]
opath, rpath = (os.path.join(bpath, k) for k in ('jperret_2', 'jperret'))
#~ opath, rpath = (os.path.join(bpath, k) for k in ('jperret', 'jperret_2'))
if not os.path.exists(rpath):
    os.mkdir(rpath)

for af in os.listdir(opath):
    if not af.endswith('.aa'):
        continue
    with open(os.path.join(opath, af)) as f:
        ct = f.read()
    cr = re.sub('jperret_2', 'jperret', ct)
    #~ cr = re.sub('jperret', 'jperret_2', ct)
    with open(os.path.join(rpath, af), 'w') as f:
        f.write(cr)

