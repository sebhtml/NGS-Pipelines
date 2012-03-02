#!/usr/bin/env python

import sys

"""
This script takes Taxon-Names.tsv in input

"""

print "<root>"

for line in open(sys.argv[1]):
	tokens=line.split("\t")
	print "<taxon><identifier>"+tokens[0]+"</identifier><name>"+tokens[1].strip()+"</name><rank>"+tokens[2].strip()+"</rank></taxon>"

print "</root>"
