# Commitment master script
# Python 2

from __future__ import print_function
import sys
import os
import Orange
import annodata as ad
from collections import defaultdict
from valmerger import gen_vm

print("Warning : Commitment annotations may not match up-to-date segmentation")

"""
Step 1 == DONE
Create domain with :
    commitment as class
    attelo unit id as meta
Fill it with data from Glozz
Create domain with :
    ... no, just let it as it is
Merge the two tables
There you go


Step 2 == DONE
Goal : Merge rows from same turn
Get list of features
Create config for merging features
    first ?
    mean, mix, max ?
    or, and ?
    reduce it to a lambda anyway
    create dict(feature, reducer)
Create new table with these merged rows
Profit

"""

# Glozz data source
sroot = '/home/arthur/These/Master/Stac/data/socl-season1'
stages = ('SILVER', 'bronze', 'Bronze', 'BRONZE')
oracle_nc = 26  # Number of game parts with Commitment

# Orange data sources
fsing = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-05-01/socl-season1.just-edus.csv'
fpair = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-05-01/socl-season1.edu-pairs.csv'
fcomm = '/home/arthur/These/Data/socl-season1.custom-edus.tab'
#~ fmerge = '/home/arthur/These/Data/socl-season1.merged.csv'
fmerge = '/home/arthur/These/Data/socl-season1.merged.tab'
fturns = '/home/arthur/These/Data/socl-season1.turns.tab'

# Features to use
feat_sel = ['word_first','word_last','has_player_name_exact','has_player_name_fuzzy','has_emoticons','is_emoticon_only','speaker_started_the_dialogue','speaker_already_spoken_in_dialogue','speakers_first_turn_in_dialogue','position_in_dialogue','edu_position_in_turn','ends_with_bang','ends_with_qmark','num_tokens','lex_domain_ressource_sheep','lex_domain_ressource_wood','lex_domain_ressource_wheat','lex_domain_ressource_ore','lex_domain_ressource_clay','lex_robber_robber','lex_trade_VBEchange_receivable','lex_trade_VBEchange_givable','lex_trade_VBEchange_mixte','lex_dialog_politesse','lex_dialog_acceptation','lex_opinion_opinionPos','lex_opinion_opinion???','lex_opinion_opinionNeg','lex_opinion_preference','lex_modifier_negation','lex_modifier_modal','lex_pronoun_pronoun_1','lex_pronoun_pronoun_3','lex_pronoun_pronoun_2','lex_pronoun_pronoun_1poss','lex_pronoun_pronoun_2poss','lex_pronoun_pronoun_3poss','lex_question_what','lex_question_who','lex_question_when','lex_question_how','lex_question_where','lex_question_why','lex_ref_pronomAI','lex_ref_quantifieur','lex_ref_pronomJoueurs','lemma_subject','has_FOR_np','is_commitment']
#~ feat_sel = ['word_first','word_last','has_player_name_exact','has_player_name_fuzzy','has_emoticons','is_emoticon_only','speaker_started_the_dialogue','speaker_already_spoken_in_dialogue','speakers_first_turn_in_dialogue','position_in_dialogue','edu_position_in_turn','ends_with_bang','ends_with_qmark','num_tokens','lex_domain_ressource_sheep','lex_domain_ressource_wood','lex_domain_ressource_wheat','lex_domain_ressource_ore','lex_domain_ressource_clay','lemma_subject','has_FOR_np','is_commitment']

def is_commitment(s, clist):
    """ Is this Segment a Commitment too ?
        s : test Segment
        clist : list of Commitement units
    """
    return any((s in c) for c in clist)

def gen_tab_header(table):
    def tri(f, tag):
        return (f.name, str(f.var_type)[0].lower(), tag)
        
    d = table.domain
    # ff : list of (name, c/d, meta/class/'')
    ff = ([tri(d.class_var, 'class')] +
          [tri(f, 'meta') for f in d.get_metas().values()] +
          [tri(f, '') for f in d.attributes])
    # Header, on 3 lines (Orange tab format)
    h = '\n'.join('\t'.join([t[k] for t in ff]) for k in range(3))+'\n'
    # Feature name list, in order
    fl = list(t[0] for t in ff)
    return h, fl

##### Part 0 : data gathering #####

def g_n():
    """ Iterates on all files annotated with Commitment
        Yields annotation objects
    """
    for gname in os.listdir(sroot):
        if gname.startswith('s1'):
            p0 = os.path.join(sroot, gname)
            if 'commitment' in os.listdir(p0):
                p1 = os.path.join(p0, 'commitment')
                for fname in os.listdir(p1):
                    if fname.endswith('.aa'):
                        bname = fname[:-3]
                        #~ if bname == 's1-league1-game2_07':
                        a = ad.Annotations(os.path.join(p1, fname))
                        a.gen_full_struct()
                        yield bname, a
                            
# Without counter
#~ all_anno = dict(g_n())

# With counter
all_anno = dict()
for i, pair in enumerate(g_n()):
    n, anno = pair
    all_anno[n] = anno
    print('Loading ({0}/{1}) : {2}\r'.format(i+1, oracle_nc, n), end='')
    sys.stdout.flush()
print('\nAnnotations loaded')

#~ for n, anno in all_anno.items():
    #~ print(n)
    #~ cl = list(dict((u.startPos, u) for u in anno.units if u.type == 'Commitment').values())
    #~ print(len(cl))
    #~ print(len(list(u for u in anno.segments if is_commitment(u, cl))))
    #~ for u in anno.segments:
        #~ print(u.startPos, u.endPos)
        #~ print([(c.startPos, c.endPos) for c in u.turn.units if c.type == 'Commitment'])
    
#~ sys.exit()
all_table = d_all = Orange.data.Table(fsing)
print('Attelo data loaded')

# Select data rows with commitment annotations
#~ ind_id = all_table.domain.index('id')
ind_id = all_table.domain.index('dialogue')
# Is the game section name known ?
knames = set('_'.join(row[ind_id].value.split('_',2)[:2])
        for row in all_table)
sel = [('_'.join(row[ind_id].value.split('_',2)[:2]) in all_anno)
        for row in all_table]
d_table = all_table.select(sel)

# Build custom features (i.e. commitment)
with open(fcomm, 'w') as f:
    # Orange format header
    f.write('is_commitment\tid\tturn_id\n')
    f.write('d\td\td\n')
    f.write('class\tmeta\tmeta\n')
    for name, anno in all_anno.items():
        if name not in knames:
            continue
        cl = list(u for u in anno.units if u.type == 'Commitment')
        for seg in anno.segments:
            f.write('\t'.join((
                str(is_commitment(seg, cl)),
                '_'.join((name, 'units', seg.oid)),
                '_'.join((name, seg.turn.oid))
                )) + '\n')

c_table = Orange.data.Table(fcomm)
print('Custom data created')

###### Part 1 : Table merging ######

# Filter non-common EDUs 
ii = c_table.domain.index('id')
jj = d_table.domain.index('id')
si = set(r[ii].value for r in c_table)
ti = set(r[jj].value for r in d_table)
c_d = list(si-ti)
d_c = list(ti-si)
print('= In Commitment, not in Discourse =')
for e in c_d:
    print(e)
print('= In Discourse, not in Commitment =')
for e in d_c:
    print(e)

cf_table = c_table.filter_ref({'id':c_d}, negate=1)
df_table = d_table.filter_ref({'id':d_c}, negate=1)

#~ for n in names:
    #~ print(n, n in all_anno)
#~ for n in all_anno:
    #~ print(n, n in names)
#~ sys.exit()

mrg_table = Orange.data.Table([cf_table, df_table])
mgd = mrg_table.domain
md = Orange.data.Domain(mgd, 'is_commitment')
md = Orange.data.Domain(feat_sel, md)
# Add necessary meta information
for nm in ('id', 'turn_id', 'dialogue', 'start'):
    md.add_meta(mgd.meta_id(nm), mgd.get_meta(nm))

m_table = Orange.data.Table(md, mrg_table)
m_table.save(fmerge)
print('Data built with {0} EDUs'.format(len(m_table)))

##### Part 2 : Turn merging #####

head, fnames = gen_tab_header(m_table)
mergers = gen_vm(fnames)

# Indexes for features AND metas
#   (can't iterate easily on both at the same time)
inds = list(md.index(n) for n in fnames)

# Build turn-rows dict
tid_i = md.index('turn_id')
t_rows = defaultdict(list)
for r in m_table:
    t_rows[r[tid_i].value].append(r)

# Merge and store data
s_id = md.index('start')
with open(fturns, 'w') as f:
    f.write(head)
    for rl in t_rows.values():
        # Sort turn rows by position
        rlis = sorted(rl, key=lambda x:x[s_id].value)
        # Collect and apply mergers
        vals = [rlis[0][i].value for i in inds]
        for r in rlis[1:]:
            vals = list(m(v,r[i].value) for m,v,i in zip(mergers, vals, inds))
        f.write('\t'.join(map(str,vals))+'\n')

t_table = Orange.data.Table(fturns)
print('Row merging successful with {0} turns'.format(len(t_table)))
