---
layout: default
title: How To Train TIDIGITS
---

#Introduction
TIDigits is a comparatively simple connected digits recognition task.
Like many well-known corpia, Kaldi includes a example script for it.
It is fairly typical for the example scripts.

The dataset 


##The Three Major Steps

There are Three Steps to applying Kaldi to a task such as this.

<ol>
<li> Data Preparation:
<ul>
   <li> Locating the datafiles
   <li> Parsing its annotations (eg Speaker Labels, Utterance Labels)
   <li> Converting the audio data format
</ul>
<li> Language Preparation:
<ul>
   <li> Creating a Language Model in OpenFST
</ul>
<li>Training/Evaluating the Speach Recogniser:
<ul>
<li> This is the only step that is actually done in Kali proper, rather than by helper scripts and tools.
<li> Viewing the results is also nontrivial
<li> Kaldi does not store results in the most clear way,
</ul>
</ol>




