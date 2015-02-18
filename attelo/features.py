# Feature extraction module
# Separate feature treatment form definition

import re
#~ import annodata
#~ from functools import wraps
from collections import deque

# Built at import
_single = dict()
_pair = dict()
_groups = dict()
_meta = set()
_conti = set()
_multi = dict()
_helpers = dict()

# Built at runtime
_slist = []
_plist = []
data = dict()

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
            _slist.append((n, f))

    _plist = list(_pair.items())
    
    #~ print(_plist, _slist)
    
    # Maybe use key/item but preserve order anyway
    snames, pnames = ([n for n,_ in l] for l in (_slist, _plist))
    _slist, _plist = ([f for _,f in l] for l in (_slist, _plist))
    mnames = _meta
    cnames = _conti
    
    return snames, pnames, mnames, cnames

def gen_features(anno, window=None):
    """ Yields features, in list format
    
    [pair feats, single feats 1, single feats 2]
    anno : source annotation, with full struct !
    """
        
    # Create EDU list and helper data
    for n, f in _helpers.items():
        data[n] = f(anno)
        #~ print(data[n])
    
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

def meta(f):
    """ Decorator for meta features """
    _meta.add(f.__name__)
    return f

def continuous(f):
    """ Decorator for continuous features """
    _conti.add(f.__name__)
    return f

def helper(name):
    """ Decorator for helper data creators """
    def wrap(f):
        _helpers[name] = f
        return f
    return wrap
    
