echo \(  1/ 36\) Processing pilot01.conll
mkdir -p /home/perret/Tests/report/data/pilot01/discourse/jperret
/home/perret/Master/Stac/code/parser/parse-to-glozz /home/perret/Master/Stac/data/pilot/pilot01/unannotated /home/perret/Tests/report/conll/pilot01.conll /home/perret/Tests/report/data/pilot01/discourse/jperret
ln -s /home/perret/Master/Stac/data/pilot/pilot01/unannotated /home/perret/Tests/report/data/pilot01/unannotated

mkdir -p /home/perret/Tests/report/graph
stac-util graph /home/perret/Tests/report/data --output /home/perret/Tests/report/graph
