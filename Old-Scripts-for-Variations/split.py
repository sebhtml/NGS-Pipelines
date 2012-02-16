#!/usr/bin/python

import sys

file=sys.argv[1]

homo=open(file+"-homozygous.xls","w+")
hetero=open(file+"-heterozygous.xls","w+")

for line in open(file):
	if line.find("AF1=1") >= 0:
		homo.write(line)
	elif line.find("AF1=0.5") >= 0:
		hetero.write(line)

homo.close()
hetero.close()

