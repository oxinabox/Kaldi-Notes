---
layout: default
title: Training & Evaluation
---

#Controlled remote vs local excution: `cmd.sh`
Kaldi is designed to work with SunGrid clusters.
It also work with other clusters.
We want to run it locally, it can do that too.
This can be done by making sure cmd.sh sets the variables as follows:

```
export train_cmd=run.pl
export decode_cmd=run.pl
```
rather than making references to `queue.pl`.



#Training/Evaluating Recogniser

The majority of what is done covered by this page, 
is triggered by the script `run.sh`



## Feature Extraction

###Extracting the MFCC Features

[Mel-frequency cepstral coefficient](http://en.wikipedia.org/wiki/Mel-frequency_cepstrum)  (MFCCs) features.
Done using the script `steps/make_mfcc.sh`

####Compute Cepstral Mean and Variance Normalization statistics
Done using the script `steps/compute_cmvn_stats.sh`

##Training
Done using the script `steps/train_mono.sh`
Usage:

```
steps/train_mono.sh [options] <training-data-dir> <lang-dir> <exp-dir>"
```
 - `training-data-dir` is the path to the training data directory [prepaired earlier](./data_prep)
 - `lang-dir` is the path the the directory containing all the language model files, [also prepared earlier](./lang_prep)
 - `exp-dir` is a path for the training to store all of its outputs. It will be created if it does not exist.

###Configuration / Options 
The `train_mono` script takes many configuration options.
They can be set by passing them as flags to script: as so: `--<option-name> <value>`.
Or by putting them all into a config bash script, and adding the flag `--config <path>`.
THey could also be set by editting the defaults in `steps/train_mono.sh`, but there is no good reason to do this.


 * `nj`: Number of Jobs to run in parrellel. (default `4`) 
 * `cmd`:  Job dispatcher script  (default `run.pl`)
 * `scale_opts`: takes a string (wrap it in quotes) to control scaling options (default `"--transition-scale=1.0 --acoustic-scale=0.1 --self-loop-scale=0.1"`)
 	* `transition-scale` (default `1.0`)
	* `acoustic-scale` (default `0.1`)
	* `self-loop-scale` (default `0.1`)
 * `num_iters` Number of iterations of training (default `40`)
 * `max_iter_inc`  Last iter to increase number of Gaussians on (default `30`)
 * `totgauss` Target number of Gaussians (detault `1000`)
 *  `careful` passed on to gmm-align-compiled. To quote its documention: "If true, do 'careful' alignment, which is better at detecting alignment failure (involves loop to start of decoding graph)." (default `false`)
 * `boost_silence` Factor by which to boost silence likelihoods in alignment. (Default `1.0`)
 *  `realign_iters` iterations in which to perform realignment (default `"1 2 3 4 5 6 7 8 9 10 12 14 16 18 20 23 26 29 32 35 38"`)
 * `power`  exponent to determine number of gaussians from occurrence counts (detault `0.25`)
 * `cmvn_opts`  options will be passed on to cmvn -- like scale_opts. (default `""`)
 * `stage`: This is used to allow you to skip some steps, if the program crashed partway though. The stage variable sets the stage to start at. The stages are discussed in the next section (default `-4`)

### Initiallisatation Stages

####Initialise GMM (Stage -3)
Uses `/kaldi-trunk/src/gmmbin/gmm-init-mono`.
Call that with the `--help` option for more info

This defines (amoung other things), how many GMMs there are initially.


####Compile Training Graphs (Stage -2)
uses `/kaldi-trunk/source/bin/compile-training-graphs`.
Call that with the `--help` option for more info.

####Align Data Equally (Stage -1)
Creates an equally spaced alignment. As a starting point for further alignment stages.
Uses `/kaldi-trunk/source/bin/align-equal-compiled`.
Call that with the `--help` option for more info.

####Estimate Gaussians (Stage 0)
Do the  maximum likelihood estimation of GMM-based acoustic model.
Uses `/kaldi-trunk/src/gmmbin/gmm-est`.
Call that with the `--help` option for more info.

The script notes:

>In the following steps, the `--min-gaussian-occupancy=3` option is important, otherwise
> we fail to est[imate] "rare" phones and later on, they never align properly.



###Training


##Making of the Graph

##Decoding

##Reading experiment Results
