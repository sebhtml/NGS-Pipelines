#!/usr/bin/env python

import sys

arguments=sys.argv

seedFile=arguments[1]
minimum=int(arguments[2])
sum=0

stream=open(seedFile)

for line in stream:
	tokens=line.split()
	length=int(tokens[0])
	frequency=int(tokens[1])

	if length>=minimum:
		sum+=length*frequency

stream.close()

print("minimum= "+str(minimum)+" sum= "+str(sum))

