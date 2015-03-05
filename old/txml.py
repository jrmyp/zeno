# nxml experiences...

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
    res = ET.Element(n, a)
    if isinstance(s, list):
        res.extend([build(se) for se in s])
    else:
        res.text = str(s)
    return res

if __name__ == '__main__':
    target = 'res/res.xml'
    meta = {'author':'me'}
    feat = {'no':3, 'yes':4}
    pos = {'start':1, 'end':2}
    src = ('unit', [
        ('metadata', list(meta.items())),
        ('characterisation', [
            ('type', 'commitment')
        ]),
        ('featureSet', list(
            ('feature', {'name':n}, v) for n,v in feat.items()
        )),
        ('positioning', list(
             (n,[('singlePosition', v)]) for n,v in pos.items()
        ))
    ])
    e = build(src)
    ET.ElementTree(e).write(target, encoding='utf-8')
