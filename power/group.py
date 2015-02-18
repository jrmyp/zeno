# Group relations in clusters...

import re

#~ frel = '/home/arthur/These/Master/Stac/data/EVAL/2014-06-11/all.relations.csv'
frel = '/home/arthur/These/Master/Stac/data/EVAL/2014-06-11/socl-season1.relations.csv'
fout = '../res/grouped.csv'
#~ fout = '../res/minigrouped.csv'

grp = dict([
    ('Question-answer_pair','Question-answer_pair'),
    ('Acknowledgement','Acknowledgement'),
    ('Q-Elab','Q-Elab'),
    ('Comment','Comment'),
    ('Alternation','Alternation'),
    ('Conditional','Result'),
    ('Clarification_question','Q-Elab'),
    ('Continuation','Result'),
    ('Contrast','Contrast'),
    ('Elaboration','Elaboration'),
    ('Result','Result'),
    ('Parallel','Result'),
    ('Narration','Result'),
    ('Explanation','Elaboration'),
    ('Correction','Elaboration'),
    ('Background','Result'),
    ('UNRELATED','UNRELATED')
])

with open(frel) as f_in, open(fout, 'w') as f_out :
    first = True
    for line in f_in:
        if first:
            f_out.write(line)
            first = False
            continue
        reln = re.match('([^,]+),', line).group(1)
        f_out.write(re.sub(reln, grp[reln], line))

