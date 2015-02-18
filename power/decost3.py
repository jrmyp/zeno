# Right frontier, continued, again
# This is getting out of hand

# One problem.
# You're going up sub-graphs filtering only conversations between
# Some people. But you have to include them only if they're really talking

# This could be problematic when dealing with monologues

import sys
import annoget
from collections import defaultdict

# I know, should do it with argparse
INTERACT_MODE = True
# INTERACT_MODE = False

outfile = 'res.txt'

S_R = SUBORDINATING_RELATIONS = set(
    ['Explanation',
     'Background',
     'Elaboration',
     'Correction',
     'Q-Elab',
     'Comment',
     'Question-answer_pair',
     'Clarification_question',
     'Acknowledgement'])

C_R = COORDINATING_RELATIONS = set(
    ['Result',
     'Narration',
     'Continuation',
     'Contrast',
     'Parallel',
     'Conditional',
     'Alternation'])

def segs(elt):
    if elt.type == 'Segment':
        return [elt]
    elif elt.type == 'Complex_discourse_unit':
        return [x for selt in elt.args for x in segs(selt)]
    return []

def emits(elt):
    return set(e.turn.Emitter for e in segs(elt))

def all_units(box, lis):
    """ All units (even CDUs) inside box """
    sbox = set(box.units)
    return set(u for u in lis
        if segs(u)
        if set(segs(u)) <= sbox)

def poskey(elt):
    sl = segs(elt)
    if not sl:
        print('ANOMALY', elt.id, elt.type)
    return (min(x.startPos for x in sl),
            max(x.endPos for x in sl))

def posnkey(elt):
    u, v = poskey(elt)
    return (u, -v)

def powerset(l, min_size=0):
    """ Set of subsets """
    ps = [[]]
    for x in list(l):
        ps.extend([s+[x] for s in ps])
    return [set(s) for s in ps if len(s)>=min_size]

def pretty(e):
    if e.type == 'Segment':
        return '{0}: {1}'.format(e.turn.Emitter, e.text)
    else:
        return 'CDU from {0}'.format(' '.join(emits(e)))

def rels(elt):
    return list((x, r.type) for r in elt.inRelation
                    for x in r.args if x!=elt)

def prec_rels(elt, group):
    return set((e, rel) for (e, rel) in rels(elt)
        if e in group
        if poskey(e) < poskey(elt))
    
def all_rf(elts):
    def right_frontier(candidate, speakers):
        frontier, explored = set(), set()
        prev = [e for e in elts[:elts.index(candidate)]
            if emits(e) <= speakers]
        sprev = set(prev)
        prev_speakers = set(s 
            for e in prev+[candidate]
            for s in emits(e))
        
        # print(len(prev), prev_speakers)
        # Go up the history
        for pe in reversed(prev):
            if pe in explored:
                continue
            open_list = [(pe, True, True)]
            local_frontier = set()
            local_explored = set()
            local_speakers = set()
            while open_list:
                cur_e, by_sub, on_rf = open_list.pop()
                if cur_e in explored:
                    # Already explored component : abort !
                    local_frontier.clear()
                    del open_list[:]
                    continue

                local_explored.add(cur_e)
                local_speakers |= emits(cur_e)
                
                # Is the unit a true RF member ?
                if by_sub and on_rf:
                    local_frontier.add(cur_e)
                
                # Relations from preceding units
                erel = prec_rels(cur_e, prev)
                if not erel:
                    continue
                
                # We want the next unit in RF:
                #   Priority to subordinating relations
                #   Priority to late units
                rf_e, _ = sorted(erel, 
                    key=lambda x:(x[1] in S_R, poskey(x[0])))[-1]

                # Continue the search
                open_list.extend((e, (rel in S_R), (on_rf and e==rf_e))
                    for e, rel in erel)
            
            # Search is over, wrap up
            explored |= local_explored
            # Filter out singletons
            if prev_speakers == local_speakers:
                frontier |= local_frontier
        
        return frontier

    # Get all speaker subsets (at least two of them)
    subsets = powerset(set(se.turn.Emitter
        for e in elts
        for se in segs(e)), 2)
    # print(subsets)
    
    res = dict()
    for e in elts:
        res[e] = set(x for s in subsets
            for x in right_frontier(e, s))
    
    return res
    
count_rfv = defaultdict(int)
annos = annoget.gather()

with open(outfile, 'w') as f:
# Get annos in order (clearer display)
 for name in sorted(annos):
    print('Processing {0:30}\r'.format(name), end='')
    f.write('== {0} ==\n'.format(name))
    anno = annos[name]
    report = []
    # print([u.type for u in anno.units])

    # Dialogues are already ordered
    for d in anno.dialogues:
        # Units are already ordered
        # Get top-level EDU-CDUs
        d_units = all_units(d, anno.elements.values())
        top = sorted((u for u in d_units if not u.inSchema),
                key=poskey)
        topid = dict((e, i) for i, e in enumerate(top))
        rfs = all_rf(top)
        for e in top:
            if INTERACT_MODE:
                print('= {0}:{1} {2} {3}'.format(
                    topid[e], poskey(e), e.type,
                    ' '.join(emits(e))))

            # Skip first unit
            if topid[e] == 0:
                if INTERACT_MODE:
                    print('First of (sub)sequence\n')
                continue
            rf = rfs[e]
            if INTERACT_MODE:
                print('Frontier: {0}'.format(sorted(topid[x] for x in rf)))
            for ae, ar in prec_rels(e, top):
                invalid = ae not in rf
                if INTERACT_MODE:
                    print('{0} {1} {2} {3}'.format(
                        'KO' if invalid else 'OK',
                        topid[ae],
                        'S' if ar in S_R else 'C',
                        ar))
                count_rfv[invalid] += 1
                if invalid:
                    lrep = '\n'.join([
                    # "-- {0} {1}".format(ae.dialogue.id, e.dialogue.id),
                    "U: {0:20} {1}".format(ae.id, pretty(ae)),
                    "C: {0:20} {1}".format(e.id, pretty(e)),
                    "Rel: {0}".format(ar)
                    ])
                    report.append(lrep)
            
            if INTERACT_MODE:
                input()
            
        if report:
            f.write('= Dialogue id : {0} =\n'.format(d.id))
            f.write('\n\n'.join(report)+'\n\n')


print('{0:40}'.format('Right-frontier violations'))
tv, fv = count_rfv[True], count_rfv[False]
data = (
    ('Total relations', tv+fv),
    ('RF violations', tv),
    ('Violation ratio', '{0:.1f}%'.format(100*float(tv)/(tv+fv)))
    )
for title, val in data:
    print('{0:>8}{1:5}{2}'.format(val, '', title))
