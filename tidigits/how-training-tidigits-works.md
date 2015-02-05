---
layout: default
title: How To Train TIDIGITS
---

#Introduction
TIDigits is a comparatively simple connected digits recognition task.
Like many well-known corpia, Kaldi includes a example script for it.
It is fairly typical for the example scripts.

The example script can be foung in `kaldi-trunk/egs/tidigits/s5/` all other scripts refered to here are relitive to that path. Kaldi example scripts are all written to be run from that path (or it equivelent in other examples) even if they are located in a subfolder.
Kaldi example scripts should only be run in `bash`

##The Three Major Steps

There are Three Steps to applying Kaldi to a task such as this.

<ol>
<li> Data Preparation:
<ul>
   <li> Locating the datafiles</li>
   <li> Parsing its annotations (eg Speaker Labels, Utterance Labels)</li>
   <li> Converting the audio data format</li>
</ul></li>
<li> Language Preparation:
<ul>
   <li> Creating a Language Model in OpenFST</li>
</ul></li>
<li>Training/Evaluating the Speach Recogniser:
<ul>
<li> This is the only step that is actually done in Kali proper, rather than by helper scripts and tools.</li>
<li> Viewing the results is also nontrivial</li>
<li> Kaldi does not store results in the most clear way,</li>
</ul></li
</ol>


#Data Preparation
These steps are carried out by the script `local/tidigits_data_prep.sh`.

##Locate the Dataset 
on on the SIP network, the TIDIGITs data set can be found at `/user/data14/res/speech_data/tidigits/`. Symlink it into a convient location.

##


#Language Preparation

#Training/Evaluating Recogniser

