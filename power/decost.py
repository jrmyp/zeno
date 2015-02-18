# Structure checks, continued
# Hello, right frontier

# What if there is one or more parents
# - take the last subordinating link only

import sys
import annoget
from collections import defaultdict

MAGIC = {'stac_1368694163': [7], 'stac_1366532861': [4, 8], 'stac_1361234620': [7], 'stac_1361134599': [6], 'stac_1377311194': [3], 'stac_1368693225': [7], 'stac_1368694181': [4], 'stac_1365461724': [4, 7], 'stac_1377311522': [2], 'stac_1368640590': [2, 10, 11, 13, 14], 'stac_1368361728': [2, 3, 5, 8], 'stac_1368693249': [7, 8, 9, 12, 35, 41, 44, 47, 49, 54, 56], 'stac_1368693185': [6, 9, 15, 16], 'stac_1368640708': [2, 3, 8], 'stac_1372667146': [2], 'stac_1367461727': [3, 6], 'stac_1369627359': [2, 8, 11, 15, 16], 'stac_1368640654': [14, 15, 19, 20, 23], 'stac_1368693136': [2], 'stac_1368708142': [2, 3, 4], 'stac_1375061767': [2], 'stac_1370761745': [4, 4, 5, 6], 'stac_1368694082': [2], 'stac_1363534600': [6, 16, 22, 24], 'stac_1366261731': [5], 'stac_1377296137': [2, 4], 'stac_1364432856': [2, 5], 'stac_1368640665': [2], 'stac_1368694471': [7], 'stac_1365232851': [5, 5], 'stac_1377311153': [4], 'stac_1368694095': [2, 3], 'stac_1368694113': [9], 'stac_1368561738': [2], 'stac_1368708128': [2, 3], 'stac_1365334604': [2, 3], 'stac_1370861737': [3, 6], 'stac_1362234601': [2, 3], 'stac_1365461723': [3, 6, 9, 10], 'stac_1368161734': [4, 5, 14, 16, 20, 24, 25], 'stac_1369335211': [3, 5, 5, 9, 14, 26, 28, 30, 37, 38, 40, 47], 'stac_1366032861': [2, 3], 'stac_1370927362': [3, 4], 'stac_1368640622': [3, 17, 18, 24, 25, 30, 34], 'stac_1368640646': [2, 3, 4], 'stac_1369335335': [5, 11], 'stac_1364132853': [6], 'stac_1369761736': [5], 'stac_1362132850': [3, 7, 8], 'stac_1368694126': [3], 'stac_1367834608': [4], 'stac_1377311266': [7, 8, 18], 'stac_1368694414': [2, 3, 4], 'stac_1368708107': [3, 4], 'stac_1368708087': [12, 12, 15, 17], 'stac_1377296116': [2, 4], 'stac_1368694407': [4], 'stac_1377296044': [3, 5, 5], 'stac_1368694380': [4, 9], 'stac_1368694413': [3], 'stac_1364527358': [8, 9, 11, 22], 'stac_1368694162': [2, 5, 6], 'stac_1368694158': [2], 'stac_1366761724': [3, 7, 8], 'stac_1368708045': [5], 'stac_1368527366': [9, 11], 'stac_1363332849': [5, 11], 'stac_1366061727': [7, 13, 15], 'stac_1365327358': [13, 15], 'stac_1368640607': [5, 9, 10], 'stac_1368640612': [9, 11], 'stac_1377311418': [4, 7, 9], 'stac_1368861728': [2, 3, 5, 6], 'stac_1368708083': [9], 'stac_1368694499': [2], 'stac_1362934626': [11, 17], 'stac_1368693193': [12, 15, 17, 22, 24, 30, 35, 36, 37], 'stac_1368708118': [10], 'stac_1377296052': [2], 'stac_1365661723': [2, 3], 'stac_1365061726': [3], 'stac_1368694105': [3, 5], 'stac_1371161733': [2], 'stac_1368694097': [6, 7], 'stac_1367227361': [4, 7], 'stac_1368640572': [9, 10, 15, 17, 18, 19, 24, 25, 26, 38, 39, 9], 'stac_1368694396': [3], 'stac_1360232846': [2], 'stac_1368694409': [10], 'stac_1362332853': [5], 'stac_1367927362': [3, 3, 4], 'stac_1366232854': [2], 'stac_1363034621': [10], 'stac_1367432862': [3, 4], 'stac_1368693139': [6], 'stac_1368693163': [4, 6], 'stac_1368708079': [3, 4], 'stac_1368694159': [2, 3], 'stac_1366461725': [2], 'stac_1377296083': [2, 2, 4], 'stac_1367461726': [7], 'stac_1373761762': [2], 'stac_1368640575': [3, 6, 9], 'stac_1368694218': [5, 6, 17, 19, 21, 21, 23, 26, 27, 31], 'stac_1377296064': [2, 4], 'stac_1377296046': [3, 5], 'stac_1361634600': [3], 'stac_1368694140': [3, 9, 11], 'stac_1368693224': [10, 11, 15, 15], 'stac_1368640634': [8, 12, 12], 'stac_1368694378': [6], 'stac_1370867144': [3], 'stac_1360434598': [2, 3], 'stac_1377311156': [5], 'stac_1369335276': [2, 3, 5, 7, 7], 'stac_1368694198': [6, 14, 18, 20], 'stac_1368693203': [3], 'stac_1366561727': [5, 7], 'stac_1367261728': [2, 4, 5], 'stac_1362932852': [2, 3], 'stac_1368708053': [2], 'stac_1368694110': [3], 'stac_1368693123': [6], 'stac_1377296093': [5, 6, 12, 14, 15, 20, 22], 'stac_1368694212': [9, 13, 15, 16, 20, 21], 'stac_1368640693': [3, 4, 6], 'stac_1365327359': [2], 'stac_1368694086': [2], 'stac_1368694448': [5], 'stac_1377296051': [2, 3], 'stac_1367927357': [7, 13, 17, 18, 21, 22], 'stac_1370361736': [4, 5], 'stac_1365934601': [12, 18, 18, 22, 28, 35, 42], 'stac_1362134619': [11, 14], 'stac_1366727362': [4], 'stac_1368708044': [2], 'stac_1368694136': [3, 7], 'stac_1377296072': [3, 4], 'stac_1368708077': [5, 6], 'stac_1377311149': [2], 'stac_1367861730': [2], 'stac_1368861730': [4, 6], 'stac_1368640658': [4, 14, 19, 19], 'stac_1368693114': [7], 'stac_1377296098': [2, 3, 5], 'stac_1367867140': [6, 7, 9, 12, 13, 15, 18], 'stac_1368694368': [2], 'stac_1365761726': [12], 'stac_1377311425': [8], 'stac_1368694098': [2, 5], 'stac_1364834603': [4, 7, 8, 11, 15, 19], 'stac_1368694143': [3, 7], 'stac_1368640579': [9, 14, 15, 16, 19, 20, 21], 'stac_1368640605': [9, 12, 20, 20, 34, 36, 36, 38], 'stac_1363134622': [5], 'stac_1379461780': [4], 'stac_1368640617': [6, 19, 22, 26, 29, 30, 33, 37, 44], 'stac_1367961731': [4], 'stac_1368708134': [3, 6], 'stac_1368708075': [2, 3, 3, 8, 14], 'stac_1367427366': [5, 8, 14, 19, 20, 22, 23, 24, 27], 'stac_1360734598': [2, 3, 4], 'stac_1377311427': [2, 3, 4, 9], 'stac_1377311423': [2], 'stac_1368640662': [5, 12, 14, 16, 29, 34], 'stac_1368694131': [6], 'stac_1365061725': [4], 'stac_1378461777': [2, 3], 'stac_1368640640': [8, 9], 'stac_1368708084': [3], 'stac_1368640578': [5], 'stac_1368640569': [3, 5, 9], 'stac_1368693204': [2], 'stac_1368227364': [4, 10], 'stac_1363832852': [4, 7], 'stac_1368694142': [2, 7, 8, 11], 'stac_1377311401': [2, 6, 8, 13, 19, 20, 21, 22, 26, 31, 37, 39, 41, 45, 46, 47, 49, 51, 63, 65, 65, 65, 65, 66, 66, 66, 69, 75, 76, 84, 88, 91, 92, 98, 98, 99], 'stac_1367234606': [4, 4], 'stac_1367161731': [6], 'stac_1368640625': [3, 10, 12, 14, 17, 18], 'stac_1368694455': [3, 6], 'stac_1361734618': [9], 'stac_1366867139': [6], 'stac_1366434607': [4], 'stac_1361334619': [6], 'stac_1368640559': [2, 3, 4], 'stac_1368694486': [3, 10, 15], 'stac_1366527357': [2, 6, 6, 10, 16, 19], 'stac_1377311209': [4], 'stac_1365261724': [2, 3, 4, 6, 8], 'stac_1368694440': [4, 10, 14, 17, 19, 25, 28], 'stac_1362034596': [4, 5, 9, 11], 'stac_1368640574': [6], 'stac_1366427361': [3, 6, 7, 8, 10, 12, 14, 15], 'stac_1367927356': [7, 7, 8, 10, 14, 16, 19, 21], 'stac_1377296122': [3], 'stac_1364532849': [2, 3], 'stac_1369227358': [4], 'stac_1377311181': [4], 'stac_1366434606': [2, 3], 'stac_1368694415': [3, 5], 'stac_1368693165': [3], 'stac_1368694102': [2, 8, 6], 'stac_1369335205': [10, 11, 12, 13, 19, 23], 'stac_1365727357': [5, 7, 10, 12], 'stac_1368694428': [8], 'stac_1368640684': [6], 'stac_1368694135': [6], 'stac_1368694087': [2, 3], 'stac_1368640666': [3, 4], 'stac_1364534602': [11, 12, 19], 'stac_1377296059': [2], 'stac_1370861749': [5], 'stac_1362232844': [8, 9, 15], 'stac_1377311528': [9, 12, 20, 32, 33], 'stac_1377311199': [4], 'stac_1368640673': [4, 5, 6, 11, 19, 22], 'stac_1367661735': [2], 'stac_1368693153': [9], 'stac_1370161731': [3, 4, 7], 'stac_1368561722': [6, 11, 14, 15, 18, 24, 25], 'stac_1377296081': [2, 4], 'stac_1368640568': [5, 6, 6, 7, 8, 14], 'stac_1363634621': [6, 9], 'stac_1377311486': [6, 13], 'stac_1369661725': [8, 10, 19, 24, 33, 38, 39, 40], 'stac_1368708131': [3, 6], 'stac_1368640632': [4, 5, 6], 'stac_1372167145': [4], 'stac_1368694367': [3], 'stac_1377296133': [5], 'stac_1368708093': [4], 'stac_1368640713': [2, 3, 4, 10, 12, 12], 'stac_1377311531': [7], 'stac_1368708124': [4, 5], 'stac_1368694470': [3, 4, 15, 21, 27, 28], 'stac_1368927358': [2, 14, 15, 19, 31, 33, 33, 35, 36], 'stac_1360532847': [2, 3], 'stac_1363934619': [7, 12, 17, 19, 26, 31, 41, 42, 44], 'stac_1368694128': [6, 8, 15, 18, 18], 'stac_1377311436': [2], 'stac_1365634605': [8, 9], 'stac_1377311475': [7, 8, 8, 15], 'stac_1363734617': [9, 12, 22, 29], 'stac_1369334526': [5, 8, 10, 22, 24, 28, 37, 38, 44, 45, 48, 54, 60, 64, 67, 70, 71, 73, 77, 79, 81, 82, 83, 85, 86, 92, 95, 98, 99, 101, 109, 110, 114, 115, 125, 131, 138, 138, 141, 142, 143, 144, 146, 147, 148, 153, 154], 'stac_1366561724': [16, 21, 22, 24], 'stac_1368708049': [2, 3, 7, 7], 'stac_1368708165': [7, 8, 9, 10], 'stac_1368694462': [5]}

SILENT = False
#~ SILENT = True
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

def show_right_frontier(elts):    
    global report, violations
    di = elts[0].dialogue.id
    # Get all linkable elements
    #~ ae = all_elts(elts)
    ae = sorted(elts, key=posnkey)
    
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
        #~ frontier = sub_chain(ae[i-1])
        # With speaker pairs
        #~ print(dict((en, aei[eu.id]) for en, eu in emlast.items()))
        frontier = set(x for sp, su in emlast.items()
                        for x in sub_chain(su, set([emits, sp])))
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
            if di in MAGIC and i in MAGIC[di]:
                sprint('D2 KO')
            
            # REPORT ZONE
            #~ if x not in frontier:
                #~ violations[x.dialogue.id].append(i)
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

c_rfv = defaultdict(int)
# COUNT MODE
if True:
    for anno in annos.values():
        anno.convert_dt()
        for d in anno.dialogues:
            if d.id not in MAGIC:
                continue
            print('== {0} =='.format(d.id))
            c = show_right_frontier(d.units)
            input()
            for k, v in c.items():
                c_rfv[k] += v

    print("RF violations")
    print(dict(c_rfv), sum(c_rfv.values()))
    #~ print(violations)

# REPORT MODE
if False:
    for anno in annos.values():
        #~ anno.convert_dt()
        print('== {0} =='.format(anno.basename))
        for d in anno.dialogues:
            report = list()
            show_right_frontier(d.units)
            if report:
                print('= {0} ='.format(d.id))
                print('\n\n'.join(report)+'\n')
                
