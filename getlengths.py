#!/usr/bin/env python
# S. Boisvert

"""
This tool takes a fasta file as input
and prints the sequence lengths.
"""

import sys

file=sys.argv[1]

currentLength=0
currentName=None

for line in open(file):
	filtered=line.strip()

	if filtered[0]=='>':
		if currentName!=None:
			print currentName+"	"+str(currentLength)
	
		currentLength=0
		currentName=filtered

	else:
		currentLength+=len(filtered)

if currentName!=None:
	print currentName+"	"+str(currentLength)
