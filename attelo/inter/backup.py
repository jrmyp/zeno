# Backup script for annotations

import sys
import os

bpath = sys.argv[1]
opath, rpath = (os.path.join(bpath, k) for k in ('jperret_2', 'backup'))
#~ opath, rpath = (os.path.join(bpath, k) for k in ('backup', 'jperret_2'))
if not os.path.exists(rpath):
    os.mkdir(rpath)

for af in os.listdir(opath):
    if not af.endswith('.aa'):
        continue
    with open(os.path.join(opath, af)) as f:
        ct = f.read()
    with open(os.path.join(rpath, af), 'w') as f:
        f.write(ct)

