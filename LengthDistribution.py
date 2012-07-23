#!/usr/bin/python
# encoding: utf-8
# author: Charles Joly Beauparlant
# 2012-07-23

"""
This script calculates the distribution of sequence's length from a fastq file
Usage:
cat joe.fastq | ./LengthDistribution.py <maxLength> > out.distribution
maxLength: Maximum sequence length to compute
"""

class DistributionCalculator:
        def __init__(self, maxLength):
                self.maxLength = maxLength
                self.clear()

        def clear(self):
                self.distribution = [0] * self.maxLength

        def processSequence(self, sequence):
                length = len(sequence)
                if length <= self.maxLength:
                        self.distribution[length] += 1

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
                if i==1:
                        sequence = line.strip()
                        distributionCalculator.processSequence(sequence)

                i+=1

                if i==4:
                        i=0

        distributionCalculator.printResults()

