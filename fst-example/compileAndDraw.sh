#!bash
#Create the example using this script
if [[ $# -eq 0 ]] ; then
	echo 'One argument must be given of the form \"name.fst.txt\" or \"name.fsa.txt\"';
	exit 1;
fi

IFS="."; #Make . the split character
inputFilenameParts=($1);
IFS=" "; #Put it back to default space

name=${inputFilenameParts[0]};
type=${inputFilenameParts[1]};

echo 'Preparing: '$name;

fsTextFile="${name}.${type}.txt";
fsFile="$name.${type}";
osymsFile="${name}.osyms";
isymsFile="${name}.isyms";
svgOutputFile="${name}.svg";

isymbols="--isymbols=${isymsFile}";
osymbols="--osymbols=${osymsFile}";


python makeSymbols.py $fsTextFile 2 > $isymsFile;

if [ $type = "fst" ] ; then
    python makeSymbols.py $fsTextFile 3 > $osymsFile;
    fstcompile $isymbols $osymbols --keep_isymbols --keep_osymbols $fsTextFile $fsFile;
    fstdraw --portrait $fsFile  | dot -Tsvg > $svgOutputFile;
elif [ $type = "fsa" ] ; then
    fstcompile --acceptor $isymbols --keep_isymbols $fsTextFile $fsFile;
    fstdraw --portrait $fsFile | dot -Tsvg > $svgOutputFile;
else
    echo "Filetype: ${type} not recognitsed. Recognised types are fst=finite state trasducer and fsa=finite state acceptor";
fi 

echo 'Done, outputted: ' $svgOutputFile

