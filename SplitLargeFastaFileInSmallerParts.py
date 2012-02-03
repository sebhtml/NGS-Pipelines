#!/usr/bin/env python

import sys

file=sys.argv[1]
parts=int(sys.argv[2])

count=0

for line in open(file):
	if line[0]=='>':
		count+=1

elementsPerPart=count/parts

flushed=0

part=0

out=open(file.replace(".fasta",".Part."+str(part)+".fasta"),"w")

for line in open(file):
	if line[0]=='>':
		flushed+=1

		if flushed==elementsPerPart:
			if part!=parts-1:
				out.close()
				part+=1
				flushed=0
				out=open(file.replace(".fasta",".Part."+str(part)+".fasta"),"w")

	out.write(line)

out.close()
