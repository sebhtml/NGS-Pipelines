#!/usr/bin/python
# encoding: utf-8
# author: Charles Joly Beauparlant
# 2012-07-23

"""
This script calculates the distribution of sequence's length from a fasta file
Usage:
cat joe.fasta | ./LengthDistribution.py <maxLength> > distribution.txt
maxLength: Maximum sequence length to compute
"""

class DistributionCalculator:
        def __init__(self, maxLength):
                self.maxLength = maxLength
                self.clear()

        def clear(self):
                self.distribution = [0] * self.maxLength

        def processSequence(self, sequence, count):
                length = len(sequence)
                if length <= self.maxLength:
                        self.distribution[length] += count

        def printResults(self):
                for i in range(self.maxLength):
                        print str(i) + "\t" + str(self.distribution[i])

import sys

if __name__=="__main__":
        if len(sys.argv)!=2:
                print __doc__
                sys.exit(1)

        maxLength=int(sys.argv[1])
        distributionCalculator = DistributionCalculator(maxLength)

        i =0
        for line in sys.stdin:
		if i==0:
			count = int(line.split()[3])
                if i==1:
                        sequence = line.strip()
                        distributionCalculator.processSequence(sequence, count)

                i+=1

                if i==2:
                        i=0

        distributionCalculator.printResults()

