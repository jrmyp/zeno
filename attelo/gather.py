# New master script for commitment stuff
# Shorter, cleaner
#   Yeah, right

from __future__ import print_function
import sys
import os
import re
import annodata as ad
import classify as cs
from collections import defaultdict

print("Warning : Commitment annotations may not match up-to-date segmentation")

# Glozz data source
sroot = '/home/arthur/These/Master/Stac/data/socl-season1'
stages = ('SILVER', 'bronze', 'Bronze', 'BRONZE', 'jperret')
#~ stages = ('SILVER', 'bronze', 'Bronze', 'BRONZE', 'sa')
oracle_nc = 62  # Number of game parts with Commitment

# Orange data sources
fsing = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-05-12/socl-season1.just-edus.csv'
fpairs = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-05-12/socl-season1.relations.csv'

# Savefiles for tables
fcomm = '/home/arthur/These/Data/socl-season1.custom-edus.tab'
fmerge = '/home/arthur/These/Data/socl-season1.merged.tab'
fturns = '/home/arthur/These/Data/socl-season1.turns.tab'
fqap = '/home/arthur/These/Data/socl-season1.qap.tab'
fxqap = '/home/arthur/These/Data/socl-season1.xqap.tab'
frqap = '/home/arthur/These/Data/socl-season1.rqap.tab'
fnsing = '/home/arthur/These/Data/socl-season1.single.tab'
ffinal = '/home/arthur/These/Data/socl-season1.final.tab'

# Features to use
#~ feat_sel = ['is_commitment','word_first','word_last','has_player_name_exact','has_player_name_fuzzy','has_emoticons','is_emoticon_only','speaker_started_the_dialogue','speaker_already_spoken_in_dialogue','speakers_first_turn_in_dialogue','position_in_dialogue','edu_position_in_turn','ends_with_bang','ends_with_qmark','num_tokens','lex_domain_ressource_sheep','lex_domain_ressource_wood','lex_domain_ressource_wheat','lex_domain_ressource_ore','lex_domain_ressource_clay','lex_robber_robber','lex_trade_VBEchange_receivable','lex_trade_VBEchange_givable','lex_trade_VBEchange_mixte','lex_dialog_politesse','lex_dialog_acceptation','lex_opinion_opinionPos','lex_opinion_opinion???','lex_opinion_opinionNeg','lex_opinion_preference','lex_modifier_negation','lex_modifier_modal','lex_pronoun_pronoun_1','lex_pronoun_pronoun_3','lex_pronoun_pronoun_2','lex_pronoun_pronoun_1poss','lex_pronoun_pronoun_2poss','lex_pronoun_pronoun_3poss','lex_question_what','lex_question_who','lex_question_when','lex_question_how','lex_question_where','lex_question_why','lex_ref_pronomAI','lex_ref_quantifieur','lex_ref_pronomJoueurs','lemma_subject','has_FOR_np']
# Restricted set
#~ feat_sel = ['word_first','word_last','has_player_name_exact','has_player_name_fuzzy','has_emoticons','is_emoticon_only','speaker_started_the_dialogue','speaker_already_spoken_in_dialogue','speakers_first_turn_in_dialogue','position_in_dialogue','edu_position_in_turn','ends_with_bang','ends_with_qmark','num_tokens','lex_domain_ressource_sheep','lex_domain_ressource_wood','lex_domain_ressource_wheat','lex_domain_ressource_ore','lex_domain_ressource_clay','lemma_subject','has_FOR_np','is_commitment']
#~ meta_sel = ['id', 'turn_id', 'dialogue', 'start']

# New sets
feat_sel = ['clue_resource','unclue_resource', 'word_first','word_last','has_player_name_exact','has_player_name_fuzzy','has_emoticons','is_emoticon_only','speaker_started_the_dialogue','speaker_already_spoken_in_dialogue','speakers_first_turn_in_dialogue','position_in_dialogue','edu_position_in_turn','ends_with_bang','ends_with_qmark','lex_domain_ressource_sheep','lex_domain_ressource_wood','lex_domain_ressource_wheat','lex_domain_ressource_ore','lex_domain_ressource_clay','lex_robber_robber','lex_trade_VBEchange_receivable','lex_trade_VBEchange_givable','lex_trade_VBEchange_mixte','lex_dialog_politesse','lex_dialog_acceptation','lex_opinion_opinionPos','lex_opinion_opinion???','lex_opinion_opinionNeg','lex_opinion_preference','lex_modifier_negation','lex_modifier_modal','lex_pronoun_pronoun_1','lex_pronoun_pronoun_3','lex_pronoun_pronoun_2','lex_pronoun_pronoun_1poss','lex_pronoun_pronoun_2poss','lex_pronoun_pronoun_3poss','lex_question_what','lex_question_who','lex_question_when','lex_question_how','lex_question_where','lex_question_why','lex_ref_pronomAI','lex_ref_quantifieur','lex_ref_pronomJoueurs','lemma_subject','has_FOR_np']
#~ feat_sel = ['clue_resource', 'word_first','word_last','has_player_name_exact','has_player_name_fuzzy','has_emoticons','is_emoticon_only','speaker_started_the_dialogue','speaker_already_spoken_in_dialogue','speakers_first_turn_in_dialogue','position_in_dialogue','edu_position_in_turn','ends_with_bang','ends_with_qmark','num_tokens','lex_domain_ressource_sheep','lex_domain_ressource_wood','lex_domain_ressource_wheat','lex_domain_ressource_ore','lex_domain_ressource_clay','lex_robber_robber','lex_trade_VBEchange_receivable','lex_trade_VBEchange_givable','lex_trade_VBEchange_mixte','lex_dialog_politesse','lex_dialog_acceptation','lex_opinion_opinionPos','lex_opinion_opinion???','lex_opinion_opinionNeg','lex_opinion_preference','lex_modifier_negation','lex_modifier_modal','lex_pronoun_pronoun_1','lex_pronoun_pronoun_3','lex_pronoun_pronoun_2','lex_pronoun_pronoun_1poss','lex_pronoun_pronoun_2poss','lex_pronoun_pronoun_3poss','lex_question_what','lex_question_who','lex_question_where','lex_question_why','lex_ref_pronomAI','lex_ref_quantifieur','lex_ref_pronomJoueurs','lemma_subject','has_FOR_np']
meta_sel = ['is_commitment', 'is_ore_c','is_wheat_c','is_sheep_c','is_wood_c','is_clay_c','id', 'turn_id', 'dialogue', 'start', 'has_res']

#~ if True:
if False:
    def is_commitment(s, clist):
        """ Is this Segment a Commitment too ?
            s : test Segment
            clist : list of Commitement units
        """
        return any((s in c) for c in clist)

    def get_commitments(s, clist):
        """ Get all commitment resources for a given Segment """
        return set(c.Resource for c in clist if (s in c))

    clue_r = re.compile('none|(i ha(ve|s)|(offer|giv)ing|no|for) ([\w\d]+ )?(clay|ore|wheat|wood|sheep)', re.I)
    def is_clue(s):
        return bool(clue_r.search(s.text))

    unclue_r = re.compile('(need|any )(?!.* for)', re.I)
    def is_unclue(s):
        return bool(unclue_r.search(s.text))

    nr_r = re.compile('(clay|ore|wheat|wood|sheep)')
    def has_nr(s):
        return bool(nr_r.search(s.text))
        
    #~ def gid(id):
        #~ """ Returns Glozz data id from table id """
        #~ return '_'.join(str(id).split('_', id)[-2:])

    def gid(id):
        """ Returns units table id from relation table id
            This is why I hate external data sources
        """
        return re.sub('discourse', 'units', str(id))

    def g_n():
        """ Iterates on all files annotated with Commitment
            Yields annotation objects
        """
        for gname in os.listdir(sroot):
            if gname.startswith('s1'):
                p0 = os.path.join(sroot, gname)
                for stage in stages:
                    p1 = os.path.join(p0, 'commitment', stage)
                    if os.path.isdir(p1):
                        for fname in os.listdir(p1):
                            if fname.endswith('.aa'):
                                bname = fname[:-3]
                                #~ if bname == 's1-league1-game2_07':
                                    #~ continue
                                a = ad.Annotations(os.path.join(p1, fname))
                                a.gen_full_struct()
                                a.load_text(os.path.join(p0, 'unannotated', bname + '.ac'))
                                yield bname, a
                        # Break on first found stage
                        break

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

    #~ e_t = cs.TabData(fsing)
    e_t = cs.TabData(fnsing)

    def gsname(row):
        """ Returns game section name from id """
        return '_'.join(row['id'].value.split('_',2)[:2])

    snames = set(map(gsname, e_t))
    # Only keep rows with Commitment annotations
    e_t.sel_row_by(lambda r: gsname(r) in all_anno)

    ######### Stat
    #~ count = defaultdict(lambda:0)
    #~ for n, a in all_anno.items():
        #~ if n not in snames:
            #~ continue
        #~ print(n)
        #~ for t in a.turns:
            #~ count[len(t.units)] += 1
    #~ print(dict(count))
    #~ sys.exit()
    #########

    c_feat = (('is_ore_c', 'd', 'meta'),
              ('is_wheat_c', 'd', 'meta'),
              ('is_sheep_c', 'd', 'meta'),
              ('is_wood_c', 'd', 'meta'),
              ('is_clay_c', 'd', 'meta'),
              ('is_commitment', 'd', 'meta'),
              #~ ('clue_ore', 'd', ''),
              #~ ('clue_wheat', 'd', ''),
              #~ ('clue_sheep', 'd', ''),
              #~ ('clue_wood', 'd', ''),
              #~ ('clue_clay', 'd', ''),
              ('clue_resource', 'd', ''),
              ('unclue_resource', 'd', ''),
              ('has_res', 'd', 'meta'),
              ('id', 'd', 'meta'),
              ('turn_id', 'd', 'meta'))

    resl = ['ore', 'wheat', 'sheep', 'wood', 'clay']

    def c_data():
        for name, anno in all_anno.items():
            if name not in snames:
                continue
            cl = list(u for u in anno.units if u.type == 'Commitment')
            # File without Commitment : skip
            # Probably game-unrelated chat
            #~ if not cl:
                #~ continue
            for seg in anno.segments:
                # is_commitment only
                #~ yield (is_commitment(seg, cl),
                       #~ '_'.join((name, 'units', seg.oid)),
                       #~ '_'.join((name, seg.turn.oid)))
                # full six features
                rc = get_commitments(seg, cl)
                rcm = [(r in rc) for r in resl]
                yield rcm + [bool(rc),
                    is_clue(seg),
                    is_unclue(seg),
                    has_nr(seg),
                    '_'.join((name, 'discourse', seg.oid)),
                    '_'.join((name, seg.turn.oid))
                ]
                
    c_t = cs.custom(c_feat, c_data())
    c_t.save(fcomm)
    c_t.merge(e_t)
    c_t.sel_col(feat_sel, meta_sel)

    c_t.save(fmerge)
    print('Commitment data merged')

    #~ print(snames)
    lgames = set(na[:-3] for na in all_anno) & set(na[:-3] for na in snames)
    for lg in lgames:
        print(lg)

    sys.exit()

###### QAP #######################################

#~ if True:
if False:
    p_t = cs.TabData(fpairs)
    p_t.sel_row({'CLASS':'UNRELATED'}, negate=1)
    # Warning : you're supposing ALL EDUs are part of a relation
    #   Check this, or you'll lose some
    print('Pairs loaded')
    p_c = cs.Trainer(p_t, 10, 'dialogue')

    pc_feat = (('is_question_p', 'd', ''),
               ('is_answer_p', 'd', ''),
               ('id', 'd', 'meta'))
               
    def pc_data():
        #~ it = ((r['CLASS'], r) for r in p_t)
        #~ for pred, row in it:
        for pred, row in p_c.pred_rows():
            if pred.value == 'Question-answer_pair':
                yield (True, False,
                       #~ gid(row['id_DU1']))
                       row['id_DU1'])
                yield (False, True,
                       #~ gid(row['id_DU2']))
                       row['id_DU2'])
            else:
                # Not a QAP, but still an instance
                yield (False, False,
                       #~ gid(row['id_DU1']))
                       row['id_DU1'])
                yield (False, False,
                       #~ gid(row['id_DU2']))
                       row['id_DU2'])

    pc_t = cs.custom(pc_feat, pc_data())
    pc_t.fuse_rows('id')
    pc_t.save(fqap)
    print('QAP data created')

    xpc_feat = (('q_id', 'd', ''),
                ('a_id', 'd', ''))
    
    def xpc_data():
        delayed = []
        for pred, row in p_c.pred_rows():
        #~ for row in p_t:
            if pred.value == 'Question-answer_pair':
            #~ if row['CLASS'].value == 'Question-answer_pair':
                yield (row['id_DU1'], row['id_DU2'])
            if pred.value == 'Q-Elab':
            #~ if row['CLASS'].value == 'Q-Elab':
                delayed.append((row['id_DU1'], row['id_DU2']))
        for e in delayed:
            yield e
            
    xpc_t = cs.custom(xpc_feat, xpc_data())
    xpc_t.save(fxqap)
    #~ xpc_t.save(frqap)
    print('Extra QAP data created')

#~ c_t.merge(pc_t)
#~ c_t.save(ffinal)

##### EDU fusion ! #####

if False:
    p_t = cs.TabData(fpairs)

    # Big list, eh ?
    single_feat = (
    ('dialogue', 'd', 'meta'),
    ('id', 'd', 'meta'),
    ('start', 'c', 'meta'),
    ('word_first', 'd', ''),
    ('word_last', 'd', ''),
    ('has_player_name_exact', 'd', ''),
    ('has_player_name_fuzzy', 'd', ''),
    ('has_emoticons', 'd', ''),
    ('is_emoticon_only', 'd', ''),
    ('speaker_started_the_dialogue', 'd', ''),
    ('speaker_already_spoken_in_dialogue', 'd', ''),
    ('speakers_first_turn_in_dialogue', 'd', ''),
    ('position_in_dialogue', 'd', ''),
    ('edu_position_in_turn', 'd', ''),
    ('ends_with_bang', 'd', ''),
    ('ends_with_qmark', 'd', ''),
    ('lex_domain_ressource_sheep', 'd', ''),
    ('lex_domain_ressource_wood', 'd', ''),
    ('lex_domain_ressource_wheat', 'd', ''),
    ('lex_domain_ressource_ore', 'd', ''),
    ('lex_domain_ressource_clay', 'd', ''),
    ('lex_robber_robber', 'd', ''),
    ('lex_trade_VBEchange_receivable', 'd', ''),
    ('lex_trade_VBEchange_givable', 'd', ''),
    ('lex_trade_VBEchange_mixte', 'd', ''),
    ('lex_dialog_politesse', 'd', ''),
    ('lex_dialog_acceptation', 'd', ''),
    ('lex_opinion_opinionPos', 'd', ''),
    ('lex_opinion_opinion???', 'd', ''),
    ('lex_opinion_opinionNeg', 'd', ''),
    ('lex_opinion_preference', 'd', ''),
    ('lex_modifier_negation', 'd', ''),
    ('lex_modifier_modal', 'd', ''),
    ('lex_pronoun_pronoun_1', 'd', ''),
    ('lex_pronoun_pronoun_3', 'd', ''),
    ('lex_pronoun_pronoun_2', 'd', ''),
    ('lex_pronoun_pronoun_1poss', 'd', ''),
    ('lex_pronoun_pronoun_2poss', 'd', ''),
    ('lex_pronoun_pronoun_3poss', 'd', ''),
    ('lex_question_what', 'd', ''),
    ('lex_question_who', 'd', ''),
    ('lex_question_when', 'd', ''),
    ('lex_question_how', 'd', ''),
    ('lex_question_where', 'd', ''),
    ('lex_question_why', 'd', ''),
    ('lex_ref_pronomAI', 'd', ''),
    ('lex_ref_quantifieur', 'd', ''),
    ('lex_ref_pronomJoueurs', 'd', ''),
    ('lemma_subject', 'd', ''),
    ('has_FOR_np', 'd', ''))

    def single_data():
        for row in p_t:
            dn = (row['dialogue'].value,)
            yield dn + tuple(row[k[0]+'_DU1'].value for k in single_feat[1:])
            yield dn + tuple(row[k[0]+'_DU2'].value for k in single_feat[1:])

    #~ r = p_t.t[0]
    #~ for k in single_feat[1:]:
        #~ print(k)
        #~ print(r[k[0]+'_DU1'].value)
    #~ sys.exit()

    se_t = cs.custom(single_feat, single_data())
    print('Data built, now merging')
    se_t.fuse_rows('id')
    se_t.save(fnsing)

#~ sys.exit()
p_t = cs.TabData(fpairs)
p_t.sel_row({'CLASS':'UNRELATED'}, negate=1)
p_c = cs.Trainer(p_t, 10, 'dialogue')
p_c.evaluate()

#~ print(set(row['dialogue'].value.split('_')[0] for row in c_t))
