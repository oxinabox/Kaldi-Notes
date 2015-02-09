---
layout: default
title: How To Train TIDIGITS
---

#Introduction
TIDigits is a comparatively simple connected digits recognition task.
Like many well-known corpia, Kaldi includes a example script for it.
It is fairly typical for the example scripts.

The example script can be foung in `kaldi-trunk/egs/tidigits/s5/` all other scripts refered to here are relitive to that path. Kaldi example scripts are all written to be run from that path (or it equivelent in other examples) even if they are located in a subfolder.
Kaldi example scripts should only be run in `bash` -- they will not nescisarily work in other POSIX shells.

Be aware that a lot of the recipy code is shared between WSJ (Wall Street Journal), and all the other examples (including TIDIGITs).
the `util/` and `steps/` folders in most of the example folders (including that for TIDIGITs0),
is a symlink to the matching folders in the WSJ example. You can very well make use of these script utils and steps in your own recipies.



The offical [Kaldi tuitorial](http://kaldi.sourceforge.net/tutorial.html) is not perfect (yet), but is a valuable resource. It is linked to in various sections thoughout this document.

##The Three Major Steps

There are Three Steps to applying Kaldi to a task such as this.


 1. [Data Preparation](./data_prep):
    * Locating the datafiles
    * Parsing its annotations (eg Speaker Labels, Utterance Labels)
    * Converting the audio data format
 2. [Language Preparation](./lang_prep):
    * Creating a Language Model in OpenFST
 3. [Training/Evaluating the Speach Recogniser](train_eval):
    * This is the only step that is actually done in Kali proper, rather than by helper scripts and tools.
    * Viewing the results is also nontrivial
    * Kaldi does not store results in the most clear way,

The full process can be carried out by running `bash run.sh`. Though you most likly need to edit at least the TIDIGITs path, and the `cmd.sh` (so that it is set to run locally, not on a cluster).





