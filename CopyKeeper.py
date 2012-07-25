#!/usr/bin/python
# encoding: utf-8
# author: Charles Joly Beauparlant
# 2012-07-23

"""
This script filter a fastq file to keep only sequences with at least <minCopy> copy.
Saves data as fasta with the copy count in the header. 
Usage:
cat joe.fastq | ./CopyKeeper.py <minCopy> > out.fasta
"""

class CopyKeeper:
	def __init__(self, minCopy):
		self.minCopy = minCopy
		self.clear()

	def clear(self):
#		self.seqCounts = defaultdict(int)
		self.seqCounts = {}

	def processSequence(self, sequence):
		if sequence in self.seqCounts:
			self.seqCounts[sequence] += 1
		else:
			self.seqCounts[sequence] = 1

	def printResults(self):
		sorted(self.seqCounts, key = self.seqCounts.get)
		i = 0
		for seq in sorted(self.seqCounts, key = self.seqCounts.get, reverse = True):
			if self.seqCounts[seq] >= self.minCopy:
				print "> PP_" + str(i) + " Count: " + str(self.seqCounts[seq])
				print seq
				i += 1

import sys

if __name__=="__main__":
        if len(sys.argv)!=2:
                print __doc__
                sys.exit(1)

        minCopy = int(sys.argv[1])
        copyKeeper = CopyKeeper(minCopy)

        i =0
        for line in sys.stdin:
                if i==1:
                        sequence = line.strip()
                        copyKeeper.processSequence(sequence)

                i+=1

                if i==4:
                        i=0

        copyKeeper.printResults()

