# Data holders for Glozz annotation files

# TODO : Correct those gorram ids...
#   Done ?

import xml.etree.ElementTree as ET
import nxml
from itertools import chain

auto_id = 0

class Annotations:
    def __init__(self, baseanno=None):
        # Discriminating id suffix for annotation groups
        self.delta = 0
        
        self.ids = set()
        self.units = list()
        self.relations = list()
        self.schemas = list()
        if baseanno is not None:
            self.load_anno(baseanno)
    
    def load_anno(self, annofilename):
        def nid(id):
            return "{0}_{1}".format(id, self.delta)
        
        def common(src, tgt):
            tgt._base = self
            tgt.id = nid(src.id)
            cr = src.characterisation
            tgt.type = cr.type._val()
            tgt.features = dict((f.name, f._val()) for f in cr.featureSet.all('feature'))
            tgt.inRelation = list()
            tgt.ordRelation = dict()
            tgt.inSchema = list()
            return (tgt.id in self.ids)

        annoelt = nxml.load(annofilename)

        for ru in annoelt.all('unit'):
            u = Record('unit')
            if common(ru, u):
                continue
            u.startPos = int(ru.positioning.start.singlePosition.index)
            u.endPos = int(ru.positioning.end.singlePosition.index)
            self.units.append(u)

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
            s.nodes = list(nid(t.id) for t in rs.positioning.all('embedded-unit'))
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
                n.inSchema.append(r)
                s.args.append(n)
            del s.nodes
        
    def gen_turns(self):
        self.gen_struct()
        
        # Filter turns with the same identifier
        turns = dict((e.Identifier, e) for e in self.units if e.type == 'Turn')
        # List of unique turns, sorted by position
        self.turns = sorted(turns.values(), key=lambda t: t.endPos)
        ignore = 'paragraph Dialogue Turn'.split(' ')

        # Collect units included in turns
        for u in self.units:
            if u.type in ignore:
                continue
            turn = next(t for t in self.turns if (t.endPos >= u.endPos))
            u.turn = turn
            u.emitter = turn.features['Emitter']
            turn.units.append(u)
    
    # Very similar to gen_turns... may factor someday
    def gen_dialogues(self):
        self.gen_struct()
        
        self.dialogues = sorted((e for e in self.units if e.type == 'Dialogue'), key=lambda t:t.endPos)
        for u in self.units:
            if u.type != 'Segment':
                continue
            dia = next(d for d in self.dialogues if (d.endPos >= u.endPos))
            u.dialogue = dia
            dia.units.append(u)
        
    def load_text(self, fname):
        with open(fname) as f:
            self.raw = f.read()
    
    def text(self, unit):
        return self.raw[unit.startPos:unit.endPos]

    #~ def display(self, element, indent=0):
        #~ print(' '*indent, end='')
        #~ if(element._t == 'unit'):
            #~ print('unit ({0}) {1} : {2}'.format(element.type, element.emitter, element.text))
        #~ else:
            #~ print('{1} ({0}):'.format(element.type, element._t))
            #~ for e in element.args:
                #~ self.display(e, indent+4)
    
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

    def __eq__(self, other):
        return self.id == other.id
        
# Builds a Commitment unit xml.Element
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

# Create XML target file using :
#   base : XML unannotated source
#   elements : XML elements to add
def add_elements(base, target, elements):
    source = ET.parse(base).getroot()
    source.extend(elements)
    ET.ElementTree(source).write(target, encoding='utf-8')

