#!/usr/bin/python
# encoding: utf-8
# ticket 244
# Sébastien Boisvert

# from the pileup, get the gene down stream and upstream, 1000 bp maximum

# based on intervals trees

import sys

# pileup
pileup=sys.argv[1]

# Genes
gff=sys.argv[2]


geneIntervals={}
fivePrimeIntervals={}
threePrimeIntervals={}

window=1000

for line in open(gff):
	l=line.split()
	# psu|Lmjchr1     ApiDB   mRNA    9061    11067
	chromosome=l[0].strip()
	start=int(l[3])
	end=int(l[4])
	type=l[2].strip()
	strand=l[6].strip()
	description=l[8].strip()
	if chromosome not in geneIntervals:
		geneIntervals[chromosome]=[]
		fivePrimeIntervals[chromosome]=[]
		threePrimeIntervals[chromosome]=[]
	geneIntervals[chromosome].append((start,end))
	if type=="gene":
		if strand=="+":
			fivePrimeIntervals[chromosome].append((start-window,start-1,description))
			threePrimeIntervals[chromosome].append((end+1,end+window,description))
		else:
			threePrimeIntervals[chromosome].append((start-window,start-1,description))
			fivePrimeIntervals[chromosome].append((end+1,end+window,description))


for i in geneIntervals.items():
	chromosome=i[0]
	geneIntervals[chromosome]=sorted(geneIntervals[chromosome],key=lambda item: item[0])
	fivePrimeIntervals[chromosome]=sorted(fivePrimeIntervals[chromosome],key=lambda item: item[0])
	threePrimeIntervals[chromosome]=sorted(threePrimeIntervals[chromosome],key=lambda item: item[0])

def searchIntervals(intervals,chromosome,position):
	theIntervals=intervals[chromosome]
	numberOfIntervals=len(theIntervals)
	lowerBound=0
	upperBound=numberOfIntervals-1
	#print ""
	#print "Searching "+str(position)+" on "+chromosome
	#print str(numberOfIntervals)+" intervals"
	while lowerBound<=upperBound:
		middle=(upperBound+lowerBound)/2
		startValue=theIntervals[middle][0]
		endValue=theIntervals[middle][1]
		#print "Interval "+str(middle)+" "+str(startValue)+" "+str(endValue)
		if position<startValue:
			#print "Going left"
			upperBound=middle-1
		elif position<=endValue:
			#print "Found"
			return theIntervals[middle][2]
		else:
			#print "Going right"
			lowerBound=middle+1
	return "NULL"

def filterKey(key):
	t=key.split(";")
	if len(t)==1:
		return key
	v=t[1]+" "+t[2]
	v=v.replace("Name=","").replace("description=","").replace("%2C",",")
	return v.replace("+"," ").replace("%28","(").replace("%29",")").replace('%2F',"/")

print "Chromosome\tPosition\tReference\tSample\tUpstreamOfGene\tDownstreamOfGene"

for line in open(pileup):
	# psu|Lmjchr1     96    
	l=line.split()
	chromosome=l[0]
	position=int(l[1])
	fivePrime=filterKey(searchIntervals(fivePrimeIntervals,chromosome,position))
	threePrime=filterKey(searchIntervals(threePrimeIntervals,chromosome,position))
	if fivePrime=="NULL" and threePrime=="NULL":
		continue
	original=l[2]
	newNucleotide=l[3]
	print chromosome+"\t"+str(position)+"\t"+original+"\t"+newNucleotide+"\t"+fivePrime+"\t"+threePrime
