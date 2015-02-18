# Cycle catcher

# Works on a directory or a single file
import re
import os
import sys
import argparse as ap
import glozzdata as gd
from collections import defaultdict
from collections import Counter

class Node:    
    def __init__(self):
        self.links = []

    def link(self, other, relType, relId):
        self.links.append((other, relType, relId))
    

def process_file(fName):
    # Process data
    a = gd.Annotations(fName)
    a.gen_struct()
    nodes = defaultdict(Node)
    # Build graph
    allnodes = set()
    #~ print("N {0} -- {1}".format(len(a.relations), fName))
    for r in a.relations:
        u, v = (nodes[r.args[i].id] for i in range(2))
        u.link(v, r.type, r.id)
        v.link(u, r.type, r.id)
    for id, node in nodes.items():
        node.id = id
    cList = find_cycles(list(nodes.values()))
    return cList
    #~ print(len(cycles))
    
def find_cycles(nodelist):
    # Look for cycles
    # Scratch that, I'll rewrite everything

    # Custom algorithm (could be improved)

    stack = list()
    cycles = list()
    done = set()
    def dive():
        nst, ist = ([e[i] for e in stack] for i in (0,2))
        for (nn, rel, id) in stack[-1][0].links:
            try:
                ni = nst.index(nn)
                if id not in ist:
                    cyc = stack[ni+1:]
                    cyc.append((nn, rel, id))
                    cycles.append(cyc)
            except ValueError:
                if nn not in done:
                    stack.append((nn, rel, id))
                    dive()
        n, _, _ = stack.pop()
        done.add(n)
                    
    for n in nodelist:
        if n not in done:
            stack = [(n,'','')]
            dive()
    return cycles            

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Finds cycles')
    parser.add_argument('source', metavar='PATH', help='file/dir to look in', nargs='?', default='')    
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    
    source = args.source
    if os.path.isfile(source):
        gen = [source]
    elif os.path.isdir(source):
        gen = (os.path.join(source, name) for name in os.listdir(source)
                if name.endswith('.aa'))
    elif source == '':
        root = '/home/arthur/These/Master/Stac/data/socl-season1'
        g_a = (os.path.join(root, name, 'discourse') for name in os.listdir(root)
                if name.startswith('s1'))
        g_b = (os.path.join(src, 'bronze') for src in g_a
                if 'bronze' in os.listdir(src))
        gen = (os.path.join(src, name)
                for src in g_b 
                for name in os.listdir(src)
                    if name.endswith('.aa')
                )
    else:
        gen = []

    cRel = defaultdict(set)
    for name in gen:
        cyc = process_file(name)
        if args.verbose:
            print('== {0} =='.format(os.path.basename(name)))
            print(len(cyc)//2)
        seen = list()
        for c in cyc:
            l = [i for (_,_,i) in c][1:]
            if l[::-1] not in seen:
                seen.append(l)
                if args.verbose:
                    print([r for (_,r,_) in c][1:])
                for _, r, i in c:
                    cRel[r].add(i)
                
    ct = [(r, len(s)) for r,s in cRel.items()]
    ct = sorted(ct, key=lambda x:x[1], reverse=True)
    print(ct)
