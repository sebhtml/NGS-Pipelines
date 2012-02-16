#!/usr/bin/python

# split a file in several files using the first column as bin filter key

import sys

prefix=sys.argv[1]
column=int(sys.argv[2])

output=None
lastKey=None

for line in sys.stdin:
	tokens=line.split()
	key=tokens[0]

	if output==None:
		lastKey=key
		output=open(prefix+"."+key,"w")
		
	if lastKey!=key:
		output.close()
		output=open(prefix+"."+key,"w")

	lastKey=key

	output.write(line)


output.close()
