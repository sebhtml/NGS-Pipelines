#!/usr/bin/env python

import sys

threshold=float(sys.argv[2])

for line in open(sys.argv[1]):
	if line[0]=='#':
		continue

	tokens=line.split("\t")
	ratio=float(tokens[5])

	if ratio<threshold:
		continue

	print line.strip()

