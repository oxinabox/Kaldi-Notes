#Language Preparation
[The offical kaldi documentation on this section](http://kaldi.sourceforge.net/data_prep.html#data_prep_lang).

To understand this section you should first [understand openFST]( ../fst-example/intro_to_OpenFST.md).

##The Phones
Kaldi expects a number of files to be in the `data/lang/phones/` directory.
Most of them are not complex for TIDIGITS.

To falcilitate the creation of this, it is useful to have a full list of phonemes. This could be created many ways. One way it to apply Awk to the lexicon (see next section).

These phone files a simple lists with one phone each line:

 - `silence.txt`, `context_indep.txt` and `optional_silence.txt` all are made to just single like files containing `sil` the silence phoneme symbol.
 - `nonsilence.txt` contains all other phonemes.

The following files would do alot more in more complicated situations, but are ssimple for TIDIGITS
- `sets.txt` each line contains a set of phones that should be considered to be the same phoneme (ie a set of morphemes for one phoneme). Since in TIDIGITS this is not a concern (we don't have access to a morpheme level transcription), each set contains just the one phonene so all phonems should be listed on there own line in this file. Including sil.
- `disambig.txt` should be created and left empty.
- `extra-questions.txt` should also be created and left empty.

###Generating isymbols files from the phones.
Once you have a phonelist, it is very easy to enumerate it to create the isymbols file required for the phoneme-word FST.

###Convertering Symbol Phonelist to Integer Phone Lists 
Once you have aisymbols file, each of the files created in the previous set need to be converted to lists of there matching integers rather than textual symbols. The files created this way have the same name, but with a `.int` extension.

The perl script `utils/sym2int.pl` is used for this. It can take a single paramerter of the symbols file, and then will take on standard in, the sybolic (`.txt`) phone lists, and output (on standard out), there corrisponding integer forms.


silence, nonsilence, context_indep, optional_silence, disambig
 all also need to be converter to colon seperated list files (`.csl`),
 these are the same as the `.int` files, but instead of the integer phone representation being seperated by linebreaks, they are seperated with colons. A simplish job for Awk/sed.

###roots.txt Decision Tree Roots
Kaldi makes use of Decision Trees for some functionality.
See [the documentation](http://kaldi.sourceforge.net/tree_externals.html) for the why and how of this.

It require a root definition file.
For TIDIGITS is is very simple.
`roots.txt` contains  on each line, `shared split <phone-symmbol>`, and has one line for each phone.
It is converted to `roots.int`, by converting each phone symbol to it integer representation.

##Words and Out of Vocabulary Lists
A word symbol list will also need to be constructed for the FST.
Again this can be generated from the lexicon (see below), with Awk.

The word symbols are simply: o, z ,1, 2, 3, 4, 6, 7, 8, 9.

To go with this Kaldi needs to be told what word to use when words that are not in the vocabulary list are found. Since no such words exist in TIDIGITS, it really doesn't mater what it done with them. But Kalidi requires the files.

Create a oov.txt with any one word in it. (Example script uses z).
Create a oov.int with the matching interger for it.
This can be done manually,
or it could be done with `sym2int` on the words symbol list, created earlier.
<sub>
If you arranged you wordsymbols so that the int form of your oov word is the same is its text form then you are either over or under thinging this, and  you could copy the oov.txt to oov.int</sub>

## The Lexicon
The example recipy for TIDIGITs is quiet clever about contructing the phoneneme to word FST.
There script `util/make_lexicon_fst.pl` takes a lexicon file, and outputs a text FST file.
Each line of the Lexicon file has the format:

```
<word> <phoneme> <phoneme> <phonen....
```

ie one word followed by its phonene make up, specified with space delimited symbols.


### Converting Lexicon to lexicon.fst.txt: `util/make_lexicon_fst.pl`
The Full break-down of how to use it (which will be output if no arguements are passed to it):

Usage: 
```
make_lexicon_fst.pl [--pron-probs] lexicon.txt [silprob silphone [sil_disambig_sym]] >lexicon.fst.txt
```

Creates a lexicon FST that transduces phones to words, and may allow optional silence.
Note: ordinarily, each line of `lexicon.txt` is: `w`fstcompile`ord phone1 phone2 ... phoneN`; if the `--pron-probs` option is used, each line is: `word pronunciation-probability phone1 phone2 ... phoneN`.  The probability 'prob' will typically be between zero and one, and note that it's generally helpful to normalize so the largest one for each word is 1.0, but this is your responsibility.  The silence disambiguation symbol,
e.g. something like #5, is used only when creating a lexicon with disambiguation symbols, e.g. L_disambig.fst, and was introduced to fix a particular case of non-determinism of decoding graphs.

###Compiling the Lexicon FST:  `L.fst`
The lexicon.fst.txt, is then compiled (`fstcompile`), using isymbols and osymbols from the generated from the lexicon.txt, plus the silence phoneme (silphone) added in the make lexicon.txt.fst step, plus a emptysi
It it then arcsorted with `fstarcsort` on output lable. (not sure why this is required.)

####L_disambig.fst = L.fst

To quote the tidigits recipe:
>in this setup there are no "disambiguation symbols" because the lexicon
 contains no homophones; and there is no '#0' symbol in the LM because it's
 not a backoff LM, so L_disambig.fst is the same as L.fst

SO L.fst is copied to L_disambig.fst

For more information on disambiguation read the [documentation page](http://kaldi.sourceforge.net/graph.html#graph_disambig).



