# Bypass attelo entirely
# Not enough time to do otherwise

# Theorically could work with scipy.sparse
# but let's not get ahead of ourselves there

# Sparse note : shift rel ids by one (currently -1 is unrelated)

import os
import numpy as np
from functools import wraps
from collections import defaultdict

import config as cfg
from ilp import parse_pairs

join = os.path.join

""" Arguments for decoders
prob is a numeric 2d array (or equivalent)
    prob[i][j] is the probability of attachment (i,j)
    note that you must combine attach & prob models beforehand
rels is a str 2d array (or equivalent)
    rel[i][j] is the relation used for attachment
order is a str array with ids in the correct order
    order[n] is the n-th EDU in timeline
"""

class Data:
    pass

def get_decoder(name):
    """ Return correctly configured decoder """
    t = next(e for e in _decoders if e[0] == name)
    return lambda d: t[1](d,*t[2:])

def needs():
    """ Decorator : set requirements for data argument """
    pass

def argnames(t):
    def wrap(f):
        return f
    return wrap

@argnames(())
def d_last(data):
    """ Baseline : attach to last """
    rels = data.rels
    pred = []
    for i in range(len(rels)-1):
        pred.append((i, i+1, rels[i][i+1]))

    return pred

@argnames(('threshold',))
def d_local(data, threshold=0.5):
    """ Baseline : attach if prob > threshold """
    prob, rels = data.prob, data.rels
    pred = []
    for i in range(len(prob)):
        for j in range(len(prob)):
            if prob[i][j] > threshold:
                pred.append((i, j, rels[i][j]))

    return pred

@argnames(())
def d_ilp(data):
    """ Retrieve ILP results from files """
    pred = []
    rels, d_path = data.rels, data.ilp_path
    if not os.path.exists(d_path):
        return None
    for i, j in parse_pairs(d_path):
        pred.append((i, j, rels[i][j]))

    return pred

@argnames(())
def d_mst(data):
    """ MST, but faster ? """
    pass

@argnames(())
def d_msdag(data):
    """ MSDAG, but faster ? """
    pass

@argnames(())
def d_mst_plus(data, thres=0.5, maxdist=5):
    """ MST with added edges """
    base, full, (iqap, iack) = data.base.copy(), data.full, data.irels
    qap_up = defaultdict(set)
    qap_down = defaultdict(set)
    ack_down = defaultdict(set)

    # Next, test it with nonzero...
    for i in range(len(base)):
        for j in range(len(base)):
            if base[i][j] == iqap:
                qap_up[j].add(i)
                qap_down[i].add(j)
            elif base[i][j] == iack:
                ack_down[i].add(j)

    # Check nodes C that verify A-qap-C-ack-B
    # Then if A-qap-D then link D-ack-B
    for c in (set(qap_up) & set(ack_down)):
        for a in qap_up[c]:
            for d in qap_down[a]:
                for b in ack_down[c]:
                    if (0 < (b-d) <= maxdist) and base[d][b] == -1 and full[d][b][iack] > thres:
                        base[d][b] = iack

    pred = list()
    for i in range(len(base)):
        for j in range(len(base)):
            if base[i][j] >= 0:
                pred.append((i, j, base[i][j]))

    return pred
    
def mat_to_tsr(fmat):
    """ From rel.dat to 3D map """
    with open(fmat) as f:
        itf = iter(f)
        names = next(itf).rstrip().split(' ')
        rsize = len(next(itf).rstrip().split(':'))
        size = len(names)
        data = np.zeros((size, size, rsize), float)
        for i, line in enumerate(itf):
            if not line:
                break
            for j, block in enumerate(line.rstrip().split(' ')):
                data[i][j] = np.fromstring(block, dtype=float, sep=':')
    return data, names

def mat_to_map(fmat, attach=False, use_float=False):
    """ From .dat to 2D map

    Uses numpy, because efficiency """
    def relblock(block, dt):
        a = np.fromstring(block, dtype=dt, sep=':')
        return a.argmax() if np.max(a) > 0 else -1
        
    with open(fmat) as f:
        itf = iter(f)
        names = next(itf).rstrip().split(':' if attach else ' ')
        if not attach:
            next(itf)
        size = len(names)
        dt = float if use_float else int
        data = np.zeros((size, size), dt)
        for i, line in enumerate(itf):
            if not line:
                break
            if attach:
                data[i] = np.fromstring(line.rstrip(), dtype=dt, sep=':')
            else:
                data[i] = np.fromiter((relblock(b, dt)
                    for b in line.rstrip().split(' ')), dt, size)

    return data, names

def mat_to_tri(frel):
    """ From .rel.dat to decoding triplets

    Used to retrieve already decoded stuff
    """
    tri = list()
    with open(frel) as f:
        itf = iter(f)
        names = next(itf).rstrip().split(' ')
        next(itf)
        for i, line in enumerate(itf):
            if not line:
                break
            for j, block in enumerate(line.rstrip().split(' ')):
                a = np.fromstring(block, dtype=int, sep=':')
                if np.max(a) > 0:
                    tri.append((i, j, a.argmax()))
    return tri, names

def tri_to_mat(ftgt, order):
    pass

# Syntax : name, fun, extra args
_decoders = (
    ('last', d_last),
    ('local', d_local, 0.5),
    ('ilp', d_ilp)
)

def run(d_name):
    pass

