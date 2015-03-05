mkdir -p ~/Tests/probs/2015-02-26T0251/maxent/ref
mkdir -p ~/Tests/probs/2015-02-26T0251/maxent/pred
mkdir -p ~/Tests/probs/2015-02-26T0251/maxent/msdag
mkdir -p ~/Tests/probs/2015-02-26T0251/maxent/mst
echo === Classifier : maxent ===
echo == Fold : 0 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-0/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-0/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 0 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-0/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-0/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

echo == Fold : 1 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-1/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-1/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 1 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-1/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-1/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

echo == Fold : 2 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-2/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-2/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 2 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-2/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-2/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

echo == Fold : 3 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-3/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-3/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 3 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-3/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-3/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

echo == Fold : 4 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-4/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-4/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 4 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-4/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-4/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

echo == Fold : 5 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-5/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-5/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 5 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-5/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-5/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

echo == Fold : 6 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-6/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-6/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 6 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-6/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-6/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

echo == Fold : 7 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-7/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-7/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 7 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-7/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-7/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

echo == Fold : 8 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-8/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-8/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 8 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-8/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-8/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

echo == Fold : 9 ==
attelo show_probs -C ~/Master/Stac/code/parser/stac-features.config -A ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-9/all.maxent.attach.model -R ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-9/all.maxent.relate.model -o ~/Tests/probs/2015-02-26T0251/maxent --fold-file ~/Master/Stac/TMP/2015-02-26T0251/eval-current/folds-all.json --fold 9 ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.edu-pairs.csv ~/Master/Stac/TMP/2015-02-26T0251/eval-current/all.relations.csv 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-9/output.maxent-msdag ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/msdag 
python postrel.py ~/Master/Stac/TMP/2015-02-26T0251/scratch-current/fold-9/output.maxent-mst ~/Tests/probs/2015-02-26T0251/maxent/ref ~/Tests/probs/2015-02-26T0251/maxent/mst 

