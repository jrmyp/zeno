# Curve learning... with Orange (meh)

from __future__ import print_function
import sys
import random
import classify as cs
print('Imports done')

fpairs = '/home/arthur/These/Master/Stac/TMP/latest/socl-season1.edu-pairs.csv'
fsrc = 'data/full.tab'

feat_sel = ['CLASS', 'num_edus_between', 'num_speakers_between', 'same_speaker', 'same_turn', 'has_inner_question', 'is_question_pairs', 'dialogue_act_pairs', 'num_tokens_DU1', 'word_first_DU1', 'word_last_DU1', 'has_player_name_exact_DU1', 'has_player_name_fuzzy_DU1', 'has_emoticons_DU1', 'is_emoticon_only_DU1', 'speaker_started_the_dialogue_DU1', 'speaker_already_spoken_in_dialogue_DU1', 'speakers_first_turn_in_dialogue_DU1', 'turn_follows_gap_DU1', 'position_in_dialogue_DU1', 'position_in_game_DU1', 'edu_position_in_turn_DU1', 'has_correction_star_DU1', 'ends_with_bang_DU1', 'ends_with_qmark_DU1', 'lemma_subject_DU1', 'has_FOR_np_DU1', 'is_question_DU1', 'num_tokens_DU2', 'word_first_DU2', 'word_last_DU2', 'has_player_name_exact_DU2', 'has_player_name_fuzzy_DU2', 'has_emoticons_DU2', 'is_emoticon_only_DU2', 'speaker_started_the_dialogue_DU2', 'speaker_already_spoken_in_dialogue_DU2', 'speakers_first_turn_in_dialogue_DU2', 'turn_follows_gap_DU2', 'position_in_dialogue_DU2', 'position_in_game_DU2', 'edu_position_in_turn_DU2', 'has_correction_star_DU2', 'ends_with_bang_DU2', 'ends_with_qmark_DU2', 'lemma_subject_DU2', 'has_FOR_np_DU2', 'is_question_DU2']
meta_sel = ['dialogue']

step_size = 10
if len(sys.argv) >= 2:
    step_size = int(sys.argv[1])

# Step 1 : master data table
if False:
    t_full = cs.TabData(fpairs)
    t_full.sel_col(feat_sel, meta_sel, 'CLASS')
    t_full.save(fsrc)

# Step 2 : set of all dialogues
t_master = cs.TabData(fsrc)
dials = list(set(l['dialogue'].value for l in t_master))
random.shuffle(dials)
print('Data loaded')

# Step 3 : the curve loop
all_scores = list()
n = len(dials)
n_steps = int(n/step_size)
for m in range(n_steps):
    t_size = step_size*(m+1)
    d_train = set(dials[:t_size])
    print('= Iteration {0:2}/{1:2}, size {2:3} ='.format(m+1, n_steps, t_size))
    t_cur = cs.TabData(fsrc)
    t_cur.sel_row_by(lambda x:(x['dialogue'].value in d_train))
    trainer = cs.Trainer(t_cur, grouper='dialogue')
    scores = trainer.evaluate(quiet=True)
    print('Score : {0:.3}'.format(scores['True']))
    all_scores.append((t_size, scores['True']))

# Step 4 : output scores
with open('res/curve.log', 'a') as fres:
    fres.write('# {0}\n'.format(n))
    fres.write(str(all_scores)+'\n')
