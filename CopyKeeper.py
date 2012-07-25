#!/usr/bin/python
# encoding: utf-8
# author: Charles Joly Beauparlant
# 2012-07-23

"""
This script filter a fastq file to keep only sequences with at least <minCopy> copy.
Saves data as fasta or fastq.
In fasta, all the identical sequences are collapsed together with the copy count in the header. 
In fastq, there is one entry per sequence.

Usage:
./CopyKeeper.py <inputFile> <minCopy> <outputType> > out.fasta|out.fastq
inputFile: fastq file.
minCopy: Minimal number of copy to keep sequence.
outputType: fasta or fastq.

"""

class CopyKeeper:
	def __init__(self, inputFile, minCopy):
		self.minCopy = minCopy
		self.inputFile = inputFile
		self.clear()

	def clear(self):
		self.seqCounts = {}

	def processFile(self):
		i = 0
		for line in open(self.inputFile):
			if i == 1:
				sequence = line.strip()
				self.processSequence(sequence)
			i += 1
			if i == 4:
				i = 0

	def processSequence(self, sequence):
		if sequence in self.seqCounts:
			self.seqCounts[sequence] += 1
		else:
			self.seqCounts[sequence] = 1

	def printResults(self, outputType):
		if outputType == "fasta":
			sorted(self.seqCounts, key = self.seqCounts.get)
			i = 0
			for seq in sorted(self.seqCounts, key = self.seqCounts.get, reverse = True):
				if self.seqCounts[seq] >= self.minCopy:
					print "> PP_" + str(i) + " Count: " + str(self.seqCounts[seq])
					print seq
					i += 1

		elif outputType == "fastq":
			i = 0
			for line in open(self.inputFile):
				if i == 0:
					header = line.strip()
				elif i == 1:
					sequence = line.strip()
				elif i == 2: 
					dummy = line.strip()
				elif i == 3:
					quality = line.strip()

					if sequence in self.seqCounts and self.seqCounts[sequence] >= self.minCopy:
						print header
						print sequence
						print dummy
						print quality

				i += 1
				if i == 4:
					i = 0
					
		else:
			print "Incorrect outputType!"
			print ""
			print __doc__
			sys.exit(1)

import sys

if __name__=="__main__":
        if len(sys.argv)!=4:
                print __doc__
                sys.exit(1)

	inputFile = sys.argv[1]
        minCopy = int(sys.argv[2])
	outputType = sys.argv[3]
	
        copyKeeper = CopyKeeper(inputFile, minCopy)
	copyKeeper.processFile()
        copyKeeper.printResults(outputType)

