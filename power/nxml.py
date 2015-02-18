# Wrapping around xml module
# I guess it's simpler that way...

import xml.etree.ElementTree as ET

def load(filename):
    return Element(ET.parse(filename).getroot())

class Element:
    def __init__(self, src):
        self.src = src
        
    def one(self, name):
        if name in self.src.attrib:
            return self.src.attrib[name]
        r = self.src.find(name)
        if r is not None:
            return Element(r)
        
    def all(self, name):
        return (Element(e) for e in self.src.findall(name))
        
    def _name(self):
        return self.src.tag
        
    def _val(self):
        if len(self.src) > 0:
            return (Element(e) for e in self.src)
        return self.src.text
        
    def __getattr__(self, name):
        return self.one(name)

def build(source):
    if len(source) == 3:
        n, a, s = source
    else:
        (n, s), a = source, {}
    res = ET.Element(n, dict((k, str(v)) for k,v in a.items()))
    if isinstance(s, list):
        res.extend([build(se) for se in s])
    else:
        res.text = str(s)
    return res

def add_elements(base, target, elements):
    """ Create XML target file using :
        base (str) : XML unannotated source
        target (str) : XML result filename   
        elements (list(ET.Element)) : XML elements to add
    """
    
    source = ET.parse(base).getroot()
    source.extend(elements)
    ET.ElementTree(source).write(target, encoding='utf-8', xml_declaration=True)
