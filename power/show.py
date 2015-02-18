# Simply output dialogues... from a list

import sys
import os
import annodata as ad
from collections import defaultdict
from ast import literal_eval as leval

name_src = '../struct/conf/names_col.txt' 
num_src = [242, 407, 317, 5, 181, 324, 199, 45, 273, 263, 221, 164, 40, 123, 331, 174, 193, 60, 6, 318, 180, 235, 124, 302, 25, 287, 171, 209, 79, 110, 106, 355, 112, 4, 169, 404, 389, 401, 339, 313, 366, 326, 126, 380, 29, 397, 332, 321, 154, 177, 184, 50, 150, 134, 178, 315, 98, 200, 316, 163, 136, 170, 310, 159, 239, 144, 161, 33, 62, 139, 341, 42, 130, 224, 306, 28, 151, 250, 335, 279, 96, 119, 145, 241, 196, 165, 168, 237, 344, 3, 368, 54, 0, 330, 381, 188, 173, 85, 342, 402, 116, 138, 357, 114, 408, 102, 347, 272, 299, 229, 337, 222, 93, 259, 246, 333, 280, 270, 231, 277, 274, 328, 8, 243, 61, 148, 300, 101, 158, 294, 286, 179, 76, 376, 220, 383, 121, 211, 127, 285, 296, 26, 152, 122, 20, 192, 329, 146, 44, 247, 59, 108, 13, 100, 265, 80, 89, 364, 109, 382, 305, 72, 348, 278, 92, 212, 115, 172, 261, 409, 320, 291, 398, 176, 129, 37, 187, 214, 303, 309, 97, 281, 375, 390, 99, 15, 64, 107, 7, 234, 207, 218, 48, 367, 396, 69, 394, 175, 377, 271, 276, 203, 253, 258, 356, 386, 201, 217, 167, 288, 249, 18, 120, 9, 304, 370, 395, 334, 245, 47, 12, 58, 293, 301, 204, 289, 248, 35, 410, 346, 244, 194, 325, 87, 257, 360, 358, 215, 371, 23, 83, 198, 353, 1, 388, 323, 406, 387, 213, 267, 66, 311, 77, 117, 166, 363, 297, 75, 149, 206, 264, 298, 400, 195, 52, 128, 36, 327, 365, 290, 32, 362, 38, 111, 143, 30, 228, 275, 374, 205, 252, 373, 255, 185, 268, 392, 340, 88, 350, 208, 292, 140, 183, 312, 232, 84, 156, 63, 135, 379, 118, 95, 191, 391, 256, 233, 14, 70, 307, 190, 19, 24, 352, 105, 43, 254, 354, 295, 189, 160, 65, 137, 349, 103, 361, 74, 53, 319, 322, 369, 251, 182, 262, 202, 81, 27, 132, 21, 31, 56, 147, 385, 155, 17, 405, 71, 51, 223, 269, 266, 282, 210, 125, 314, 230, 384, 238, 90, 49, 22, 283, 399, 351, 359, 260, 133, 41, 67, 157, 73, 131, 308, 345, 82, 16, 113, 91, 284, 68, 142, 343, 378, 219, 57, 236, 162, 46, 338, 2, 55, 104, 227, 403, 393, 78, 240, 225, 226, 153, 39, 10, 94, 372, 336, 197, 11, 216, 86, 34, 141, 186]

sroot = '/home/arthur/These/Master/Stac/data'
seasons = ('socl-season1',)
stages = ('GOLD', 'SILVER', 'bronze', 'Bronze', 'BRONZE')

# The great big loop for retrieving all annotations
# Someday, I'll simplify this, there are redundancies...
def g_n():
    # Season loop
    for sname in seasons:
        # Game loop
        for gname in os.listdir(os.path.join(sroot, sname)):
            if gname.startswith(('s1','s2','pilot')):
                p0 = os.path.join(sroot, sname, gname)
                if 'discourse' in os.listdir(p0):
                    p1 = os.path.join(p0, 'discourse')
                    # Stage loop
                    for tname in stages:
                        if tname in os.listdir(p1):
                            p2 = os.path.join(p1, tname)
                            if not os.listdir(p2):
                                continue
                            # Annotation file loop
                            for fname in os.listdir(p2):
                                if fname.endswith('.aa'):
                                    bname = fname[:-3]
                                    a = ad.Annotations(os.path.join(p2, fname))
                                    a.gen_full_struct()
                                    a.load_text(os.path.join(p0, 'unannotated', bname+'.ac'))
                                    yield bname, a
                            # Only check first found stage
                            break

all_anno = dict()
for i, pair in enumerate(g_n()):
    n, anno = pair
    all_anno[n] = anno
    print('Loading ({0}/{1}) : {2}\r'.format(i+1, '???', n), end='')
    #~ sys.stdout.flush()
print('\nAnnotations loaded')

#~ ndl = list()
#~ for anno in all_anno.values():
    #~ su = sum(len(d.units) for d in anno.dialogues)
    #~ sd = len(anno.segments)
    #~ su = len(set(u.dialogue.id for u in anno.units))
    #~ sd = len(anno.dialogues) 
    #~ ndl.append((su, sd))
#~ print(ndl)
#~ print()
#~ sys.exit()

def sid(e):
    l = e.split('_')
    return tuple('_'.join(pl) for pl in (l[:2], l[3:]))

def rline(l):
    return leval(l[:-1])
    
with open(name_src) as fn:
    d = rline(next(fn))
    dr = [d[num_src[i]] for i in range(100)]
    ids = list(map(sid, dr))

#~ print(ids[:5])
#~ sys.exit()

k = 0
#~ posl = defaultdict(list)
for doc, eid in ids:
    fu = all_anno[doc].elements[eid]
    dia = fu.dialogue
    #~ posl[doc+'_'+dia.id].append((dia.units.index(fu)+1, eid))
    print('#{2} - {0} - {1}'.format(doc, dia.id, k))
    for t in dia.turns:
        print(t.text)
    k += 1
    print()

#~ for k, v in posl.items():
    #~ if len(v) > 1:
        #~ print(k, v)
