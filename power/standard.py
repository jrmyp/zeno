# Standard training
# Python 2

import sys
import classify as cs

# Bali sources
fpairs = '/home/perret/data/latest/socl-season1.edu-pairs.csv'

#~ fpairs = '/home/arthur/These/Master/Stac/TMP/latest/socl-season1.edu-pairs.csv'
#~ frel = '../res/minigrouped.csv'
#~ fpairs = '../res/grouped.csv'

feat_sel = ['CLASS', 'num_edus_between', 'num_speakers_between', 'same_speaker', 'same_turn', 'has_inner_question', 'is_question_pairs', 'num_tokens_DU1', 'has_player_name_exact_DU1', 'has_player_name_fuzzy_DU1', 'has_emoticons_DU1', 'is_emoticon_only_DU1', 'speaker_started_the_dialogue_DU1', 'speaker_already_spoken_in_dialogue_DU1', 'speakers_first_turn_in_dialogue_DU1', 'turn_follows_gap_DU1', 'position_in_dialogue_DU1', 'position_in_game_DU1', 'edu_position_in_turn_DU1', 'has_correction_star_DU1', 'ends_with_bang_DU1', 'ends_with_qmark_DU1', 'has_FOR_np_DU1', 'is_question_DU1', 'num_tokens_DU2', 'has_player_name_exact_DU2', 'has_player_name_fuzzy_DU2', 'has_emoticons_DU2', 'is_emoticon_only_DU2', 'speaker_started_the_dialogue_DU2', 'speaker_already_spoken_in_dialogue_DU2', 'speakers_first_turn_in_dialogue_DU2', 'turn_follows_gap_DU2', 'position_in_dialogue_DU2', 'position_in_game_DU2', 'edu_position_in_turn_DU2', 'has_correction_star_DU2', 'ends_with_bang_DU2', 'ends_with_qmark_DU2', 'has_FOR_np_DU2', 'is_question_DU2']
meta_sel = ['dialogue', 'id_DU1','id_DU2']

t_r = cs.TabData(fpairs)
#~ t_r.sel_row({'CLASS':'UNRELATED'}, negate=1)
t_r.sel_col(feat_sel, meta_sel, 'CLASS')
#~ t_r.save('res/cut.tab')

#~ c_r = cs.Trainer(t_r, grouper='dialogue')
c_r = cs.Trainer(t_r, learner='logreg', grouper='dialogue')

c_r.evaluate()
sys.exit()
with open('../res/gpred.tab', 'w') as f:
    for pred, row in c_r.pred_rows():
        line = '\t'.join([k.value for k in (
            pred,
            row.getclass(),
            row['id_DU1'],
            row['id_DU2'])])
        f.write(line + '\n')

