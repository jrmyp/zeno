# Structure checks - pre-decoding stuff

import sys
import annoget
from collections import defaultdict

T = set([1,2,3,4,5,6])
yup = set(['Segment', 'Complex_discourse_unit'])

annos = annoget.gather()

def cycles(lis):
    """ Returns list of lists of Segments"""
    def genNex(seg):
        res = list()
        for r in seg.inRelation:
            for arg in r.args:
                if arg != seg:
                    res.append(arg)
        return res
    
    chd = dict((s.id, genNex(s)) for s in lis)
    idlis = set(u.id for u in lis)
    
    def subcy(cands, clolis, found):
        if not cands:
            return found
        nfound = found[:]
        ncand = list()
        # Take head
        # Take all linked to
        for cand in cands:
            last = cand[-1]
            for nex in chd[nex.id]:
                if nex == cand[0]:
                    nfound.append(cand+[nex])
                elif (nex in clolis) or (nex in cand) or (nex.id not in idlis) :
                    continue
                ncands.append(cand+[nex])
        return subcy(ncands, clolis, nfound)
        
    res = list()
    for i in range(len(lis)):
        res.extend(subcy([lis[i]], lis[:i], []))
        
    return res

def segs(elt):
    if elt.type == 'Segment':
        return [elt]
    elif elt.type == 'Complex_discourse_unit':
        res = []
        for selt in elt.args:
            res.extend(segs(selt))
        return res
    #~ print(elt.type)
    return []

def firstPos(lis):
    return sorted(lis, key=lambda x:x.startPos)[0]

class Record:
    def __init__(self, su=list()):
        self.units = su[:]

def xturns(an):
    for d in an.dialogues:
        ct = Record()
        ce = ''
        for t in d.turns:
            if ce != t.Emitter:
                if ct.units:
                    yield ct
                ct = Record(t.units)
                ce = t.Emitter
            else:
                ct.units.extend(t.units)
        yield ct
    
def reord(t):
    return tuple(sorted((firstPos(segs(te)) for te in t), key=lambda e:e.startPos))

def etext(u):
    return ' '.join(s.text for s in segs(u))
    
def relins(lis):
    dem = set()
    ilis = set(e.id for e in lis)
    for u in lis:
        for r in u.inRelation:
            ar = set(a.id for a in r.args)
            if ar <= ilis:
                dem.add(r.id)
    return dem

def relto(lis):
    dem = defaultdict(int)
    phpos = sorted(e.startPos for e in lis)[0]
    for i, u in enumerate(lis):
        for r in u.inRelation:
            fsarg = reord(r.args)[0]
            if fsarg.startPos < phpos:
                dem[i] += 1
    return dem

### Precomputations

for anno in annos.values():
    for r in anno.relations:
        if not (set(a.type for a in r.args) <= yup):
            u, v = r.args
            print("\n= {0} = {1} =".format(r.type, anno.basename))
            print("{0} : {1}".format(u.type, u.id))
            print("{0} : {1}".format(v.type, v.id))
    
sys.exit()

### TASK 1
if 1 in T:
    print("== Task 1 : intra-turn structure ==")
    counts = defaultdict(lambda:defaultdict(int))
    counts_th = defaultdict(lambda:defaultdict(int))
    counts_ri = defaultdict(lambda:defaultdict(int))
    counts_l = defaultdict(int)
    print("WARNING : supposing that no pair is linked by more than one relation")    
    for anno in annos.values():
        #~ print("== {0} ==".format(anno.basename))
        # for t in anno.turns:
        for t in xturns(anno):
            lt = len(t.units)
            counts_l[lt] += 1
            si = set(u.id for u in t.units)
            if lt < 2:
                continue

            lr = len(relins(t.units))+1
            #~ print("{0:20}{1:5}{2:5}".format(t.id, len(t.units), len(relins(t.units))))
            for i, v in ((0, lr<lt), (1, lr==lt), (2, lr>lt)):
                if v:
                    counts[lt][i] += 1
            
            # Task 5
            tgts = set()
            for u in t.units:
                for r in u.inRelation:
                    su, sv = r.args
                    if su.id not in si or sv.id not in si:
                        continue
                    tgts.add(sv.id)
            counts_th[lt][len(si - tgts)] += 1
            
            # Task 2
            try:
                d = relto(t.units)
            except IndexError:
                #~ print(list(u.type for u in t.units))
                continue
            if len(si -tgts) == 0:
                hind = 0
            else:
                hind = list(i for i,v in enumerate(t.units) if v.id not in tgts)[0]

            for k, v in d.items():
                counts_ri[len(t.units)][k==hind] += v

        #~ break

    print(dict(counts_l))
    print('{0:>10}{1:>10}{2:>10}{3:>10}'.format('Length', 'Less', 'Exact', 'More'))
    for k in sorted(counts):
        ki, kj, kk = (counts[k][e] for e in range(3))
        print('{0:>10}{1:>10}{2:>10}{3:>10}'.format(k, ki, kj, kk))

### TASK 2
if 2 in T:
    print("== Task 2 : relation entering turns ==")
    #~ counts = defaultdict(lambda:defaultdict(int))
    #~ for anno in annos.values():
        #~ # for t in anno.turns:
        #~ for t in xturns(anno):
            #~ counts_l[len(t.units)] += 1
            #~ if len(t.units) < 2:
                #~ continue
            #~ try:
                #~ d = relto(t.units)
            #~ except IndexError:
                ##~ print(list(u.type for u in t.units))
                #~ continue
            #~ for k, v in d.items():
                #~ counts[len(t.units)][k] += v

    print("{0:>10}{1:>10}{2:>10}".format('Length', 'Head', 'Other'))
    for k in sorted(counts_ri):
        ki, kj = (counts_ri[k][v] for v in (True, False))
        print("{0:10}{1:>10}{2:>10}".format(k, ki, kj))

### TASK 3
if 3 in T:
    print("== Task 3 : relation exiting turns ==")
    counts = defaultdict(lambda:defaultdict(int))
    print("WARNING : right-frontier not defined yet")
    #~ for anno in annos.values():
        #~ pass

### TASK 4
if 4 in T:
    print("== Task 4 : CDU punctures ==")
    counts = defaultdict(int)
    for anno in annos.values():
        for s in anno.schemas:
            if s.type != 'Complex_discourse_unit':
                continue
            si = set(u.id for u in s.units)
            rogue = list()
            for us in s.units:
                for r in us.inRelation:
                    for ur in r.args:
                        if ur.type == 'Segment' and ur.id not in si:
                            rogue.append(r)
                        elif ur.type == 'Complex_discourse_unit':
                            ure = segs(ur)
                            if any((ureu.id not in si) for ureu in ure):
                                rogue.append(r)
            counts[not bool(rogue)] += 1
            
    for k in sorted(counts):
        print('{0:>10}{1:>10}'.format(k, counts[k]))

### TASK 5
if 5 in T:
    print("== Task 5 : Turn heads ==")
    print("WARNING : Case >3 heads ignored for now")
    # See task 1
    print('Row : Turn length -- Col : Heads')
    print('{0:>10}{1:>10}{2:>10}{3:>10}'.format('', 1, 2, 3))
    for k in sorted(counts_th):
        kk = (counts_th[k][e] for e in range(1, 4))
        print('{0:>10}{1:>10}{2:>10}{3:>10}'.format(k, *kk))
    
### TASK 6
if 6 in T:
    print("== Task 6 : Backward links ==")
    print("WARNING : errors in annotations may remain")
    counts = defaultdict(int)
    for anno in annos.values():
        for r in anno.relations:
            ux, vx = r.args
            if ux.type not in yup or vx.type not in yup:
                continue
            u, v = (firstPos(segs(e)) for e in r.args)
            if u.startPos > v.startPos :
                #~ print("\n= {0} = {1} =".format(r.type, anno.basename))
                #~ print("{0} : {1}".format(u.turn.Emitter, etext(u)))
                #~ print("{0} : {1}".format(v.turn.Emitter, etext(v)))
                counts[r.type] += 1

    for k in sorted(counts):
        print('{0:20}{1:>10}'.format(k, counts[k]))
