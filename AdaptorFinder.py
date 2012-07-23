#!/usr/bin/python
# encoding: utf-8
# author: Sébastien Boisvert
# 2012-01-24
# modified by: Charles Joly Beauparlant
# 2012-07-17

import sys

if len(sys.argv)!=4:
	print ""
	print "This program keeps only sequence containing the full sequence of an adaptor."
	print "Only useful in the cases of small sequences (i.e.: miRNA) where the presence of the adaptor is expected."
	print "Make sure that the expected length of the sequence + the length of the adaptor is <= than the length of the read."
	print "This program keeps only things before the adaptor."
	print "Usage "
	print "cat joe.fastq | ./AdaptorRemover.py <adaptorSequence> <trimSize> <maxMismatches> > joe.trimmed.fastq"
	print "trimSize: If no match is found with adaptor, the script will try again removing 1 base at a time,"
	print "          until a match is found or trimSize base are removed."
	print "maxMismatches: Maximum number of mismatches that can be tolerated."
	print ""
	sys.exit()

def mismatches(s1,s2):
	i=0
	mismatches=0
	while i<len(s1):
		if s1[i]!=s2[i]:
			mismatches+=1
		i+=1
	return mismatches

def findOffset(sequence,adaptor,maxMismatches):
	i=0
	sequenceLength=len(sequence)
	adaptorLength=len(adaptor)

	#no mismatch
	while i<=sequenceLength-adaptorLength:
		observed=sequence[i:adaptorLength]
		if observed==adaptor:
			return i

		i+=1

	i=0

	# mismatch
	while i<=sequenceLength-adaptorLength:
		observed=sequence[i:i+adaptorLength]

		nonHits=mismatches(observed,adaptor)
#		if nonHits<=adaptorLength/2:
		if nonHits<=maxMismatches:
			return i

		i+=1

	return sequenceLength-1
	

def process(header,sequence,dummy,quality,adaptor,maxMismatches):
	offset=findOffset(sequence,adaptor,maxMismatches)
	
	lengthDiff=len(sequence)-len(adaptor)

	# If count == 0, then there is only the adaptor
	# Sequence shorter than 10 nucleotides are removed
	if offset>10:
		# If count > lengthDiff, then the full sequence of the adaptor is not present
		if offset<=lengthDiff:
			print header
			print sequence[0:offset]
			print dummy
			print quality[0:offset]
			return True

	return False	
	

adaptor=sys.argv[1]
trimSize=int(sys.argv[2])
maxMismatches=int(sys.argv[3])

if (maxMismatches>len(adaptor)):
	print "maxMismatches value bigger than adaptor size."
	sys.exit()

i=0

l0=""
l1=""
l2=""
l3=""

for line in sys.stdin:
	if i==0:
		l0=line.strip()
	elif i==1:
		l1=line.strip()
	elif i==2:
		l2=line.strip()
	elif i==3:
		l3=line.strip()

		j=0
		tmpAdaptor=adaptor
		# If the full sequence of the adaptor was not found, we truncate it and try to find it again (up to 3 tries)
		while (j<=trimSize and process(l0,l1,l2,l3,tmpAdaptor,maxMismatches)==False):
			j=j+1
			tmpAdaptor=adaptor[j:len(adaptor)]

	i+=1

	if i==4:
		i=0
		
		
