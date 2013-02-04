#!/usr/bin/env python
# Author: Sébastien Boisvert

import sys

if len(sys.argv)!=3:
	print("Usage")
	print("Program fastaFile lengthInNucleotides")
	sys.exit()

file=sys.argv[1]
theLength=int(sys.argv[2])

header=""
sequence=""
length=0

for line in open(file):
	if line[0]=='>':
		if length==theLength:
			print(header.strip())
			print(sequence.strip())
		header=line
		sequence=""
		length=0
	else:
		sequence+=line
		length+=len(line.strip())

print(header.strip())
print(sequence.strip())
