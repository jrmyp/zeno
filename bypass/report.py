""" Scoring for bypass annotation """

"""Use sets... use sets....
OMG, genius !"""

import numpy as np
from collections import defaultdict

def sdiv(a,b):
    return a/b if b != 0 else 0.

def doc_score(ref, pred):
    """ Ref and pred are lists of triplets """

    def score_set(ref, pred):
        true_pos = float(len(ref & pred))
        sum_pred = len(pred)
        sum_ref = len(ref)
        return np.array((true_pos, sum_pred, sum_ref))
    
    ref_rel = set(ref)
    ref_att = set(e[:2] for e in ref)
    pred_rel = set(pred)
    pred_att = set(e[:2] for e in pred)

    return np.hstack((score_set(ref_att, pred_att),
        score_set(ref_rel, pred_rel)))

def score(iscores):
    """ iscores iterates on doc_score res """

    def score_stat(true_pos, sum_pred, sum_ref):
        precision = sdiv(true_pos, sum_pred)
        recall = sdiv(true_pos, sum_ref)
        f_score = sdiv(2*precision*recall, precision+recall)
        return f_score, precision, recall

    sums = np.vstack(iscores).sum(0)
    return score_stat(*sums[:3]), score_stat(*sums[3:])

def score_line(iscores=None, method='unknown'):
    def p_tri(t):
        return ''.join('{0:>8.1f}'.format(100*e) for e in t)
        
    if iscores is None:
        # Return header
        res = ('{0:20}|{1:^24} |{2:^24}'.format(
            '', 'ATTACHMENT', 'RELATIONS'),
         '{0:20}|{1:>8}{2:>8}{3:>8} |{4:>8}{5:>8}{6:>8}'.format(
            '', 'f1', 'prec', 'rec', 'f1', 'pre', 'rec'))
        return '\n'.join(res)
    # Return regular line
    a_s, r_s = score(iscores)
    return '{0:<20}|{1} |{2}'.format(method, p_tri(a_s), p_tri(r_s))
    
def tri_to_conll(tri, dia, order, rels):
    def tune(id):
        return id.replace('discourse', 'unannotated')

    units = set()
    parents = defaultdict(list)
    for u, v, r in tri:
        if order[u].startswith('ROOT'):
            continue
        units.update((u, v))
        parents[v].append((tune(order[u]), rels[r]))

    res = ''
    for v in units:
        pl = parents[v]
        if not pl:
            pl.append(('0', 'ROOT'))
        # print(v, pl)
        res += '\t'.join([tune(order[v]), dia, '0', '0'] +
            ['\t'.join((u,r)) for u, r in pl]) + '\n'

    return res

    
    
