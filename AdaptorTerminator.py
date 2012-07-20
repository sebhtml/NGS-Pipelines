#!/usr/bin/python
# encoding: utf-8
# author: Sébastien Boisvert
# 2012-01-24

import sys

if len(sys.argv)!=2:
	print ""
	print "This program keeps only things before the adaptor."
	print "usage "
	print "cat joe.fastq | ./AdaptorRemover.py <adaptorSequence> > joe.trimmed.fastq"
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

def findOffset(sequence,adaptor):
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
		if nonHits<=adaptorLength/2:
			#print i
			#print adaptor
			#print observed
			#print "Mismatches: "+str(nonHits)
			return i

		i+=1

	return sequenceLength-1
	

def process(header,sequence,dummy,quality,adaptor):
	offset=findOffset(sequence,adaptor)

#	count=offset+1
#	if offset==0:
#		count=0

	if offset!=0:
		print header
#		print sequence[0:count]
		print sequence[0:offset]
		print dummy
#		print quality[0:count]
		print quality[0:offset]

adaptor=sys.argv[1]

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

		process(l0,l1,l2,l3,adaptor)

	i+=1

	if i==4:
		i=0
		
		
