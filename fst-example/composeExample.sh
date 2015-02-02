#!bin/sh

# Bases on http://www.isle.illinois.edu/sst/courses/minicourses/2009/lecture6.pdf

./compileAndDraw.py sent.fsa
./compileAndDraw.py dict.fst
fstcompose sent.fsa dict.fst > strings.fst
fstdraw --portrait --isymbols=sent.isyms --osymbols=dict.osyms strings.fst | dot -Tsvg >  strings.svg
echo 'done composing outputted strings.svg'
echo 'example sentences'

for i in `seq 1 10`;
do
	fstrandgen --seed=$RANDOM strings.fst | fstproject --project_output |
	fstprint --acceptor --isymbols=dict.osyms |
	awk 'BEGIN{printf("\n")}{printf("%s ",$3)}END{printf("\n")}'
done
