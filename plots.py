# Histograms !

# One with... number of EDU by dialogue ? Done
# One with... distance between linked EDUs
import re
import Orange
import matplotlib.pyplot as plt
from itertools import chain
from collections import defaultdict

f_source = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-04-10/tmp/socl-season1.relations.csv'
d_full = Orange.data.Table(f_source)
d_source = d_full.filter({'CLASS':'UNRELATED'}, negate=1)

#~ print(d_source.domain)

# EDU between cumulative counting (works)
#~ ig = d_source.domain.index('num_edus_between')
#~ counts = defaultdict(lambda : 0)
#~ for line in d_source:
    #~ counts[int(line[ig].value)] += 1
#~ 
#~ s = 0
#~ print(len(d_source))
#~ for i in range(15):
    #~ s += counts[i]
    #~ print(i, counts[i], s, float(s)/len(d_source))

# Count checking (it worked)
#~ ig = d_source.domain.index('dialogue')
#~ counts = defaultdict(lambda : 0)
#~ 
#~ for line in d_source:
    #~ counts['_'.join(re.split('_',line[ig].value)[:2])] += 1
    #~ 
#~ for k,v in counts.items():
    #~ print v, k

# Edus between
#~ ig = d_source.domain.index('num_edus_between')
#~ counts = defaultdict(list)
#~ for line in d_source:
    #~ counts[line.getclass().value].append(1+int(line[ig].value))
#~ 
#~ la = counts['Question-answer_pair']
#~ lb = counts['Comment']
#~ ex = {'Question-answer_pair', 'Comment','UNRELATED'}
#~ ex2 = {'UNRELATED'}
#~ lc = list(chain.from_iterable(counts[e] for e in counts if e not in ex))
#~# lc = list(chain.from_iterable(counts[e] for e in counts if e not in ex2))
#~ 
#~ plt.hist((la,lb,lc), color=('red', 'green', 'blue'), label=('QAP','Comment','Others'), stacked=True, bins=range(7), align='left')
#~# plt.hist(lc, bins=range(7), align='left')
#~ 
#~ plt.xlabel("Distance between EDUs")
#~ plt.ylabel("Frequency")
#~ plt.legend()
#~ plt.show()

# Relation count
counts = defaultdict(lambda : 0)
for line in d_source:
    counts[line.getclass().value] += 1

print sum(counts.values())
for l, s in sorted(counts.items(), key=lambda x:x[1],reverse=True):
    print('{0:25}: {1}'.format(l, s))


# Number of EDUs by dialogue
#~ ig, iu, iv = (d_source.domain.index(e)
    #~ for e in ('dialogue','id_DU1','id_DU2'))
#~ counts = defaultdict(set)    
#~ for line in d_source:
    #~ counts[line[ig].value] |= {line[iu].value, line[iv].value}
#~ 
#~ nums = list(len(e) for e in counts.values())
#~ 
#~ plt.hist(nums, bins=range(0,60,5))
#~ plt.xlabel("Number of EDUs in dialogue")
#~ plt.ylabel("Frequency")
#~ plt.show() 
