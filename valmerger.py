# Value merger
# Not very useful outside of commitment script, but eh

# d : dict(feature, merger name)
d = {'start': 'first', 'speaker_already_spoken_in_dialogue': 'or', 'lex_pronoun_pronoun_2': 'or', 'has_FOR_np': 'or', 'lex_opinion_opinion???': 'or', 'lex_domain_ressource_wheat': 'or', 'lex_question_when': 'or', 'has_player_name_exact': 'or', 'lex_robber_robber': 'or', 'lex_dialog_acceptation': 'or', 'edu_position_in_turn': 'first', 'speakers_first_turn_in_dialogue': 'first', 'lex_opinion_opinionNeg': 'or', 'lemma_subject': 'first', 'speaker_started_the_dialogue': 'or', 'lex_domain_ressource_sheep': 'or', 'lex_modifier_modal': 'or', 'lex_question_what': 'or', 'lex_pronoun_pronoun_1poss': 'or', 'has_emoticons': 'or', 'lex_domain_ressource_clay': 'or', 'position_in_dialogue': 'first', 'lex_question_who': 'or', 'lex_trade_VBEchange_givable': 'or', 'word_last': 'second', 'ends_with_qmark': 'second', 'lex_modifier_negation': 'or', 'lex_trade_VBEchange_mixte': 'or', 'lex_ref_pronomJoueurs': 'or', 'lex_question_why': 'or', 'id': 'first', 'lex_ref_quantifieur': 'or', 'lex_opinion_preference': 'or', 'is_emoticon_only': 'and', 'dialogue': 'first', 'lex_pronoun_pronoun_2poss': 'or', 'lex_dialog_politesse': 'or', 'lex_pronoun_pronoun_3poss': 'or', 'lex_opinion_opinionPos': 'or', 'lex_ref_pronomAI': 'or', 'is_commitment': 'or', 'lex_domain_ressource_ore': 'or', 'lex_trade_VBEchange_receivable': 'or', 'has_player_name_fuzzy': 'or', 'lex_question_where': 'or', 'lex_question_how': 'or', 'num_tokens': 'add', 'lex_pronoun_pronoun_1': 'or', 'ends_with_bang': 'second', 'turn_id': 'first', 'lex_domain_ressource_wood': 'or', 'lex_pronoun_pronoun_3': 'or', 'word_first': 'first'}

# Actual merger functions
# All designed to take and return strings
p = {'or': (lambda x,y: str((x == 'True') or (y == 'True'))),
     'and': (lambda x,y: str((x == 'True') and (y == 'True'))),
     'first': (lambda x,y : x),
     'second': (lambda x,y : y),
     'add': (lambda x,y : str(int(x)+int(y)))
    }

def gen_vm(l):
    return list(p[d[k]] for k in l)

