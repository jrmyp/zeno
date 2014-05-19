# Testing soothes the mind

import Orange

fsing = '/home/arthur/These/Master/Stac/data/SNAPSHOTS/2014-05-01/socl-season1.just-edus.csv'
feat_sel = ['word_first','word_last','has_player_name_exact','has_player_name_fuzzy','has_emoticons','is_emoticon_only','speaker_started_the_dialogue','speaker_already_spoken_in_dialogue','speakers_first_turn_in_dialogue','position_in_dialogue','edu_position_in_turn','ends_with_bang','ends_with_qmark','num_tokens','lex_domain_ressource_sheep','lex_domain_ressource_wood','lex_domain_ressource_wheat','lex_domain_ressource_ore','lex_domain_ressource_clay','lemma_subject','has_FOR_np','id', 'dialogue']

t = Orange.data.Table(fsing)
print t[0]['id'].__class__
