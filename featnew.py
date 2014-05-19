# Reimplementation of feature extractor
# Hopefully clean

# Python 3
# Test on Python 2 ?

# Todo : Sync with classify
# Todo : check multi, please
# Todo : maybe more arguments for pairs ?

# Cando : convert dicts to records (oh fanciness)
# Cando : reconvert meta to feature argument

# Tokens : tuple(word, lemma, start, end)
# Segments : Annotation Unit

import re
#~ import annodata
#~ from functools import wraps
from collections import deque

# Built at import
_single = dict()
_pair = dict()
_groups = dict()
_multi = dict()
_helpers = dict()

# Built at runtime
_slist = []
_plist = []
_help = dict()

def pre_features(options=None):
    """ Prepares feature computation """
    global _slist, _plist
    mnames = []
    for n, f in _single.items():
        if _multi[n]:
            for mn, me in _multi[n]:
                _slist.append(('{0}_{1}'.format(n, mn),
                    lambda s, t, e=me, lf=f : lf(s, t, e)))
        else:
            if _groups[n] == 'meta':
                mnames.append(n)            
            _slist.append((n, f))

    cls_f = None
    for n, f in _pair.items():
        if _groups[n] == 'class':
            cls_f = (n,f)
        else:
            _plist.append((n,f))
        if cls_f is None:
            print('Class missing... fail')
    _plist = [cls_f] + _plist
    
    #~ print(_plist, _slist)
    
    snames, pnames = ([n for n,_ in l] for l in (_slist, _plist))
    _slist, _plist = ([f for _,f in l] for l in (_slist, _plist))
     
    return snames, pnames, mnames

def gen_features(anno, window=None):
    """ Yields features, in list format
    
    [class, pair feats, single feats 1, single feats 2]
    anno : source annotation, with full struct !
    """
        
    # Create EDU list and helper data
    for n, f in _helpers.items():
        _help[n] = f(anno)
        #~ print(_help[n])
    
    edu_win = deque(maxlen=window)
    for dia in anno.dialogues:
        edu_win.clear()
        for s in dia.units:
            t = anno.parsed.tlist(s)
            # Generate single-EDU features
            d = list(f(s,t) for f in _slist)
            # Pair it with EDUs in window
            for ws, wt, wd in edu_win:
                pd = list(f(ws, wt, s, t) for f in _plist)
                yield pd + wd + d
            edu_win.append((s,t,d))

# Yes, this can be factorized even more. Maybe.
#   by "number of args" arg
#   by "on_pair" boolen arg
def single(group, name=None, meta=None, multi=None):
    """ Decorator for single-EDU features
    
    group : Feature group name
    name : Feature name
    """
    def wrap(f):
        n = name or f.__name__
        _single[n] = f
        _groups[n] = group
        _multi[n] = multi
        return f
    return wrap

def pair(group, name=None):
    """ Decorator for pair-of-EDU features
    
    group : Feature group name
    name : Feature name
    """
    def wrap(f):
        n = name or f.__name__
        _pair[n] = f
        _groups[n] = group
        return f
    return wrap

def helper(name):
    """ Decorator for helper data creators """
    
    def wrap(f):
        _helpers[name] = f
        return f
    return wrap

""" Provide:
    text
    tokens
    plist : player list
    elist : emoticon list
"""

@pair('class')
def dummy_cls(s, t, os, ot):
    return t[0][0]

# Also works by looking at last token
@single('text')    
def end_bang(s, t):
    return s.text[-1] == '!'

# Idem
@single('text')    
def end_qmark(s, t):
    return s.text[-1] == '?'
    
@single('text')    
def start_word(s, t):
    return t[0][1]
    
@single('text')    
def end_word(s, t):
    return t[-1][1]

# Needs an emoticon lexicon (rhymes)    
#~ @single('text')
#~ def has_emo(s, t):
    #~ return any((ti[0].lower() in elist for ti in t))
    
#~ @single('text')    
#~ def is_emo(s,t):
    #~ return has_emo(s,t) and len(t) == 1
    
@single('text')    
def num_tokens(s,t):
    return len(t)
    
@single('meta')    
def pos_start(s,t):
    return s.startPos

@single('meta')    
def pos_end(s,t):
    return s.endPos

lexicon = list((w,w) for w in ('ore', 'sheep', 'wheat', 'wood', 'clay'))
@single('lex', multi=lexicon)
def has_lex(s,t,l):
    return any((ti[1].lower() in l for ti in t))

@single('chat')
def first_speaker_in_dia(s,t):
    spn = s.turn.Emitter
    for tr in s.dialogue.turns:
        if s.turn == tr:
            break
        if tr.Emitter != spn:
            return False
    return True
    
@single('chat')
def turn_pos_in_dia(s,t):
    return s.dialogue.turns.index(s.turn)

#~ @single('chat')
#~ def ...(s,t):
    #~ pass
#~ 
#~ @single('chat')
#~ def ...(s,t):
    #~ pass

# Works, but useless. Who names people anyway ?
#~ @helper('player_names')
#~ def h_pnames(a):
    #~ return set(u.Emitter for u in a.units if u.type == 'Turn')
    #~ 
#~ @single('text')    
#~ def has_p_name(s, t):
    #~ l = _help['player_names']
    #~ return any((ti[0].lower() in l for ti in t))
