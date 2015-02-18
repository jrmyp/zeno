# Structure : Season Game Annotype Stage Files
def sel_season(l, req):
    return list(req)
    
def sel_game(l, req):
    return [n in l if n.startswith(('s1','s2','pilot'))]
    
def sel_annotype(l, req):
    return [r for r in re if r in l]
    
def sel_stage(l, req):
    ll = [n.lower() for n in l]
    return [r for r in req if r in l][0:1]

sels = (sel_season, sel_game, sel_annotype, sel_stage)    
rl = [('season1',), (), ('discourse',), ('gold', 'silver', 'bronze')]

def browse():
    tree = dict()
    for sel, par in zip(sels, rl):
        pass
