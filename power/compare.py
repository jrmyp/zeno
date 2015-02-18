# Stats on annotations (again)

# TODO
# Plot all ranks. Constant is weird.
# META : Spot annotation errors (Turn-Segment relations !)

from __future__ import print_function
import sys
import re
import annoget
#~ import matplotlib.pyplot as plt
from collections import defaultdict

fpairs = '/home/arthur/These/Master/Stac/TMP/latest/socl-season1.edu-pairs.csv'
annos = annoget.gather()

# Sanity-check (relations between other than Segment/CDU)
#~ valid = {'Segment', 'Complex_discourse_unit'}
#~ for anno in annos.values():
    #~ for r in anno.relations:
        #~ ra, rb = r.args
        #~ if (ra.type not in valid) or (rb.type not in valid):
            #~ print(anno.basename, ra.id, rb.id, ra.type, rb.type, r.type)

def nlink(n):
    if n<6:
        return int(n*(n-1)/2)
    else:
        return 6*(n-6) + 15

# CSV preprocessing
def ext(h, v):
    _, n = re.split('#', h)

    if v in ('True', 'False'):
        tt = 'bool'
    elif re.match('^[0-9]+', v):
        tt = 'int'
    else:
        tt = 'str'

    return n, tt

with open(fpairs) as f:
    fi = iter(f)
    head, vals = next(fi), next(fi)
shead, svals = (re.split(',', s) for s in (head, vals))    
fields = list(map(ext, shead, svals))
names = [e[0] for e in fields]

# Counting from annotations
c_rel = 0
c_adjrel = 0
c_tpair = 0
c_pair = 0
c_lapse = 0
counts = defaultdict(int)
for anno in annos.values():
    for r in anno.relations:
        ra, rb = r.args
        if (ra.dialogue is None) or (rb.dialogue is None):
            continue
        if ra.dialogue.id != rb.dialogue.id:
            c_lapse += 1
            continue
        dpos = abs(ra.dialogue.units.index(ra) - rb.dialogue.units.index(rb))
        counts[dpos] += 1
        if dpos == 1:
            c_adjrel += 1
        if dpos == 0:
            print(anno.basename, r.type, ra.text, '//', rb.text)
    
    for d in anno.dialogues:
        n = len(d.units)
        c_tpair += int((n*(n-1))/2)
        c_pair += nlink(n)

print('RC between EDUs', sum(counts.values()))
print('RC total anno', sum(len(a.relations) for a in annos.values()))
print('RC counted', sum(counts.values()))
print('RC in window', sum(counts[k] for k in range(0,6)))
print('RC inter-dia', c_lapse)
print('Number of annofiles', len(annos))        
print(dict(counts))
print('PC in window', c_pair)
print('PC total', c_tpair)
print('='*20)

sys.exit()
# Compare annotations and CSV
uid_p, vid_p = (names.index(n) for n in ('id_DU1', 'id_DU2'))
def sid(e):
    l = e.split('_')
    return tuple('_'.join(pl) for pl in (l[:2], l[3:]))

def cdus(elt):
    res = [elt]
    if elt.inSchema:
        res.extend(cdus(elt.inSchema[0]))
    return res

def linked(ea, eb):
    for r in ea.inRelation:
        if eb in r.args:
            return (ea, eb)
    return None

c_labeled = 0
c_notfound = 0
c_stillnotfound = 0
cc_nf = defaultdict(int)
cc_snf = defaultdict(int)
with open(fpairs) as f:
    ilines = iter(f)
    next(ilines)
    for i, line in enumerate(ilines):
        if i%2 == 1:
            continue
        #~ print('{0:10}\r'.format(i), end='')
        
        asrc = re.split(',', line)
        # Only consider linked EDUs
        if asrc[0] != 'True':
            continue
        c_labeled += 1
        
        ui, vi = (asrc[k] for k in (uid_p, vid_p))
        (fn, uid), vid = sid(ui), sid(vi)[1]
        anno = annos[fn]
        try:
            ue, ve = (anno.elements[i] for i in (uid, vid))
        except KeyError:
            print('Missing EDU', ui, vi)
            continue

        # Normal case : 2 linked segments
        if linked(ue, ve):
            continue
        
        c_notfound += 1
        found = None
        cu, cv = (cdus(e) for e in (ue, ve))
        for ea in cu:
            for eb in cv:
                found = linked(ea, eb)
                if found:
                    break
            if found:
                break
        if not found:
            print('== ANOMALY ==')
            c_stillnotfound += 1
            print(anno.basename, ue.id, ve.id)
            print(ue.text)
            print(ve.text)
        else:
            fu, fv = found
            cc_nf[(cu.index(fu), cv.index(fv))] += 1
                #~ print('= Regular : {0} {1} ='.format(cu.index(fu), cv.index(fv)))
            
                #~ c_notfound += 1
                #~ cc_nf[(bool(ue.inSchema), bool(ve.inSchema))] += 1
                #~ if ue.inSchema:
                    #~ ue = ue.inSchema[0]
                #~ if ve.inSchema:
                    #~ ve = ve.inSchema[0]
                #~ try:
                    #~ rt = next(r for r in ue.inRelation
                        #~ if ve in r.args)
                #~ except StopIteration:
                    #~ c_stillnotfound += 1
                    #~ cc_snf[(bool(ue.inSchema), bool(ve.inSchema))] += 1
                

print(c_labeled)
print(c_notfound)
print(dict(cc_nf))
print(c_stillnotfound)
#~ print(dict(cc_snf))

# == OLD ZONE =============
#~ def order(dd):
    #~ return sorted((p for p in dd.items()), key=lambda e:e[1], reverse=True) 
#~ 
#~ sumlis = list()
#~ points = list()
#~ for anno in annos.values():
    #~ edd = defaultdict(lambda:defaultdict(int))
    #~ for r in anno.relations:
        #~ ra, rb = r.args
        #~ if (ra.dialogue is None) or (rb.dialogue is None):
            #~ ##~ print(ra.type, rb.type)
            #~ continue
        #~ edd[ra.dialogue.id][ra.turn.Emitter] += 1
        #~ edd[rb.dialogue.id][rb.turn.Emitter] += 1
    #~ for di, ec in edd.items():
        #~ s = sum(ec.values())
        #~ sumlis.append(s)
        #~ sm = ec[max(ec, key=lambda k:ec[k])]
        #~ points.append(float(sm)/s)
#~ 
#~ ##~ print(sumlis)
#~ ##~ print(points)
#~ plt.plot(range(len(points)), sorted(points))
#~ plt.show()
#~ 
#~ ##~ for k,v in order(rdd):
    ##~ print('{0:25}: {1}'.format(k, v))
    #~ 

