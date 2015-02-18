# Testing soothes the mind
import re

r_neg, r_snd, r_to, r_from, r_for = (re.compile(reg, re.I) for reg in
    ('(?<!\w)no|don\'?t', 'you|(any|some)one(?! *\?)', 'got|ha(ve|s)|giv|spare|offer', 'want|need|get', 'for'))
r_res = re.compile('(clay|ore|wheat|wood|sheep)', re.I)

names_r = ('clay', 'ore', 'wheat', 'wood', 'sheep')


def ext_one(txt, orig=True, pres_pre=True):
    pres_cue = pres_pre if not orig else not bool(r_neg.search(txt))

    m_to = r_to.search(txt)
    m_from = r_from.search(txt)
    if m_to:
        auto_cue = not bool(r_snd.search(txt[:m_to.start()]))
    elif m_from:
        auto_cue = bool(r_snd.search(txt[:m_from.start()]))
    else:
        auto_cue = bool(r_snd.search(txt))
    
    print(auto_cue)
    
    m_for = r_for.search(txt)
    if m_for:
        bef, aft = txt[:m_for.start()], txt[m_for.end():]
    else:
        bef, aft = txt, txt
        
    src = bef if (auto_cue == orig) else aft
    if orig and not auto_cue:
        src = ''
    lr = r_res.findall(src)
    res = [(pres_cue, r.lower()) for r in lr]
    return pres_cue, res

print(ext_one('I need clay'))
