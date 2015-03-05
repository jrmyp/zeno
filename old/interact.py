# Interactive annotations
# If this works, I think I'll promote it
# Time is running out. Can't continue for now :(

# NEXT : ability to edit existing annos...
#   Seconded by myself, would save much, much time

# Python 3. NOT Python 2.
import sys
import os
import re
#~ import pickle as pk

import nxml
import annodata as ad

inc = re.compile('(wheat|ore|sheep|clay|wood) (\d+|inf) (\d+|inf)')
inc2 = re.compile('(some|no) (wheat|ore|sheep|clay|wood)')

class Conf:
    """ Config state """
    
    def __init__(self, name, src, i=0):
        """ Class initialiser """
        self.name = name
        self.src = src
        self.i = int(i)
        
    def id(self):
        self.i += 1
        return '{0}_{1:04}'.format(self.name, self.i-1)

    def display(self):
        print('Annotator : ', self.name)
        print('Data path : ', self.src)
        print('Start id : ', self.i)

    @classmethod
    def load(cls, fn):
        """ Load config from file """
        with open(fn, 'r') as f:
            s = f.read()
        return cls(*(s.split('\n')[:3]))
    
    def save(self, fn):
        """ Save config in file """
        with open(fn, 'w') as f:
            for e in (self.name, self.src, self.i):
                f.write(str(e)+'\n')

seasons = ('socl-season1','socl-season2','pilot')

def load_anno(cf, name):
    # Season loop
    for sname in seasons:
        # Game loop
        for gname in os.listdir(os.path.join(cf.src, sname)):
            if gname == name:
                p0 = os.path.join(cf.src, sname, gname)
                pc = os.path.join(p0,'commitment')
                if 'commitment' not in os.listdir(p0):
                    os.mkdir(pc)
                if cf.name not in os.listdir(pc):
                    os.mkdir(os.path.join(pc, cf.name))
                for fname in sorted(os.listdir(os.path.join(p0, 'unannotated'))):
                    if fname.endswith('.aa'):
                        bname = fname[:-3]
                        base = os.path.join(p0, 'unannotated', fname)
                        a = ad.Annotations(base)
                        a.gen_turns()
                        a.load_text(os.path.join(p0, 'unannotated', bname+'.ac'))
                        yield a, base, os.path.join(p0, 'commitment', cf.name, fname)
                break
        else:
            continue
        break
    else:
        print('Game not found :', name)

def creation(anno):
    for s in anno.segments:
        #~ kay = s.turn.text
        #~ print(kay)
        print('T : {0}'.format(s.turn.text))
        print('S : {0}'.format(s.text))
        while True:
            try:
                c = input('> ')
            except EOFError:
                print()
                raise StopIteration
            if not c:
                break
            m = inc.match(c)
            m2 = inc2.match(c)
            if m or m2:
                if m:
                    vals = (re.sub('inf', 'infinity', e) for e in m.groups())
                elif m2.group(1) == 'no':
                    vals = (m2.group(2), '0', '0')
                else:
                    vals = (m2.group(2), '1', 'infinity')
                feats = zip(('Resource', 'Lower_bound', 'Upper_bound'), vals)
                yield s, feats
            elif m2:
                has, rn = m.groups()
                
            else:
                print('Invalid input')

def g_comm(cf, data):
    seg, feats = data
    nid = cf.id()
    meta = [('author', cf.name),
            ('creation-date',nid[-4:]),
            ('lastModifier', 'n/a'),
            ('lastModificationDate','0')]
    pos = [('start',seg.startPos), ('end',seg.endPos)]
    src = ('unit', {'id':nid}, [
        ('metadata', list(meta)),
        ('characterisation', [
            ('type', 'Commitment'),
            ('featureSet', list(
                ('feature', {'name':n}, v) for n,v in feats
            )),
        ]),
        ('positioning', list(
             (n,[('singlePosition', {'index':v}, [])]) for n,v in pos
        ))
    ])
    return nxml.build(src)

if __name__ == '__main__':
    
    cfn = 'inter/user.conf'
    # Uncomment to reinitialize
    #~ cf = Conf('jperret_2','/home/arthur/These/Master/Stac/data/', 18)
    #~ cf.save(cfn)
    
    cf = Conf.load(cfn)
    cf.display()
    
    print('Please enter a game name to annotate')
    n = input('> ')
    ns = re.match('(\d+) (\d+) (\d+)', n)
    if ns:
        n = 's{0}-league{1}-game{2}'.format(*ns.groups())
    for anno, basepath, respath in load_anno(cf, n):
        print('\nNow annotating {0}'.format(os.path.basename(basepath)))            
        try:
            input('Press Enter to continue, Ctrl-D to abort')
        except EOFError:
            print()
            break

        if os.path.exists(respath):
            try:
                r = input('An annotation file already exists. Overwrite ? ')
                if r.startswith(('n', 'N')):
                    continue
            except EOFError:
                print()
                break
            
        with open('inter/help.txt', 'w', encoding='utf-8') as f:
            for d in anno.dialogues:
                for t in d.turns:
                    f.write(t.text)
                    f.write('\n')
                f.write('\n')
        print('File help.txt generated\n')
        nxml.add_elements(basepath, respath, list(
            g_comm(cf, data) for data in creation(anno)))

    cf.save(cfn)
