---
layout: default
title: How To Train TIDIGITS
---

#Introduction to training TIDIGITS
TIDIGITS is a comparatively simple connected digits recognition task.
Like for many well-known corpora, Kaldi includes a example script for it.
It is fairly typical for the example scripts -- though simpler than most.

The example script can be found in `kaldi-trunk/egs/tidigits/s5/` all other scripts referred to here are relative to that path. Kaldi example scripts are all written to be run from that path (or it equivelent in other examples) even if they are located in a subfolder.
Kaldi example scripts should only be run in `bash` -- they will not necessarily work in other POSIX shells.

Be aware that a lot of the recipe code is shared between WSJ (Wall Street Journal), and all the other examples (including TIDIGITs).
The `util/` and `steps/` folders in most of the example folders (including that for TIDIGITs),
is a symlink to the matching folders in the WSJ example. You can very well make use of these scripts in your own recipes.


####Other Resources:

 - The official [Kaldi tutorial](http://kaldi.sourceforge.net/tutorial.html) is not perfect (yet), but is a valuable resource. It is linked to in various sections throughout this document.

 - [This tutorial](http://analytcz.com/kaldi-hybrid-mlphmm-asr-2/) seems good. Its web hosting does not seem stable, right now the [google cached version can be used](http://webcache.googleusercontent.com/search?q=cache:z-MGlCv917sJ:analytcz.com/kaldi-hybrid-mlphmm-asr-2/)


##The Major Steps

There are Four Steps to applying Kaldi to a task such as this.


 1. [Data Preparation](./data_prep):
    * Locating the datafiles
    * Parsing its annotations (e.g. Speaker Labels, Utterance Labels)
    * Converting the audio data format
 2. [Language Preparation](./lang_prep):
    * Create Lexicon (Phoneme/Word dictionary)
    * Create Grammar (Word Language Model)
 3. [Training Speech Recognizer](train):
    * Training the GMMs
    * Building the HMM graph
 4. [Evaluating the Speech Recognizer](eval):
    * Decoding and building the lattices
    * Interpreting the results
The full process can be carried out by running `bash run.sh`. Though you most likely need to edit at least the TIDIGITs path, and the `cmd.sh` (so that it is set to run locally, not on a cluster).

These instructions also briefly touch on some of the option that might be needed in more complicated tasks. They also go into some detail on things which are not done by the `run.sh` script, for example outputting utterance recognition lattice diagrams. The instructions do not provide any kind of solid introduction to HMMs or GMMs. Nor to bash or awk.
