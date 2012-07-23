#!/usr/bin/python
# encoding: utf-8
# author: Sébastien Boisvert
# 2012-01-24
# modified by: Charles Joly Beauparlant
# 2012-07-23

import sys

if len(sys.argv)!=2:
	print ""
	print "This program trims sequences based on their Phred Qualilty Score."
	print "The longest stretch of sequence with score higher or equal to <minQual> will be printed."
	print "Usage "
	print "cat joe.fastq | ./AdaptorRemover.py <minQual> > joe.trimmed.fastq"
	print ""
	sys.exit()

def process(header,sequence,dummy,quality,minQual):
	current=0
	longest=0
	longestCount=0
#	print "Sequence: " + sequence
#	print "Quality: " + quality 
	# If it's not possible to get a better score, stop looping
	while len(sequence)-longestCount > current:
#		print "Current: " + str(current)
		miss=False
		i=0
		# Stop checking when you find a score below treshold or if you are at the end of the sequence
		while miss==False and current+i < len(sequence)-1:
#			print "i: " + str(i)
#			print "quality[current+i]: " + quality[current+i]
#			print "Phred: " + str(ord(quality[current+i]))
#			print str(ord(quality[current+i]))
			if ord(quality[current+i]) < minQual+33:
				miss=True
#				print "miss == True"
			i=i+1
			if i > longest:
				longest=current
				longestCount=i
#				print "Longest: " + str(longest)
#				print "Count: " + str(longestCount)

		current=current+1
	
	# Only print if you have a sequence of at least 10 nucleotides with high enough quality score 
	if longestCount >= 10:
		print header
		print sequence[longest:longest+longestCount]	
		print dummy
		print quality[longest:longest+longestCount]	


minQual=int(sys.argv[1])

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

		process(l0,l1,l2,l3,minQual)

	i+=1

	if i==4:
		i=0
		
		
