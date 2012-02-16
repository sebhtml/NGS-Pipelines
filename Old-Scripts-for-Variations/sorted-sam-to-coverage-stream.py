#!/usr/bin/python

# this is an online algorithm to convert a sam file to a coverage stream
# no memory allocation

# TODO: indel support is buggy (for coverage)
# TODO: the last positions of a chromosome are not reported if they have 0 reads

# input: sorted sam in stdin

import sys

chromosomes={}

buffers={}

currentPosition=None
currentChromosome=None
positionIterator=None

def flushBuffers(buffers,currentChromosome,positionIterator,lastPosition):
	while positionIterator <= lastPosition:
		if positionIterator in buffers:
			signal=buffers[positionIterator]
			del buffers[positionIterator]

			print currentChromosome+"	"+str(positionIterator)+"	"+str(signal)

		positionIterator += 1

for line in sys.stdin:
	tokens=line.split()
	if tokens[0]=='@SQ':
		chromosome=tokens[1].replace('SN:','')
		length=int(tokens[2].replace('LN:',''))
	
		chromosomes[chromosome]=length
	elif len(tokens) >= 10:
		chromosome=tokens[2]
		if chromosome!='*':

			position=int(tokens[3])

			sequenceLength=len(tokens[9])

			# first entry
			if currentPosition == None:
				positionIterator=1
				currentPosition=position
				currentChromosome=chromosome

			# flush everything from positionIterator to position-1
			if chromosome==currentChromosome:
				flushBuffers(buffers,currentChromosome,positionIterator,position-1)
				positionIterator=position

			# new chromosome, we need to flush all the buffers
			if chromosome != currentChromosome:
				flushBuffers(buffers,currentChromosome,positionIterator,chromosomes[currentChromosome])
	
				positionIterator=1
				currentChromosome=chromosome
				currentPosition=position

			# here, we update the buffers
			i=0
			while i<sequenceLength:
				thePosition=position+i
				if thePosition not in buffers:
					buffers[thePosition] = 0
				buffers[thePosition] += 1

				i+=1

flushBuffers(buffers,currentChromosome,positionIterator,chromosomes[currentChromosome])
