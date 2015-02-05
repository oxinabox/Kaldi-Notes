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
<li> Data Preparation:</li>
<ul>
   <li> Locating the datafiles</li>
   <li> Parsing its annotations (eg Speaker Labels, Utterance Labels)</li>
   <li> Converting the audio data format</li>
</ul>
<li> Language Preparation:</li>
<ul>
   <li> Creating a Language Model in OpenFST</li>
</ul>
<li>Training/Evaluating the Speach Recogniser:</li>
<ul>
<li> This is the only step that is actually done in Kali proper, rather than by helper scripts and tools.</li>
<li> Viewing the results is also nontrivial</li>
<li> Kaldi does not store results in the most clear way,</li>
</ul>
</ol>




