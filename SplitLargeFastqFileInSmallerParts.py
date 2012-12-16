#!/usr/bin/env python
# Author: Sebastien Boisvert

import sys

arguments=sys.argv

if len(arguments)!=3:
	print("Split a large fastq file in smaller parts.")
	print("Usage: "+arguments[0]+" fileName blockSize")
	sys.exit()

fileName=arguments[1]
blockSize=int(arguments[2])
flushed=0
lineNumber=0
block=0

def openNewFile(fileName,block):
	return open(fileName.replace(".fastq","-block-"+str(block)+".fastq"),"w")

outputStream=openNewFile(fileName,block)
inputStream=open(fileName,"r")

for line in inputStream:

	#print("Line number "+str(lineNumber))

	if lineNumber==0:
		if flushed==blockSize:
			outputStream.close()
			block+=1
			flushed=0
			outputStream=openNewFile(fileName,block)

	outputStream.write(line)

	if lineNumber==3:
		flushed+=1
		lineNumber=0
	else:
		lineNumber+=1

outputStream.close()
