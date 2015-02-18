# Structure checks, continued
# Hello, right frontier

# What if there is one or more parents
# - take the last subordinating link only

import sys
import annoget
from collections import defaultdict

#~ MAGIC = {'stac_1360734598', 'stac_1371161733', 'stac_1369335276', 'stac_1368640662', 'stac_1368708049', 'stac_1368694110', 'stac_1366561727', 'stac_1377311475', 'stac_1368161734', 'stac_1362332853', 'stac_1363534600', 'stac_1368693165', 'stac_1366232854', 'stac_1377296051', 'stac_1377296116', 'stac_1368694486', 'stac_1368694414', 'stac_1368640684', 'stac_1368708107', 'stac_1373761762', 'stac_1377311153', 'stac_1368708142', 'stac_1368694086', 'stac_1370861737', 'stac_1362934626', 'stac_1368708075', 'stac_1360532847', 'stac_1368708045', 'stac_1366261731', 'stac_1368708083', 'stac_1368640579', 'stac_1364527358', 'stac_1368708087', 'stac_1368708131', 'stac_1368640666', 'stac_1377296046', 'stac_1368708077', 'stac_1369335205', 'stac_1362034596', 'stac_1368694212', 'stac_1377311528', 'stac_1367927356', 'stac_1377311423', 'stac_1368640572', 'stac_1377296083', 'stac_1377311486', 'stac_1364534602', 'stac_1365461724', 'stac_1368640578', 'stac_1368694102', 'stac_1368708118', 'stac_1363332849', 'stac_1368694095', 'stac_1368694128', 'stac_1368694448', 'stac_1368694378', 'stac_1368694409', 'stac_1369661725', 'stac_1377296064', 'stac_1368694471', 'stac_1366532861', 'stac_1368693139', 'stac_1365661723', 'stac_1368361728', 'stac_1368640574', 'stac_1368694415', 'stac_1368694105', 'stac_1379461780', 'stac_1368640575', 'stac_1364834603', 'stac_1368640646', 'stac_1377296137', 'stac_1364532849', 'stac_1368694131', 'stac_1377296133', 'stac_1368693249', 'stac_1367427366', 'stac_1361734618', 'stac_1368640605', 'stac_1363934619', 'stac_1377296044', 'stac_1368693123', 'stac_1370861749', 'stac_1377311425', 'stac_1368693114', 'stac_1368640612', 'stac_1368708165', 'stac_1368694218', 'stac_1365061726', 'stac_1368640713', 'stac_1368640568', 'stac_1368708134', 'stac_1368561738', 'stac_1366561724', 'stac_1361234620', 'stac_1369761736', 'stac_1368694143', 'stac_1367234606', 'stac_1368694181', 'stac_1364132853', 'stac_1363734617', 'stac_1365634605', 'stac_1377296098', 'stac_1368640640', 'stac_1377311209', 'stac_1362132850', 'stac_1377296072', 'stac_1368694097', 'stac_1368693203', 'stac_1378461777', 'stac_1363034621', 'stac_1368861730', 'stac_1365934601', 'stac_1368694126', 'stac_1367861730', 'stac_1366867139', 'stac_1369334526', 'stac_1368694082', 'stac_1367961731', 'stac_1368640658', 'stac_1368708079', 'stac_1368640673', 'stac_1360434598', 'stac_1377311156', 'stac_1368694198', 'stac_1368708044', 'stac_1364432856', 'stac_1365761726', 'stac_1368694428', 'stac_1368694470', 'stac_1367161731', 'stac_1368694367', 'stac_1363134622', 'stac_1368640569', 'stac_1377311181', 'stac_1368708093', 'stac_1370761745', 'stac_1365232851', 'stac_1363832852', 'stac_1368693136', 'stac_1368708124', 'stac_1365327359', 'stac_1363634621', 'stac_1367867140', 'stac_1368527366', 'stac_1368694158', 'stac_1368694140', 'stac_1365327358', 'stac_1362232844', 'stac_1368694413', 'stac_1365461723', 'stac_1367227361', 'stac_1368694142', 'stac_1366061727', 'stac_1367432862', 'stac_1372167145', 'stac_1368640634', 'stac_1369335211', 'stac_1368693153', 'stac_1368227364', 'stac_1368708053', 'stac_1377296059', 'stac_1370361736', 'stac_1367261728', 'stac_1367927357', 'stac_1369627359', 'stac_1368694407', 'stac_1367661735', 'stac_1367461727', 'stac_1365061725', 'stac_1366427361', 'stac_1368694159', 'stac_1362932852', 'stac_1368640622', 'stac_1366032861', 'stac_1362134619', 'stac_1368640559', 'stac_1368693225', 'stac_1367834608', 'stac_1368708128', 'stac_1368693185', 'stac_1372667146', 'stac_1368694499', 'stac_1368694396', 'stac_1377311266', 'stac_1366527357', 'stac_1368640590', 'stac_1366434607', 'stac_1365727357', 'stac_1368561722', 'stac_1368640625', 'stac_1368708084', 'stac_1368640654', 'stac_1367927362', 'stac_1377311401', 'stac_1369227358', 'stac_1368694162', 'stac_1368693224', 'stac_1368861728', 'stac_1377311149', 'stac_1366727362', 'stac_1377311436', 'stac_1370927362', 'stac_1368927358', 'stac_1369335335', 'stac_1377311418', 'stac_1361134599', 'stac_1368693204', 'stac_1377296093', 'stac_1368694462', 'stac_1377296081', 'stac_1368640665', 'stac_1370867144', 'stac_1368694087', 'stac_1366761724', 'stac_1360232846', 'stac_1368694440', 'stac_1366461725', 'stac_1368640693', 'stac_1361334619', 'stac_1368694136', 'stac_1365261724', 'stac_1377311427', 'stac_1370161731', 'stac_1368693163', 'stac_1375061767', 'stac_1377311522', 'stac_1377311531', 'stac_1366434606', 'stac_1368694380', 'stac_1368694163', 'stac_1368694135', 'stac_1368694113', 'stac_1377296122', 'stac_1368640632', 'stac_1367461726', 'stac_1361634600', 'stac_1368693193', 'stac_1377296052', 'stac_1368640617', 'stac_1368640708', 'stac_1368694455', 'stac_1362234601', 'stac_1377311194', 'stac_1368694098', 'stac_1368694368', 'stac_1368640607', 'stac_1377311199', 'stac_1365334604'}
MAGIC = {'stac_1368694378'}
#~ SILENT = False
SILENT = True
def sprint(*a, **ka):
    if not SILENT:
        print(*a, **ka)

reports = list()
violations = defaultdict(list)

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

def pretty(e):
    return '{0}: {1}'.format(e.turn.Emitter, e.text) if e.type == 'Segment' else 'CDU'

def powerset(l):
    """ Set of subsets """
    ps = [[]]
    for x in list(l):
        ps.extend([s+[x] for s in ps])
    return frozenset(x for x in map(frozenset, ps))

def show_right_frontier(elts):    
    global report, violations
    # Get all linkable elements
    #~ ae = all_elts(elts)
    ae = sorted(elts, key=posnkey)
    
    aei = dict((e.id, i) for i,e in enumerate(ae))
    def sub_chain(e, p=set(), d=0):
        if not e:
            return []
        rel = sorted(
            [(aei[x.id], x, rt) for x, rt in rels(e)
                if x.id in aei
                and aei[x.id] < aei[e.id]
                and rt in SUBORDINATING_RELATIONS
                and ((not p) or x.turn.Emitter in p)
            ])

        if not rel:
            return [e]

        pe = rel[-1][1]
        return sub_chain(pe, p, d+1) + [e]
    
    def alt_chain(e, p=set(), keep=True):
        if not e:
            return []
        arel = sorted([(aei[x.id], x, rt) for x, rt in rels(e)
                if x.id in aei
                and aei[x.id] < aei[e.id]
                and ((not p) or x.turn.Emitter in p)
                ])
        srel, crel =([e for e in arel if e[2] in s]
            for s in (SUBORDINATING_RELATIONS, COORDINATING_RELATIONS))
        
        if srel:
            res = alt_chain(srel[-1][1], p, True)
        elif crel:
            res = alt_chain(crel[-1][1], p, False)
        else:
            res = []
        return res + ([e] if keep else [])
            
        
    count = defaultdict(int)
    emlast = dict()
    
    def tlast(ems):
        #~ print(len(list(emlast[e] for e in emlast if e <= ems)))
        cands = list(emlast[e] for e in emlast if e <= ems)
        return sorted(cands, key=posnkey)[-1] if cands else None
    
    for i, e in enumerate(ae):
        emits = frozenset(x.turn.Emitter for x in segs(e) if x.turn.Emitter)
        sprint('= {0}:{1} {2} {3}'.format(i, poskey(e), e.type, ' '.join(emits)))
        if i==0 or poskey(ae[i-1])[1] >= poskey(e)[0]:
             sprint("First of (sub)sequence")
             emlast[emits] = e
             continue
             
        # With last, ignoring speakers
        #~ frontier = sub_chain(ae[i-1])
        
        # With speaker pairs
        #~ print(dict((en, aei[eu.id]) for en, eu in emlast.items()))
        #~ frontier = set(x for sp, su in emlast.items()
                        #~ for x in sub_chain(su, emits | sp))
        
        # With all speaker groups !
        speaks = set(x for s in emlast for x in s)
        sprint(list(emits|s for s in powerset(speaks - emits)))
        frontier = set(x for s in powerset(speaks - emits)
                        for x in sub_chain(tlast(emits|s), emits|s))
        
        # With all groups and CDU simulation (this is getting silly) 
        #~ frontier = set(x for s in powerset(speaks - emits)
                        #~ for x in alt_chain(tlast(emits|s), emits|s))
        
        emlast[emits] = e
        
        #~ sprint("Frontier : {0}".format(sorted(set([aei[x.id] for x in kfrontier]))))
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
            
            # REPORT ZONE
            #~ if x not in frontier:
                #~ ##~ violations[x.dialogue.id].append(i)
                #~ msgr = 'subord.' if xr in SUBORDINATING_RELATIONS else 'coord.'
                #~ lrep = '\n'.join([
                    #~ "U: {0:20} {1}".format(x.id, pretty(x)),
                    #~ "C: {0:20} {1}".format(e.id, pretty(e)),
                    #~ "Rel: {0} ({1})".format(xr, msgr)
                    #~ ])
                #~ report.append(lrep)
                
            count[x in frontier] += 1
    
    return count

if __name__ != '__main__':
    sys.exit()

#~ DO_IT = ('report',)
#~ DO_IT = ('speak',)
DO_IT = ('count',)
c_rfv = defaultdict(int)
# COUNT MODE
if 'count' in DO_IT:
    rdia = set()
    for anno in annos.values():
        anno.convert_dt()
        for d in anno.dialogues:
            #~ if d.id not in MAGIC:
                #~ continue
            #~ print('== {0} - {1} =='.format(anno.basename, d.id))
            c = show_right_frontier(d.units)
            #~ input()
            #~ if c[False] > 0:
                #~ rdia.add(d.id)
            for k, v in c.items():
                c_rfv[k] += v

    print("RF violations")
    print(dict(c_rfv), sum(c_rfv.values()))
    #~ print(rdia)
    #~ print(dict(violations))

# REPORT MODE
if 'report' in DO_IT:
    for anno in annos.values():
        anno.convert_dt()
        print('== {0} =='.format(anno.basename))
        for d in anno.dialogues:
            report = list()
            show_right_frontier(d.units)
            if report:
                print('= {0} ='.format(d.id))
                print('\n\n'.join(report)+'\n')
                
if 'speak' in DO_IT:
    for anno in annos.values():
        ml = list()
        for s in anno.schemas:
            if s.type != 'Complex_discourse_unit':
                continue
            spl = set(x.turn.Emitter for x in segs(s)
                if x.turn.Emitter)
            if len(spl) > 1:
                ml.append('{0} {1} {2}'.format(poskey(s), s.id, ' '.join(spl)))
        if ml:
            print('== {0} =='.format(anno.basename))
            print('\n'.join(ml)+'\n')
