#Required Knowledge

To make use of Kaldi, there is some significant prior required knowledge.

 - Bash
 - Awk
 - Perl
 - Python

While Kaldi is made in C++, knowledge of C++ is not required to use it.

##Bash
Example run scripts in Kaldi are written in Bash.
Not POSIX shell, but Bash, they contain some "Bashisms", which will not reliably work in other shells.

Bash is the main glue that holds Kaldi all together.
It is used to prepare the data,
prepare the language files,
trigger the training,
and print the results.

Knowing how to at least read bash is a must for using Kaldi.
The others languages can be picked up as required, but bash is a must if you want to make use of the example scripts.
You most likely *do* what to make use fo the example scripts, they are some serious part of the documentation.

Bash is however quiet easy for anyone who has work on the unix shell.

Key knowledge areas:

 - Condtionals
 - Loops
 - Pipelines / input/output redictionion
 - variables
 - the PATH

##Awk
Awk is on of the standard tools for doing string manipulation on the commandline,
along with sed, grep, inline perl and simpler tools like tr, cut, head etc.

It is used alot in the perparing of fst file inputs. Alot of inlike Awk can be found in the aformentioned bash recipies.

It is a bit more complicated to understand than sed or grep, in that rather than a regex-tool it is a programming langauge.
A decent tuitorals exist online.

##Perl
Perl carries out alot of the heavy lifting of kaldi setup.
It is used for preparing data, where it gets to complex for Bash+Awk.
It is used to facilitate the paralell (and/or distributed) task execution.
It shows up thoughout the examples.

##Python
Python rarely shows up in the example scripts for kaldi, but it does show up.
When it does, it is doing a task similar to those perl is used for.
It is worth knowing, and using, as it is not a good idea to unleash more perl scripts into the wild.
Combining in tools like [Plumbum](https://pypi.python.org/pypi/plumbum), it could also be used to replace Bash -- this however is less portable.


