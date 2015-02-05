---
layout: default
title: Introduction to OpenFST
---

![A FST for TIDIGITS](./tidigitsFST.png)

Above: An FST for pronouncing the digits 1-9 and two pronouncations of zero as:  O(o) and zero (z), as used in TIDIGITS


#Introduction to Finite State Transducers
Weighted Finite State Transducers is a generalisations of finite state machines.
They can be used for many purposed, including implementing algorithms that are hard to write out otherwise -- such as HMMs, as well as for the representation of knowledge -- similar to a grammer.

##Other places to get information
 - A descent set of slides can be found [here](http://www.gavo.t.u-tokyo.ac.jp/~novakj/wfst-algorithms.pdf)
 - [The OpenFst documentation](http://www.openfst.org/twiki/bin/view/FST/FstQuickTour) and [FST Examples](http://www.openfst.org/twiki/bin/view/FST/FstExamples) are  nonaweful, though the shell  and C++ sections are intermixed.

##Terminology
###Symbols and Strings
Symbols come from some alphabet.
They could be letters, words, phomemes, etc.

A string is a series of symbols from an alphabet, it can include the empty string.
Matching the examples above, a string could be a word (spelt out), a sentence, a word (spelt out phonetically), etc.

A string can be represented as a Finite State Acceptor, where each symbol links to the a state which links to the next.

###Finite State Acceptor (FSA)
A Finite State Acceptor has the componants of: 

 - a number of States 
     - one or more of which is initial
     - one or more of which is terminal
 - connections between states, with a input symbol (ie label)
     - the symbol could be the empty string (often writen "-" or "<eps>" or "ε")
     - Not nescisarily a one to one label to next state mapping (ie nondetermatistic)

A FSA can be used to check if a string matches its patern -- it is computationally equivelent to a regular expression. 
It can also be used to generate strings which match that pattern.

FSA&apos;s can be treated as FSTs with same input and output symbols at each edge.

###Finite State Transducers (FST)
A Finite State Transducer extends the Finite State Acceptor wih the addition of:

 - output labels on each edge
   - again the output can be the empty string.
     - it is common (such as in the TIDIGIT example above), to see only the first transition in a nonbranching substructure to be labels -- the other states have nothing to add other than confirming we are in that chain. (which we might Not be)
     - The input alphabet and output alphabet do not have to be the same, and indeed are normally not.

A FST can be used to translate strings in its input alphabet to strings in its output alphabet, iff the input string matches the FSTs structure of allowed transistions.
Thus if a FSA accepting its input alphabet is composed with it, it can translate the FSA.
A series of FSAs can be composed, translating (matched) alphabet to alphabet, to get the desired output.


###Weighted Finite State Acceptor/Transducer
As per the orginal, but with a weight assiciated with each edge (as well as input, and output for transducers)
This weight has a ⊕ and ⊗  operation defined on it,
so that weight of alternitives and that cumulitive weight along a path can be found.

 -- eg weight along a path is prouct of probabilities, and represents the probability of that input string.
 -- eg sum of weights on two edges is the probaility of either of those alternitives.



#Finite State Transnducers in Kaldi

Kaldi uses FSTs (and FSAs), as a common knowledge repressentation for all things.


#OpenFST

##Filetypes

###Textual FST/FSA definition: `.fst.txt`, `.fsa.txt`, `.txt`
Textual Representation of the finite state transducer or finite state acceptor respectively.
These are the files you write to get things done, to describe your system.

In most of kaldi the `.fst.txt`/`.fsa.txt` is used. In other places it is just called `.txt`. In this document, it is always refered to by the former terms.


#### Line format:
Normal line `fromState toState inSymbol [outSymbol] [weight]` <br>
Terminal state line `terminalState`

 - `fromState`, `toState`, and `terminalState` are integer state labels
 - `inSymbol`, `outSymbol` are textual strings being the name of the symbols from the respective input and output alphabets.
     - `outSymbol` should not be present in FSAs, and should always be present in FSTs
 - `weight` is a decimal number, indicating the weight of the edge. It must be present in Weighted FSTs/FSAs

###Symbol table file: `.isyms`, `.osyms`, `.syms`, `.dict`, `.txt`
OpenFst like to refer to symbols by a positive integer.
Since any finite alphabet is isomorphic to a subset of the positive integers,
such a bijection exists, and can be created by enumerating each symbol.

For each FST you should have two of these files, one for the input alphabet and one for the output alphabet. For an FSA you should only have one -- for the input alphabet. Under most circumstances these can be generated from the `.fst.txt`/`.fsa.txt` programatically. One such script for that is provided here in [](./makeSymbols.py). Others exist thoughout the kaldi example scripts, often using AWK oneliners.

In different places different exentions are used.
The example [](./compileAndDraw.sh) script uses `.isyms` for symbol files generated from the input alphabet in the textual FSA/FSA description, and `.osyms` for that generated from the output alphabet.


####Line Format:
`symbol integer`

 - `symbol` is a symbol from the alphabet being maps
 - `integer` is a unique positive integer (that is to say each integer only apears once in this file).

### Binary FST/FSA: `.fst`, `.fsa`
This is the binary representation of the finite state transducer/acceptor.
It is produceced from the textual representation and symbol tables using
`fstcompile`.

### Graph of FST/FSA: `.dot`
It is a [Graph Description Language File](http://en.wikipedia.org/wiki/DOT_%28graph_description_language%29), producted by `fstdraw`.
Piping in through `dot` can convert it into another more common format.
Eg: `cat example.dot | dot -Tsvg > example.svg` will convert `example.dot` to a SVG file.
This is often done directly from the line that calls `fstdraw`.

##OpenFST componants
OpenFST is made up of several different commandline applications.
The three most used in kaldi are details briefly below:



###Common convention

####Input and Output
OpenFST commands which take a single input and produce a single output
(such as `fstdraw` and `fstcompile`)
have the basic usage of

```
fstcommand [FLAGS] [inputfile [outputfile]]
```

Which is to say an `inputfile` can optionally be provided,
and if it is, then optionally an `outputfile` can be provided also.

If either is missing then input will be taken from standard in (ie piped in, or read from keyboard if no inputpipe),
and output will be sent to standard output (ie piped out, or printed to the terminal if there is no output pipe.), repectively.


####Accessing Help (manpages)
Bacause OpenFST is not properly installed, it does not have entries in the man pages.
to get help with a command use:

```
fstcommand --help | less
```
###Compile: `fstcompile`
this converts a textural FST/FSA into a binary one.

 - FSA Usage: `fstcompile --acceptor --isymbols=<input.sym> [--keep_isymbols];`
 - FST Usage: `fstcompile --isymbols=<input.sym> -osymbols=<output.sym> [--keep_isymbols] [--keep_osymbols];`

Flags:

 - `--acceptor`: compiles it as an FSA, rather than a FST
 - `--isymbols=`, `--osymbols=`: specifies the input and output symbol tables
 - `--keep_isymbols`, `--keep_osymbols`: If set then the symbol stables as keeps in the binery file and do not need to be specified at later steps such as `fstdraw`

###Draw: `fstdraw`
produces a `.dot` file graph, from a binary FST/FSA

 - FSA Usage: `fstdraw --acceptor --portait [--isymbols=<input.sym>] [--osymbols=<output.sym>]`
 - FST Usage: `fstdraw --portait [--isymbols=<input.sym>] [--osymbols=<output.sym>]`
 - Common Use example: `cat eg.fst | fstdraw --portait --isymbols=eg.isyms --osymbols | dot -Tsvg > eg.svg`

Flags:

 - `--portrait` this flag should **always** be set. If not set then image comes out rotated 90 degrees, and on a overly large canvas.
 - `--isymbols`, `--osymbols`, as before, but if not provided then symbols in the graphic will be replaced with their numeric repressentation, unless `--keep_isymbols` or `--keep_osymbols` was set in the compile step
 - `--acceptor`: draws a FSA, rather than a FST. Without it it will label the FSA with output labels.

###Compose: `fstcompose`
Composed a FSA/FST with a FST

 - Usage: `fstcompose [--fst_compat_symbols=false] outer.[fst|fsa] inner.fst output.fst` 
 
Applying an input to the Output FST is equivelent to first applying it to the Inner then applying the output of that to the Outer. Ie `output(x)=outer(inner(x))`
 
 - `--fst_compat_symbols=false`: setting this to false (it defaults to true), may be required when composing FSTs/FSA where `--keep_isymbols` or `--keep_osymbols` was used and that the symbol files embeeded while actually compatable are not the same files (it seems to store the filenames, which can be seen by running `strings` on a fst).



###Other useful Commands
All the commands in openfst have a use.
Other commands which I have found particularly useful, 
but do not have space to detail include;

 - `fstsymbols` manipulate and export the symbols tables in the binary FST/FSA 
 - `fstproject` convert the FST into a FSA in either the input or output space by discarding the appoprate lables

#Examples provided here

Several scripts are provided here to demonstrate how to make use of OpenFST,
and to make using it easier.

###NOTE: The example scripts assume `openfst/bin` is in your `PATH`.
Add to your .bashrc (or similar) `PATH="<...>/kaldi-trunk/tools/openfst/bin:${PATH}"`, where `<...>` is the math to the kaldi-trunk folder.
then `source ~/.bashrc`


###makeSymbols.py
makeSymbols.py is a script to make creating the SymbolTables (which map symbols to arbitary unique integers) easier.

Usage: `python makeSymbols.py file fieldNumber`

 - `file`: the textual FST/FSA file (`.fst.txt` or `.fsa.txt usually`), to extract the symbols from
 - `fieldNumber`: which column of the file to take symbols from
     - input symbols use `fieldNumber` of 2
     - output symbolss use `fieldNumber` of 3

The Symbols Table is output to standard out, and can be piped into a file

###compileAndDraw.sh
Runs the whole process of compiling then drawing a FST/FSA.

Usage FSA:  `bash compileAndDraw.sh filename.fsa.txt`
Usage FST:  `bash compileAndDraw.sh filename.fst.txt`

Note: unlike  openfst programs this is file extention sensitive.
It will make the approprate call for a FSA or a FST based on the extention. 

###composeExample.sh
This example runs though the creation then compostion of the `dict.fst` and `sent.fsa`. It then outputs some sentences generated using the language model descried.

Usage: `bash composeExample.sh`

##Example FSTs/FSAs
This folder contains 3 examples:
The later two examples of sentence construction are based on ones provided in [these lecture notes](http://www.isle.illinois.edu/sst/courses/minicourses/2009/lecture6.pdf)

##[simple.fsa.txt](./simple.fsa.txt)
A  very simple Finite State Accepter.

##[dict.fst.txt](./dict.fst.txt)
A dictionary containing several words. There is only state in the dictionary -- as far it its concerns words can be in any order

##[sent.fsa.txt](./sent.fsa.txt)
A grammer for a simple sentence, expessed as a finite state acceptor.
Sentences can either be `determiner noun verb` or `determiner noun verb determiner noun`.



