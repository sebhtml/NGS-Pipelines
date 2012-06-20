#!/usr/bin/env python

#import profile
import gzip
import zlib
import sys
import os
import os.path

if len(sys.argv) !=4:
	print "Usage"
	print sys.argv[0]+" file.fastq.gz selectedSequences groupSize"

	print "Example:"
	print sys.argv[0]+"	file.fastq	1	10	# this will output 10% of the sequences"

	sys.exit()

file=sys.argv[1]
selected=int(sys.argv[2])
groupSize=int(sys.argv[3])

stream=None

if file.find(".gz")>=0:
	stream=gzip.open(file)
else:
	stream=open(file)

i=0
period=4

for line in stream:

	if i<selected*period:
		print line,

	i+=1

	if i==groupSize*period:
		i=0


