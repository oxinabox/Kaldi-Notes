---

layout: default
title: Installing Kaldi
---

##Building Kaldi
- Following instructions at: http://kaldi.sourceforge.net/tutorial_setup.html

 - first `cd` to `kaldi-trunk/tools` then do a `make -j 8` to build to tools kaldi uses
    - Issue: Requires Libtool
        - Resolution: Build and install libtool, I did so by installing from source: http://ftpmirror.gnu.org/libtool/libtool-2.4.5.tar.gz locally (via configure --prefix)
 - then try and build kaldi, first running .configure
    - Issue: Needs a BLAS.
        - Resolution: use OpenBlas
            - go back to kaldi-trunl/tools and `make openblas` 
            - use it by running `./configure  --openblas-root=../tools/OpenBLAS/install`
    - Issue: this Kaldi won&apos;t run with GCC 4.8.4
        - Resolution: install newer GCC from source
            - Follow instructions at https://gcc.gnu.org/wiki/InstallingGCC
                - in particular for getting the dependancies
            - When it comes to running configure use: `../gcc-4.9.2/configure --prefix=$LOCAL_INSTALL --disable-multilib`
            - when doing use `make -j 8` or it will take a very long time to build
        - Resolution2: install from backports

##Installing  Graph Viewer

For viewing the output of fstdraw, you need to convert it into a useful format. To do this you need `dot` wich is part of graphviz. `apt-get install graphvis`

##Adding things to your path
Since Kaldi has not been install to any location -- just built in place.
Nothing is on your path.

The build process, spreads out all the binerys into a number of folders in `\kaldi-trunk\src/*bin`,
intermixing them with the source files. (so you can't just add the bin files to your path).

You might like to symlink all excutables into one folder and add it to your path.
The symlinking can be done with the following shell script:

```
for a in  `find . -type f -executable -print`;
do
ln -s $a bins
done
```
This will put them all into the bins directory.
Then you can edit your `.bashrc` file to add that to your path.
Eg:

```
PATH="/user/data7/20361362/kaldi/kaldi-trunk/src/bins:${PATH}"
```



