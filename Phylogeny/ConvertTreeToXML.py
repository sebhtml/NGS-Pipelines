#!/usr/bin/env python

import sys

"""
This script takes Tree-of-Life-Edges.tsv in input

"""

print "<root>"

for line in open(sys.argv[1]):
	tokens=line.split("\t")
	print "<arc><parent>"+tokens[0]+"</parent><child>"+tokens[1].strip()+"</child></arc>"

print "</root>"
