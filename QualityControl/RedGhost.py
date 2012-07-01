#!/usr/bin/env python

"""
"""

import sys

if len(sys.argv)!=2:
	print "Check the quality of a fastq file."
	print " by looking for consecutive non-N nucleotides."
	print "Usage: cat file.fastq | "+sys.argv[0]+" kmerLength"
	sys.exit(1)

i=0

kmerLength=int(sys.argv[1])

good={}
good["A"]=1
good["T"]=1
good["C"]=1
good["G"]=1

frequencies={}

lines=0
for line in sys.stdin:

	if i==1:
		sequence=line.strip()
		maximumWords=len(sequence)-kmerLength+1
		validWords=0

		badPositions=[]

		j=0
		while j<len(sequence):
			letter=sequence[j]
			if letter not in good:
				badPositions.append(j)
	
			j+=1

		kmerStates={}
	
		# set them all to OK
		j=0

		while j<maximumWords:
			kmerStates[j]=True
	
			j+=1

		# using the bad position, set some to FAIL

		j=0
		while j<len(badPositions):
			nucleotidePosition=badPositions[j]

			first=nucleotidePosition-kmerLength+1
			second=nucleotidePosition+kmerLength-1

			iterator=first

			while iterator<=second:

				if iterator>=0 and iterator < maximumWords:
					kmerStates[iterator]=False
				iterator+=1
			j+=1

		# count the number of FAIL states

		j=0

		failed=0
		while j<maximumWords:
			if kmerStates[j]==False:
				failed+=1
			j+=1

		passTests=maximumWords-failed

		if passTests not in frequencies:
			frequencies[passTests]=0
		frequencies[passTests]+=1

	i+=1

	if i==4:
		if lines % 1000 == 0:
			print "Processed "+str(lines)+" sequences"

		i=0
		lines+=1
