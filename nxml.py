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

