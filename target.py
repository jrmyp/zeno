# Uncover the deep secrets of commitments
# Soon in theaters

from __future__ import print_function
import sys
import os
import re

import annodata as ad
import classify as cs
from collections import defaultdict
from codecs import open

sroot = '/home/arthur/These/Master/Stac/data/socl-season1'
ffinal = '/home/arthur/These/Data/socl-season1.final.tab'
oracle_nc = 62

fxqap = '/home/arthur/These/Data/socl-season1.xqap.tab'

r_neg, r_snd, r_to, r_from, r_for = (re.compile(reg, re.I) for reg in
    ('(?<!\w)no', 'you|(any|some)one', 'got|ha(ve|s)|giv|spare|offer', 'want|need', 'for'))
r_res = re.compile('(clay|ore|wheat|wood|sheep)', re.I)

names_r = ('clay', 'ore', 'wheat', 'wood', 'sheep')

def ext_com(ue, qe):
    def ext_one(txt, orig=True, pres_pre=True):
        pres_cue = pres_pre if not orig else not bool(r_neg.search(txt))

        m_to = r_to.search(txt)
        if m_to:
            auto_cue = not bool(r_snd.search(txt[:m_to.start()]))
        else:
            auto_cue = bool(r_snd.search(txt))

        m_for = r_for.search(txt)
        if m_for:
            bef, aft = txt[:m_for.start()], txt[m_for.end():]
        else:
            bef, aft = txt, txt
            
        src = bef if (auto_cue == orig) else aft
        lr = r_res.findall(src)
        res = [(pres_cue, r) for r in lr]
        return pres_cue, res
    
    pc, ru = ext_one(ue.text)
    if not ru and qe is not None:
        ru = ext_one(qe.text, False, pc)[1]

    dres = dict()
    for fp, fr in ru:
        if fp:
            dres[str(fr)] = ('1', 'infinity')
        else:
            dres[str(fr)] = ('0', '0')
    return dres
    
def get_commitments(s, clist):
    """ Get all commitment resources for a given Segment """
    return dict((c.Resource, (c.Lower_bound, c.Upper_bound))
        for c in clist if (s in c))

def compat(p, q):
    pl, ph = p
    ql, qh = q
    return max(pl, ql) <= min(ph, qh)

def g_n():
    """ Iterates on all files annotated with Commitment
        Yields annotation objects
    """
    for gname in os.listdir(sroot):
        if gname.startswith('s1'):
            p0 = os.path.join(sroot, gname)
            p1 = os.path.join(p0, 'commitment', 'jperret')
            if os.path.isdir(p1):
                for fname in os.listdir(p1):
                    if fname.endswith('.aa'):
                        bname = fname[:-3]
                        #~ if bname == 's1-league1-game2_07':
                            #~ continue
                        a = ad.Annotations(os.path.join(p1, fname))
                        a.load_text(os.path.join(p0, 'unannotated', bname+'.ac'))
                        a.gen_struct()
                        a.commitments = list(u for u in a.units if u.type == 'Commitment')
                        yield bname, a

# Without counter
#~ all_anno = dict(g_n())

# With counter
all_anno = dict()
for i, pair in enumerate(g_n()):
    n, anno = pair
    all_anno[n] = anno
    print('Loading ({0}/{1}) : {2}\r'.format(i+1, oracle_nc, n), end='')
    sys.stdout.flush()
print('\nAnnotations loaded')

def nsplit(id):
    l = id.split('_')
    return tuple('_'.join(pl) for pl in (l[:2], l[-2:]))

ques = defaultdict(list)
x_t = cs.TabData(fxqap)
for row in x_t:
    gi, si = nsplit(row['q_id'].value)
    if gi in all_anno:
        ques[nsplit(row['a_id'].value)].append((gi, si))

#~ print(ques)
#~ sys.exit()
c_t = cs.TabData(ffinal)
c_t.new_class('is_commitment')
#~ end_c = cs.Trainer(c_t, 10, 'dialogue', learner='logreg')
end_c = cs.Trainer(c_t, 10, 'dialogue')
end_c.evaluate()

tot_ok = 0
tot_in = 0
tot_all = 0

with open('res/zog.txt', 'w', encoding='utf-8') as f:
    for pred, row in end_c.pred_rows():
        if pred.value == 'True' and row.getclass().value == 'True':
    #~ for row in c_t:
        #~ if row.getclass().value == 'True':
            gi, si = nsplit(row['id'].value)
            u = all_anno[gi].elements[si]
            f.write(u.text +'\n')
            qe = None
            if (gi, si) in ques:
                f.write('Predicted answer to :\n')
                for gai, sai in ques[(gi, si)]:
                    try:
                        qe = all_anno[gai].elements[sai]
                        f.write(qe.text + '\n')
                    except KeyError:
                        f.write('Derp\n')
                    break

            rul_c = ext_com(u, qe)
            ann_c = get_commitments(u, all_anno[gi].commitments)
            
            for n in names_r:
                if (n in rul_c) != (n in ann_c):
                    tot_all += 1
                    continue
                if (n in rul_c) and (n in ann_c):
                    tot_all += 1
                    if rul_c[n] == ann_c[n]:
                        tot_ok += 1
                        tot_in += 1
                    elif compat(rul_c[n], ann_c[n]):
                        tot_in += 1
                    else:
                        print(n, rul_c[n], ann_c[n])
            
            f.write('Rule says : {0}\n'.format(rul_c))
            f.write('Anno says : {0}\n'.format(ann_c))
            f.write('\n')
        
print(tot_all)
print(tot_in)
print(tot_ok)
print('Done')
