#!/usr/bin/python

import sys

backgroundFile=open(sys.argv[1])
signalFile=open(sys.argv[2])
outputFile=open(sys.argv[3],"w+")


background={}

for line in backgroundFile:
	tokens=line.split()
	key=tokens[0]+tokens[1]+tokens[2]+tokens[3]
	background[key]=1

backgroundFile.close()

for line in signalFile:
	tokens=line.split()
	key=tokens[0]+tokens[1]+tokens[2]+tokens[3]
	if key not in background:
		outputFile.write(line)

outputFile.close()
signalFile.close()
