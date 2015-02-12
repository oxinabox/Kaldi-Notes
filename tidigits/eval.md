---
layout: default
title:  Evaluation
---
##Decoding

Decoding of th Graph is done using `steps/decode.sh`.
This script only works only for certain feature types -- conviently all the feature types we use in TIDIGITS. (Similar decoding functions also exist in steps, for other feature types)

###Usage for `steps/decode.sh`

Usage:
```
steps/decode.sh [options] <graph-dir> <test-data-dir> <decode-dir>
```

 - `test-data-dir` is the path to the training data directory [prepaired earlier](./data_prep)
 - `graph-dir` is the path the the directory containing the graphs generated in the previous step
 - `decode-dir` is a path to store all of its outputs -- including the results of the evaluations. It will be created if it does not exist.

###Configuration / Options 
The `decode.sh` script takes many configuration options, these should be familar from the `train_mono.sh` script options above.
They can be set by passing them as flags to script: as so: `--<option-name> <value>`.
Or by putting them all into a config bash script, and adding the flag `--config <path>`.
They could also be set by editting the defaults in `steps/decode.sh`, but there is no good reason to do this.


 * `nj`: Number of Jobs to run in parrellel. (default `4`) 
 * `cmd`:  Job dispatcher script  (default `run.pl`)


 * `iter`: Iteration of model to test. Training step above actually stores a copy of the model for each iteration. This option can be used to go back and test that (default final trained model). Overridden by `model` option.
 * `model`: which model to use, given by path. If given this overides the `iter` (default determined by valure of `iter`)
 
 * `transform-dir` directory path to find fMLLR transforms (Not useful for TIDIGITS). (default: N/A only used if fMLLR transformed were done on features.)
 * `scoring-opts` options to local/score.sh. Can be used to set min and max Language Model Weight for rescoring to be done. (default: "")
 * `num-threads` number of threads to use, (default 1).
 *  --parallel-opts <opts>                           # e.g. '-pe smp 4' if you supply --num-threads 4
 * `stage`: This is used to allow you to skip some steps, as above. However decode only has 2 stages. If stage is greater than 0 will skip decoding and just do scoring. (default `0`)

Options passed on to `kaldi-trunk/src/gmmbin/gmm-latgen-faster`:

 * `acwt` acoustic scale applied to accoustic likelyhoods applied in lattice generation (default 0.083333). It affects the pruning of the latice (low enough likelyhood will be pruned).
 * `max_active` (default 7000)
 * `beam` decoding beam (default 13.0)
 * `lattice_beam` latice generation beam (default 6.0)



###Lattices
From the [Kaldi documentation]( http://kaldi.sourceforge.net/lattices.html) "A lattice is a representation of the alternative word-sequences that are "sufficiently likely" for a particular utterance."

[This blog post](http://codingandlearning.blogspot.com.au/search/label/KWS14) gives an introduction to the Latices in Kaldi quiet well, relating them to the other FSTs.

Kaldi creates and uses these latices during the decoding step.
However, interpretting them can be hard, because all the commandline programs for working with them use [Kaldi's special table IO](http://kaldi.sourceforge.net/io_tut.html), describing how this works in detail is beyound the scope of this introduction.
The commandline programs in question can be found in `/kaldi-trunk/src/latbibin`


The Latices are output during the decoding into `<decode-dir>`. Into a numbered gzipped file. eg `lat.10.gz`. Don't bother unzipping them -- the internal files are binary also.
Each of these archieves containes many latices - one for each utterance.

Commands to work with them take the general form of:

```
<latice-command> [options] "ark:gunzip -c <path to lat.N.gz>|" ark,t:<outputpath>

```
Each of the latice commands do take the `--help` option which will cause them to give the other options.

####Example Conveting a latice to a FST Diagram
For example,
Consider the lattice gzipped at `exp/mono0a/decode/lat.1.gz`

Running:

```
lattice-to-fst "ark:gunzip -c exp/mono0a/decode/lat.1.gz|" ark,t:1.fsts
utils/int2sym.pl -f 3 data/lang/words.txt 1.fsts > 1.txt.fsts

```

(Assuming that `/kaldi-trunk/src/latbin` is in your path)

Will fill `1.fsts` with a collection of text form fsts, one for each utterance space seperated.
Ones with multiple terminal states have multiple different "reasonably likely" phrases possible.
The output labels on the transitions are words (Which we restored using int2sym).
The weights are the negitive log likelyhood of that transitor (or that final state)

As shown below:

```
ad_16a 
0 1 1 3 14.7788 
1 2 6 8 5.0416 
2 2.61209 

ad_174o2o8a 
0 1 1 3 12.5118 
0 11 o 2 9.44585 
1 2 7 9 9.34774 
1 16 o 2 6.57278 
2 3 4 6 2.08985 
3 4 o 2 10.2191 
4 5 2 4 4.91992 
4 9 o 2 3.20784 
5 6 o 2 3.84306 
6 7 o 2 3.90951 
6 13 8 10 7.07031 
7 8 8 10 6.74935 
7 14 o 2 3.79537 
8 2.61209 
9 10 2 4 5.3914 
10 6 o 2 3.84306 
11 12 1 3 4.75861 
12 2 7 9 9.34774 
13 2.61209 
14 15 8 10 6.63099 
15 2.61209 
16 17 7 9 6.38392 
17 3 4 6 2.08985 
```

Then we grab one particular FST off of it. (in this case just  using Awk to grab some lines -- most sophisticated approaches exist). Compile it. 
Project it only along the input labels (cos they are the words it will guess at), Minimise the number of states to get a simpler but equivelent model (easier to read) and finally draw it as an FSA.

```
cat 1.txt.fsts | awk "6<NR && NR<30" |\
    fstcompile --isymbols=data/lang/words.txt --keep_isymbols| \ 
    fstproject | fstminimize| \ 
    fstdraw --portrait --acceptor | dot -Tsvg > 1.2.svg
```

The Result of this, being a FSA that will accept (/generate) the likely matchs for the utterance `ad_174o2o8a`. 
The utterance actually said "174o2o8", wich is accepted by the path through states "0,2,4,5,6,8,9,12"

Note: that when the confidance in the path being correct is very high no weight is shown.

![parse lattice](./174o2o8a.png)

Notice that the latice has alot of paths allowing 'o' to be followed by another 'o'.

#### Drawing Phone Lattices
Much like we can draw lattices at the word level,
we can go down to draw them at the phone level.


```
lattice-to-phone-lattice exp/mono0a/final.mdl "ark:gunzip -c exp/mono0a/decode/lat.1.gz|" ark,t:1.ph.lats
lattice-copy --write-compact=false ark:1.ph.lats ark,t:1.ph.fsts
utils/int2sym.pl -f 4 data/lang/phones.txt 1.ph.fsts > 1.ph.txt.wfsts
cat 1.ph.txt.wfsts | awk 'BEGIN{FS = " "}{ if (NF>=4) {print $1," ", $2," ",$3," ",$4;} else {print $1;};}' > 1.ph.txt.fsts
```

Notice that in the first step the model (final.mdl)  was also used.
The output of the first step is in the Compact Latice form which is not ammniable to being worked with by scripts like int2sym.
The secondset expands it, making it a FST.
Third step is simply subsituting the phone symbols into the output. It is worth looking perhaps at 1.ph.txt.fsts, notices that the weights are only at start word phones. It is also however hard to read as it have hundred of empty string states ('<eps>'). Notice also there are 2 weights (this is the Graph Weight and the Accustic Weight). 
As there are 2 weights, this is not in a valid format for OpenFST. Thus the four line (the Awk Script) removed them all.

With that done we now have something that looks like a collection txt.fst, however it is still increbly willed with epsilon states.

Now to draw it up. Capturing the utterance `ad_174o2o8a` again, we will draw it:

```
cat 1.ph.txt.fsts| awk "199<NR && NR<1246" | \
    fstcompile --osymbols=data/lang/phones.txt --keep_osymbols | \
    fstproject --project_output | \
    fstrmepsilon | fstdeterminize | fstminimize  | \
    fstdraw --portrait --acceptor | dot -Tsvg > 1.ph.svg
```

So the steps being again, grabing the lines we want, compling it.
Projecting it (this time on the output space),
removing espilons, determining, and minimising to make it more readable.
Then drawing it.

(Click to view full screen image)
[![phone lattice](./174o2o8aPhones.png)](./174o2o8aPhones.png)



Viewing Results
Also during te decoding step the results are recorded.

The  can be found in `<decode-dir>` under filenames called  `wer_<N>` where `N` is a number

Example:

```
compute-wer --text --mode=present ark:data/test/text ark,p:-
%WER 1.63 [ 670 / 41220, 420 ins, 111 del, 139 sub ]
%SER 4.70 [ 590 / 12547 ]
Scored 12547 sentences, 0 not present in hyp.
```

The wikipedia entry on [Word Error Rate (WER)](https://en.wikipedia.org/wiki/Word_error_rate), is a reasonable introduction, if you are not familar with it.

The Sentence Error Rate (SER), is actually the utterance error rate.
Of all the unterances in the test set, it is the portion that had zero errors.
Both error rates only consider the most likely hypothesis in the latice.

