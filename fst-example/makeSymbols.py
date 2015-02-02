import sys

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




