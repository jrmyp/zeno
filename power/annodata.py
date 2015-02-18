# Data holders for annotation files !
#   Glozz
#   Stanford XML

# Python 3
# Sorry, homemade. I'll keep looking.

# TODO : Correct those gorram ids...
#   Done ? I think it was for those Offer things... shared ids (bad)
#   Actually, you'll have problems loading 2 annotypes
#       as 2 identical segments will have the differents nids
#   Just load only one annotype for now...
# TODO : Add documentation (ha ha ha)

import re
import xml.etree.ElementTree as ET
import nxml
from itertools import chain
# If Python 2...
from codecs import open

auto_id = 0

class Annotations:
    """ Holds annotations in Glozz format """
    
    def __init__(self, *args):
        """ Class initializer
        
        baseanno : Glozz filename to be loaded
        """
        
        # Discriminating id suffix for annotation groups
        self.delta = 0
        
        self.annoname = None
        self.ids = set()
        self.units = list()
        self.relations = list()
        self.schemas = list()
        if args:
            self.load_anno(*args)
    
    def load_anno(self, annofilename, basename='', annotype='unannotated'):
        """ Load Glozz annotations """
        
        def nid(id):
            """ Actual, unique id for unit
                Some ids are re-used from one file to another
            """
            #~ return "{0}_{1}".format(id, self.delta)
            return id
        
        def common(src, tgt):
            tgt._base = self
            tgt.id = nid(src.id)
            tgt.oid = src.id
            cr = src.characterisation
            tgt.type = cr.type._val()
            tgt.features = dict((f.name, f._val()) for f in cr.featureSet.all('feature'))
            tgt.inRelation = list()
            tgt.ordRelation = dict()
            tgt.inSchema = list()
            return (tgt.id in self.ids)

        self.annoname, self.annotype, self.basename = (
            annofilename, annotype, basename)
        annoelt = nxml.load(annofilename)

        for ru in annoelt.all('unit'):
            u = Record('unit')
            if common(ru, u):
                continue
            u.startPos = int(ru.positioning.start.singlePosition.index)
            u.endPos = int(ru.positioning.end.singlePosition.index)
            self.units.append(u)

        # Make sure they're sorted
        self.units = sorted(self.units, key=lambda x:x.endPos)

        for rr in annoelt.all('relation'):
            r = Record('relation')
            if common(rr, r):
                continue
            r.nodes = list(nid(t.id) for t in rr.positioning.all('term'))
            self.relations.append(r)
            
        for rs in annoelt.all('schema'):
            s = Record('schema')
            if common(rs, s):
                continue
            s.nodes = list(nid(t.id) for t in chain(
                rs.positioning.all('embedded-unit'),
                rs.positioning.all('embedded-relation'),
                rs.positioning.all('embedded-schema')
                ))
            self.schemas.append(s)

        # Annotation parsing completed
        self.delta += 1

    # Generate links between units
    def gen_struct(self):
        self.elements = dict()
        for e in chain(self.units, self.relations, self.schemas):
            self.elements[e.id] = e
            
        for r in self.relations:
            r.args = list()
            for nord, nid in enumerate(r.nodes):
                n = self.elements[nid]
                n.inRelation.append(r)
                n.ordRelation[r.id] = nord
                r.args.append(n)
            del r.nodes
        for s in self.schemas:
            s.args = list()
            for nid in s.nodes:
                n = self.elements[nid]
                n.inSchema.append(s)
                s.args.append(n)
            del s.nodes

    # Testing phase (currently, no problem)
    def gen_full_struct(self):
        self.gen_struct()
        # Already sorted
        self.segments = list(u for u in self.units if u.type == 'Segment')
        for n, ns, ng in (('dialogue', 'dialogues', 'Dialogue'),
                          ('turn', 'turns', 'Turn')):
            boxlis = list(u for u in self.units if u.type == ng)
            setattr(self, ns, boxlis)
            for u in self.segments:
                try:
                    box = next(b for b in boxlis if (b.endPos+2 >= u.endPos))
                except StopIteration:
                    print('Warning out-box', annoname)
                setattr(u, n, box)
                getattr(box, 'units').append(u)
        for d in self.dialogues:
            tlis = dict((u.turn.id, u.turn) for u in d.units).values()
            d.turns = sorted(tlis,
                key = lambda x:x.endPos)
    
    def convert_dt(self):
        """ DT conversion (replaces CDU with heads in relations) """
        def segs(e):
            if e.type == 'Complex_discourse_unit':
                return [x for a in e.args for x in segs(a)]
            else:
                return [e]
        def na(a):
            return sorted(segs(a), key=lambda x:x.startPos)[0]
        
        for r in self.relations:
            r.args = list(map(na, r.args))     
    
    def load_text(self, fname):
        """ Loads raw text (.ac) """
        
        with open(fname, encoding='utf-8') as f:
            self.raw = f.read()
    
    def load_parsed(self, fname):
        self.parsed = ParsedText(fname)
        self.parsed.fit(self)
    
    def text(self, unit):
        return self.raw[unit.startPos:unit.endPos]
    
class Record:
    def __init__(self, t):
        self._t = t
    
    def __getattr__(self, name):
        if name == 'units':
            self.units = list()
        elif name == 'text':
            return self._base.text(self)
        elif name in self.features:
            return self.features[name]
        else:
            return None
        return getattr(self, name)
    
    def __hash__(self):
        return self.id.__hash__()
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __len__(self):
        return self.endPos - self.startPos
    
    def __contains__(self, other):
        """ More of an overlap, really """
        return (2*(min(self.endPos, other.endPos)
                - max(self.startPos, other.startPos))
                > min(len(self), len(other)))

# It's a text, but with lemmas !        
class ParsedText:
    """ Holds text with Stanford XML data """
        
    def __init__(self, annofilename):
        """ Class initialiser
        
        annofilename : filename with XML data
        """
        self.tokens = list()
        self.sen_ids = [0]
        annoelt = nxml.load(annofilename)
        for s in annoelt.document.sentences.all('sentence'):
            for t in s.tokens.all('token'):
                d = tuple(self.unescape(t.one(n)._val()) for n in
                    ('word','lemma'))
                self.tokens.append(d)
            self.sen_ids.append(len(self.tokens))
    
    def fit(self, anno):
        """ Fit text to segments """
        # Use step search add
        segs = iter(sorted(list(s for s in anno.units if s.type == 'Segment'),
            key = lambda x:x.endPos))
        edus = list()
        i_low = 0
        try:
            c_seg = next(segs)
        except StopIteration:
            print('No segments ???', anno.annoname)
            return
        c_text = c_seg.text
        for i, t in enumerate(self.tokens):
            #~ print('Looking for', t)
            if c_seg is None:
                break
            while True:
                tr = re.escape(t[0])
                m = re.search(tr, c_text)
                if m:
                    # Token found, continue
                    c_text = c_text[m.end():]
                    break
                elif i_low < i:
                    # Not found, close edu and try again
                    edus.append((c_seg.id, i_low, i))
                    try:
                        c_seg = next(segs)
                        c_text = c_seg.text
                        i_low = i
                    except StopIteration:
                        c_seg = None
                        break
                else:
                    # Not found, but attach to previous edu and continue
                    # WARNING : supposes that not found tokens are not alone...
                    #~ print(t[0])
                    if edus:
                        pid, pl, ph = edus.pop()
                        edus.append((pid, pl, ph+1))
                        i_low += 1
                    break
        if c_seg is not None:
            edus.append((c_seg.id, i_low, len(self.tokens)))
        self.edus = dict()
        for i, l, h in edus:
            self.edus[i] = slice(l,h)
        
    def sentences(self):
        """ Token lists of sentences, in order """
        for i,j in zip(self.sen_ids[:-1], self.sen_ids[1:]):
            yield self.tokens[i:j]
            
    def tlist(self, e):
        """ Token list of an element """
        return self.tokens[self.edus[e.id]]
    
    def unescape(self, s):
        """ Convert those pesky PTB3 tokens """
        esc = (('-RRB-', ')'), ('-LRB-', '('))
        ns = s
        for exp, trad in esc:
            ns = re.sub(exp, trad, ns)
        return ns
    
    
# Builds a Commitment unit xml.Element
# REPLACED BY nmxl.build (see interact.py for Commitment template)
# Data comes from rules
# The element is destined to be added to blank annotations for evaluation purposes         

def build_anno_commitment(data, pos):
    global auto_id
    e = ET.Element('unit')
    e.set('id', 'jperret_auto_{0}'.format(auto_id))
    auto_id += 1

    meta = (('author','jperret_auto'),
            ('creation-date','-1'),
            ('lastModifier','n/a'),
            ('lastModificationDate','0'))
    em = ET.SubElement(e, 'metadata')
    for n, v in meta:
        eme = ET.SubElement(em, n)
        eme.text = v
    ec = ET.SubElement(e, 'characterisation')
    ect = ET.SubElement(ec, 'type')
    ect.text = 'Commitment'
    ecf = ET.SubElement(ec, 'featureSet')
    for n, v in data.items():
        ecfe = ET.SubElement(ecf, 'feature', name=n)
        ecfe.text = v
    ecp = ET.SubElement(e, 'positioning')
    for n, v in pos.items():
        ecpe = ET.SubElement(ecp, n)
        ecpes = ET.SubElement(ecpe, 'singlePosition', index=v)
        
    return e

if __name__ == '__main__':
    pa = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game2/unannotated/s1-league1-game2_06.aa'
    pr = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game2/unannotated/s1-league1-game2_06.ac'
    pp = '/home/arthur/These/Master/Stac/data/socl-season1/s1-league1-game1/parsed/stanford-corenlp/s1-league1-game1_14.xml'

    an = Annotations(pa)
    an.load_text(pr)
    an.gen_full_struct()
    
    okc = 0
    for t in an.turns:
        for s in an.segments:
            if (s in t) != (s in t.units):
                print("Anomaly")
                print(s.text)
                print(t.text)
            else:
                okc += 1

    #~ pt = ParsedText(pp)    
    #~ pt.fit(an)
    #~ 
    #~ segs = (u for u in an.units if u.type=='Segment')
#~ 
    #~ for s in segs:
        #~ i = pt.edus[s.id]
        #~ p = ' '.join([t[1] for t in pt.tokens[i]])
        #~ 
        #~ print(s.text)
        #~ print(p)
        #~ print()
