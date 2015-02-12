---
layout: default
title: Training
---

####Controlled remote vs local excution: `cmd.sh`
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
See [this section of the kaldi tuitorial](http://kaldi.sourceforge.net/tutorial_running.html#tutorial_running_feats)

[Mel-frequency cepstral coefficient](http://en.wikipedia.org/wiki/Mel-frequency_cepstrum)  (MFCCs) features.
Done using the script `steps/make_mfcc.sh`

####Compute Cepstral Mean and Variance Normalization statistics
Done using the script `steps/compute_cmvn_stats.sh`

##Training
Done using the script `steps/train_mono.sh`, However very similar steps are used in the other training scripts from in `steps` (such as `steps/train_deltas`).

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

### Initialisation Stages

####Initialise GMM (Stage -3)
Uses `/kaldi-trunk/src/gmmbin/gmm-init-mono`.
Call that with the `--help` option for more info

This defines (amoung other things), how many GMMs there are initially.


####Compile Training Graphs (Stage -2)
uses `/kaldi-trunk/source/bin/compile-training-graphs`.
Call that with the `--help` option for more info.

See [this section of the documentation](http://kaldi.sourceforge.net/graph_recipe_train.html).

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



###Training (Stage = Iterations completed)
Every Iteration a number of steps are carried out.

####Realign
If this iteration is one of the `realign_iters` then:

#####Boost Silence
Silence is boosted using `/kaldi-trunk/src/gmmbin/gmm-boost-silence`,
Call that with the `--help` option for more info.
Notably it does not nesc boost the silence phone (but it does in this training case), it can boost any phone.
It does this by modifying the GMM weights, to make silence more probable.

#####Align 
Features are aligned given the GMM models.
Uses `kaldi-kaldi/src/gmmbin/gmm-align-compiled`.
Call that with the `--help` option for more info.

###Reestimate the GMM model.
First accumulate stats which are used in the next step.
This is done using `/kaldi-trunk/src/gmmbin/gmm-acc-states-ali`.
Call that with the `--help` option for more info.

Then redo the GMM-based acoustic model.
This is done with  `/kaldi-trunk/src/gmmbin/gmm-est`, but using very different arguments.
Again call that with the `--help` option for more info.


Finally, increase the number of Gaussians (capped by `max_iter_inc`), so that by the time all the iterations (`num_iters`) are all complete, it will approach the target total number of gaussians (`totgauss`) -- assuming `max_iter_inc` did not block it.


##Making of the Graph

As showing earlier, the Grammer (G) can be composed with the Lexicon (L),
to get a phoneme to word mapping.

To increase the power of the phones, they could be expanded to add context.
For example making the 'ay' phone in 'n-ay-n' (nine) different from the one in 'm-ay-n' (mine).
This can be done with a Contrext dependancy FST, which can be scaled
with the number of phones to take into account in the context.
This is roughly equivelent to making use of n-grams on the phonetic level. Using 3 (ie one ot each side) context is refered to a triphones.

The Context Dependency can be expressed as a FST, refered to as C.



[This blog post](http://vpanayotov.blogspot.com.au/2012/06/kaldi-decoding-graph-construction.html) presents the details of the creation quiet well. It will be a bit of revision from the data preparation step.


###Usage of `util/mkgraph.sh`
The final graph is created using `util/mkgraph.sh`
To quote the introduction to that script:
> ...creates a fully expanded decoding graph (HCLG) that represents
> all the language-model, pronunciation dictionary (lexicon), context-dependency,
> and HMM structure in our model.  The output is a Finite State Transducer
> that has word-ids on the output, and pdf-ids on the input (these are indexes
> that resolve to Gaussian Mixture Models).

It also creates the afformentioned Context Dependency Graph.

Usage: 

```
utils/mkgraph.sh [options] <lang-dir> <model-dir> <graphdir>
```

 - `lang-dir` is, as before, the path the the directory containing all the language model files, [also prepared earlier](./lang_prep)
 - `model-dir` is the `exp-dir` from the previous train-mono step, which now contained the trained model.
 - `graph-dir` is the directory to place the final graph in. In the example script this is made as a graph subdirectory under the `exp-dir`. If it does not exist, it will be created

 - 

####Context Options
There are 3 options for defing how many phones are used to create the context.
theres are pathsed as the options to the `utils/mkgraph.sh` script

 - ` --mono` for monophone ie one phone ie no context (Used in `steps/train_mono.sh`)
 - no flag (default) for triphone ie 3 phones ie one phone ot each side for context
 - `--quinphone` for quinphone ie 5 phones ie 2 phones to each side for context

It would not be hard to extend the mkgraph script to create contexts of any length.
The section of the mkgraph script responsible for this,
makes use of `/kaldi-trunk/src/fstbin/fstcomposecontext`, take a look at its `--help` for more information.

