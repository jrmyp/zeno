# New master script for commitment stuff

from __future__ import print_function
import sys
import os
import annodata as ad
import classify as cs
from collections import defaultdict

print("Warning : Commitment annotations may not match up-to-date segmentation")

# Glozz data source
sroot = '/home/arthur/These/Master/Stac/data/socl-season1'
stages = ('SILVER', 'bronze', 'Bronze', 'BRONZE')
oracle_nc = 26  # Number of game parts with Commitment

# Orange data sources
fsing = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-05-01/socl-season1.just-edus.csv'
fpair = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-05-01/socl-season1.relations.csv'
fcomm = '/home/arthur/These/Data/socl-season1.custom-edus.tab'
#~ fmerge = '/home/arthur/These/Data/socl-season1.merged.csv'
fmerge = '/home/arthur/These/Data/socl-season1.merged.tab'
fturns = '/home/arthur/These/Data/socl-season1.turns2.tab'

# Features to use
feat_sel = ['word_first','word_last','has_player_name_exact','has_player_name_fuzzy','has_emoticons','is_emoticon_only','speaker_started_the_dialogue','speaker_already_spoken_in_dialogue','speakers_first_turn_in_dialogue','position_in_dialogue','edu_position_in_turn','ends_with_bang','ends_with_qmark','num_tokens','lex_domain_ressource_sheep','lex_domain_ressource_wood','lex_domain_ressource_wheat','lex_domain_ressource_ore','lex_domain_ressource_clay','lex_robber_robber','lex_trade_VBEchange_receivable','lex_trade_VBEchange_givable','lex_trade_VBEchange_mixte','lex_dialog_politesse','lex_dialog_acceptation','lex_opinion_opinionPos','lex_opinion_opinion???','lex_opinion_opinionNeg','lex_opinion_preference','lex_modifier_negation','lex_modifier_modal','lex_pronoun_pronoun_1','lex_pronoun_pronoun_3','lex_pronoun_pronoun_2','lex_pronoun_pronoun_1poss','lex_pronoun_pronoun_2poss','lex_pronoun_pronoun_3poss','lex_question_what','lex_question_who','lex_question_when','lex_question_how','lex_question_where','lex_question_why','lex_ref_pronomAI','lex_ref_quantifieur','lex_ref_pronomJoueurs','lemma_subject','has_FOR_np','is_commitment']
# Restricted set
#~ feat_sel = ['word_first','word_last','has_player_name_exact','has_player_name_fuzzy','has_emoticons','is_emoticon_only','speaker_started_the_dialogue','speaker_already_spoken_in_dialogue','speakers_first_turn_in_dialogue','position_in_dialogue','edu_position_in_turn','ends_with_bang','ends_with_qmark','num_tokens','lex_domain_ressource_sheep','lex_domain_ressource_wood','lex_domain_ressource_wheat','lex_domain_ressource_ore','lex_domain_ressource_clay','lemma_subject','has_FOR_np','is_commitment']
meta_sel = ['id', 'turn_id', 'dialogue', 'start']

def is_commitment(s, clist):
    """ Is this Segment a Commitment too ?
        s : test Segment
        clist : list of Commitement units
    """
    return any((s in c) for c in clist)

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

e_t = cs.TabData(fsing)

def gsname(row):
    """ Returns game section name from dialogue id """
    return '_'.join(row['dialogue'].value.split('_',2)[:2])

snames = set(map(gsname, e_t.t))
# Keep rows with Commitment annotations
e_t.sel_row_by(lambda r: gsname(r) in all_anno)

c_feat = (('is_commitment', 'd', 'class'),
          ('id', 'd', 'meta'),
          ('turn_id', 'd', 'meta'))
          
def g_feat():
    for name, anno in all_anno.items():
        if name not in snames:
            continue
        cl = list(u for u in anno.units if u.type == 'Commitment')
        for seg in anno.segments:
            yield (is_commitment(seg, cl),
                   '_'.join((name, 'units', seg.oid)),
                   '_'.join((name, seg.turn.oid)))

c_t = cs.custom(c_feat, g_feat())
c_t.merge(e_t)
c_t.sel_col(feat_sel, meta_sel, 'is_commitment')

c_t.t.save(fturns)

