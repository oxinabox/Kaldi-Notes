#!/usr/bin/env python
#Create the example using this script

from plumbum import local
from plumbum.cmd import python, fstcompile, fstdraw, dot
import sys


inputFilenameParts = sys.argv[1].split('.')

name = inputFilenameParts[0]
type = inputFilenameParts[1]

print("Preparing: " + name)
print ("-"*32)

fsTextFile = name +'.' + type + '.txt'
fsFile = name+'.'+type
osymsFile = name+'.osyms'
isymsFile = name+'.isyms'
svgOutputFile = name+'.svg'

isymbols = '--isymbols='+isymsFile
osymbols = '--osymbols='+osymsFile


(python['makeSymbols.py', fsTextFile, 2] > isymsFile)()
if type == 'fst':
    (python['makeSymbols.py', fsTextFile, 3] > osymsFile)()
    (fstcompile[isymbols, osymbols, fsTextFile] > fsFile)()
    (fstdraw[isymbols,osymbols,'--portrait', fsFile] 
            | dot ['-Tsvg'] > svgOutputFile)()
else:
    assert(type=='fsa')
    (fstcompile['--acceptor',isymbols, fsTextFile] > fsFile)()
    (fstdraw['--acceptor', isymbols, '--portrait', fsFile] | 
            dot ['-Tsvg'] > svgOutputFile)()


print("Done, outputted: "+ svgOutputFile)

