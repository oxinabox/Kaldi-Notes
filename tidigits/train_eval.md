---
layout: default
title: Training & Evaluation
---

#Controlled remote vs local excution: `cmd.sh`
Kaldi is designed to work with SunGrid clusters.
It also work with other clusters.
We want to run it locally.
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

###Configuration.
The train_mono script takes many configuration options.
They can be set by passing them as flags to script: as so: `--<option-name> <value>`.
Or by putting them all into a config bash script, and adding the flag `--config <path>`.
THey could also be set by editting the defaults in `steps/train_mono.sh`, but there is no good reason to do this.


 * `nj`: Number of Jobs to run in parrellel. (Default `4`) 
 * `cmd`:  Job dispatcher script  (Defult `run.pl`)
 * `scale_opts`: takes a string (wrap it in quotes) to control al scaling options (Default `"--transition-scale=1.0 --acoustic-scale=0.1 --self-loop-scale=0.1"`)
 	* `transition-scale` (default `1.0`)
	* `acoustic-scale` (default `0.1`)
	* `self-loop-scale` (default `0.1`)
 * `num_iters` Number of iterations of training (default `40`)
 * `max_iter_inc`  Last iter to increase number of Gaussians on (default `30`)
 * `totgauss` Target number of Gaussians (detault `1000`)
 * careful=false
boost_silence=1.0 # Factor by which to boost silence likelihoods in alignment
realign_iters="1 2 3 4 5 6 7 8 9 10 12 14 16 18 20 23 26 29 32 35 38";
config= # name of config file.
stage=-4
power=0.25 # exponent to determine number of gaussians from occurrence counts
norm_vars=false # deprecated, prefer --cmvn-opts "--norm-vars=false"
cmvn_opts=  # can be used to add extra options to cmvn.
#


##Making of the Graph

##Decoding

##Reading experiment Results
