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

The offical [Kaldi tuitorial](http://kaldi.sourceforge.net/tutorial.html) is a bit all over the place, but worth a look, it is no doubt getting better as the software matures.

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

The full process can be carried out by running `bash run.sh`. Though you most likly need to edit at least the TIDIGITs path, and the `cmd.sh` (so that it is set to run locally, not on a cluster).


#Data Preparation
[The offical kaldi documentation on this section](http://kaldi.sourceforge.net/data_prep.html#data_prep_data). It is the basis of alot of this section.

These steps are carried out by the script `local/tidigits_data_prep.sh`. It takes one parameter -- the path to the dataset.


##Locate the Dataset 
on on the SIP network, the TIDIGITs data set can be found at `/user/data14/res/speech_data/tidigits/`. Symlink it into a convient location.

##Parse its anonotations

###Kaldi Script: `.scp`: Basically just a list of Utterances to Filenames
A Kaldi script file is just a mapping from record_id, to extended-filenames.

Line Format:
'''
<recording_id> <extended_filename>
'''

####Extended Filename
The second part of the line is the extended filename
Extended Filename is the term used by Kaldi,  to refer ot a string that is either the path to a wav-format file or it is a bash command that will output wav-format data to standard out, followed by a pipe symbol (`|`).

As the TIDIGITS data is in the [SPHERE audio format](http://www.ee.columbia.edu/ln/LabROSA/doc/HTKBook21/node64.html), it needs to be converted to wav.
So the sample scripts in Kaldi use `sph2pipe` to convert them, so the .scp files lines will look like: (assuming `sph2pipe` is on your PATH, otherwise Path to the executable will be used)

```
ad_16a sph2pipe -f wav ../tidigits/test/girl/ad/16a.wav |
```

####Recording ID
The recording ID is the first part of each line in a  `.scp` file.



#Language Preparation
[The offical kaldi documentation on this section](http://kaldi.sourceforge.net/data_prep.html#data_prep_lang).


#Training/Evaluating Recogniser

