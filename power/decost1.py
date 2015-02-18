# Structure checks, continued
# Hello, right frontier

# What if there is one or more parents
# - take the last subordinating link only

import sys
import annoget
from collections import defaultdict

#~ SILENT = False
SILENT = True
def sprint(*a, **ka):
    if not SILENT:
        print(*a, **ka)

T = set([])
SUBORDINATING_RELATIONS = set(
    ['Explanation',
     'Background',
     'Elaboration',
     'Correction',
     'Q-Elab',
     'Comment',
     'Question-answer_pair',
     'Clarification_question',
     'Acknowledgement'])

COORDINATING_RELATIONS = set(
    ['Result',
     'Narration',
     'Continuation',
     'Contrast',
     'Parallel',
     'Conditional',
     'Alternation'])
     
annos = annoget.gather()

def segs(elt):
    if elt.type == 'Segment':
        return [elt]
    elif elt.type == 'Complex_discourse_unit':
        return [x for selt in elt.args for x in segs(selt)]
    #~ print(elt.type)
    return []

def poskey(elt):
    sl = segs(elt)
    return (min(x.startPos for x in sl),
            max(x.endPos for x in sl))

def posnkey(elt):
    u, v = poskey(elt)
    return (u, -v)

def all_elts(el):
    raw = list()
    def schl(s):
        return [s] + [sse for se in s.inSchema for sse in schl(se)]
    
    for e in el:
        for s in schl(e):
            if s not in raw:
                raw.append(s)
    
    return sorted(raw, key=posnkey)

def rels(elt):
    return [(x, r.type) for r in elt.inRelation for x in r.args if x!=elt]

def show_right_frontier(elts):    
    # Get all linkable elements
    ae = all_elts(elts)
    #~ ae = sorted(elts, key=posnkey)
    
    aei = dict((e.id, i) for i,e in enumerate(ae))
    def sub_chain(e, p=set(), d=0):
        #~ if d==10:
            #~ ##~ print("CEILING")
            #~ return [e]
        rel = sorted(
            [(aei[x.id], x, rt) for x, rt in rels(e)
                if x.id in aei
                and aei[x.id] < aei[e.id]
                and rt in SUBORDINATING_RELATIONS
                and ((not p) or x.turn.Emitter in p)
            ])
        if not rel:
            return [e]
        else:
            pe = rel[-1][1]
            #~ if pe == e:
                #~ print('ANOMALY')
                #~ return [e]
            return sub_chain(pe, p, d+1) + [e]
        
    count = defaultdict(int)
    emlast = dict()
    for i, e in enumerate(ae):
        emits = (e.turn.Emitter if e.type == 'Segment'
            else frozenset([x.turn.Emitter for x in segs(e)]))
        sprint('= {0}:{1} {2} {3}'.format(i, poskey(e), e.type, emits))
        if i==0 or poskey(ae[i-1])[1] >= poskey(e)[0]:
             sprint("First of (sub)sequence")
             emlast[emits] = e
             continue
             
        # With last, ignoring speakers
        frontier = sub_chain(ae[i-1])
        # With speaker pairs
        #~ print(dict((en, aei[eu.id]) for en, eu in emlast.items()))
        #~ frontier = set(x for sp, su in emlast.items()
                        #~ for x in sub_chain(su, set([emits, sp])))
        emlast[emits] = e
        
        sprint("Frontier : {0}".format(sorted(set([aei[x.id] for x in frontier]))))
        prel = sorted(
            [(aei[x.id], x, rt) for x, rt in rels(e)
                if x.id in aei
                and aei[x.id] < i
            ])
        for xi, x, xr in prel:
            msg = 'OK' if x in frontier else 'KO'
            sprint('{0} {1} {3} {2}'.format(msg, xi, xr,
                'S' if xr in SUBORDINATING_RELATIONS else 'C'))
            count[x in frontier] += 1
    
    return count

if __name__ != '__main__':
    sys.exit()

c_rfv = defaultdict(int)
for anno in annos.values():
    anno.convert_dt()
    for d in anno.dialogues:
        #~ print('== {0} =='.format(d.id))
        c = show_right_frontier(d.units)
        #~ input()
        for k, v in c.items():
            c_rfv[k] += v

print("RF violations")
print(dict(c_rfv))
