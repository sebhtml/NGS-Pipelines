#!/usr/bin/env python
# encoding= utf-8
# author: Sébastien Boisvert

import sys

if len(sys.argv) != 2:
	print("Usage: ")
	print("cat file.sam | ./filter-sam-stream-with-reference-column.py references.txt")
	sys.exit()

references = {}

reference_file = sys.argv[1]

for line in open(reference_file):
	reference = line.strip()
	references[reference] = 1
	#print("reference= " + reference)

for line in sys.stdin:
	tokens = line.split("\t")
	count = len(tokens)

# entries in a SAM file have 11 columns
# http://samtools.github.io/hts-specs/SAMv1.pdf
	if count < 11:
		print(line.strip())
	else:
		reference = tokens[2]
		if reference in references:
			print(line.strip())
