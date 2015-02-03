

![A FST for TIDIGITS](./tidigitsFST.png)

Above: An FST for pronouncing the digits 1-9 and two pronouncations of zero as:  O(o) and zero (z), as used in TIDIGITS



#Introduction
A Weighted Finite State Transducer is a generalisation of a Finite state machine.

A descent set of slides can be found [here](http://www.gavo.t.u-tokyo.ac.jp/~novakj/wfst-algorithms.pdf)

##Strings
A string is a series of symbols from an alphabet

##Finite State Acceptor
A Finite State Acceptor has the componants of: 

 - a number of States 
     - one or more of which is initial
     - one or more of which is terminal
 - connections between states, with a input symbol (ie label)
     - the symbol could be the empty string (often writen "-" or "<eps>" or "ε")
     - Not nescisarily a one to one label to next state mapping (ie nondetermatistic)


##Finite State Transducers



##Weighted Finite State Acceptor/Transducer
As per the orginal, but with a weight assiciated with each edge (as well as input, and output for transducers)
This weight has a ⊕ and ⊗  operation defined on it,
so that weight of alternitives and that cumulitive weight along a path can be found.

 -- eg weight along a path is prouct of probabilities, and represents the probability of that input string.
 -- eg sum of weights on two edges is the probaility of either of those alternitives.



#Finite State Transnducers in Kaldi


#Examples:

##Filetypes

.fst.txt


##Examples provided here

This folder contains 3 examples:

##simple.fsa.txt



##Scripts




####NOTE: The example scripts assume `openfst/bin` is in your `PATH`.
Add to your .bashrc (or similar) `PATH="<...>/kaldi-trunk/tools/openfst/bin:${PATH}"`, where `<...>` is the math to the kaldi-trunk folder.
then `source ~/.bashrc`


