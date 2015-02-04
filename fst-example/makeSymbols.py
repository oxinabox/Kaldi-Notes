
import sys


if len(sys.argv)<3 or '-h' in sys.argv or '--help' in sys.argv:
    print("""
    Usage: python makeSymbols file fieldNumber

    file: the textual FST/FSA file (.fst.txt or .fsa.txt usually), to extract the symbols from
    fieldNumber: which column of the file to take symbols fro
        input symbols use fieldNumber of 2
        output symbolss use fieldNumber of 3

    The Symbols Table is output to standard out, and can be piped into a file
    """)


words=set()
index = int(sys.argv[2])

with open(sys.argv[1], 'r') as ff:
    for line in ff:
        fields = line.split(' ')
        if len(fields)>index:
            field = fields[index].strip()
            if (field):
                words.add(field)

    print("- 0") #alway have the empty string as 0
    words.discard('-')
    for (ii,word) in enumerate(words,1):
        print("%s %d" % (word,ii))




