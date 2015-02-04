![A FST for TIDIGITS](./tidigitsFST.png)
Above: An FST for pronouncing the digits 1-9 and two pronouncations of zero as:  O(o) and zero (z), as used in TIDIGITS


#Introduction to Finite State Transducers
A Weighted Finite State Transducer is a generalisation of a Finite state machine.

 - A descent set of slides can be found [here](http://www.gavo.t.u-tokyo.ac.jp/~novakj/wfst-algorithms.pdf)
 - [The OpenFst documentation](http://www.openfst.org/twiki/bin/view/FST/FstQuickTour) is nonaweful, though the shell  and C++ sections are intermixed.
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



##Examples provided here

This folder contains 3 examples:

##simple.fsa.txt



##Scripts





####NOTE: The example scripts assume `openfst/bin` is in your `PATH`.
Add to your .bashrc (or similar) `PATH="<...>/kaldi-trunk/tools/openfst/bin:${PATH}"`, where `<...>` is the math to the kaldi-trunk folder.
then `source ~/.bashrc`


