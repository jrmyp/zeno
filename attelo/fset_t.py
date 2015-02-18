# Feature set for tests
# Alias "please work please please pretty please" script

import os.path
import features as ft

pre_features = ft.pre_features
gen_features = ft.gen_features

@ft.helper('aprefix')
def h_aprefix(anno):
    return anno.basename + '_' + anno.annotype + '_'

@ft.single('about')
def id(si, ti):
    return ft.data['aprefix'] + si.id

# Also works by looking at last token
@ft.single('text')    
def end_bang(s, t):
    return s.text[-1] == '!'

# Idem
@ft.single('text')    
def end_qmark(s, t):
    return s.text[-1] == '?'
