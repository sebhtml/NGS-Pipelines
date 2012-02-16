#!/usr/bin/python
# encoding: utf-8
# ticket 244
# Sébastien Boisvert


import sys

# pileup
pileup=sys.argv[1]

# Genes
gff=sys.argv[2]


intervals={}

for line in open(gff):
	l=line.split()
	# psu|Lmjchr1     ApiDB   mRNA    9061    11067
	chromosome=l[0].strip()
	start=int(l[3])
	end=int(l[4])
	if chromosome not in intervals:
		intervals[chromosome]=[]
	intervals[chromosome].append((start,end))

sortedIntervals={}

for i in intervals.items():
	chromosome=i[0]
	elements=i[1]
	sortedElements=sorted(elements,key=lambda item: item[0])
	sortedIntervals[chromosome]=sortedElements

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
			return True
		else:
			#print "Going right"
			lowerBound=middle+1
	return False

for line in open(pileup):
	# psu|Lmjchr1     96    
	l=line.split()
	chromosome=l[0]
	position=int(l[1])
	found=searchIntervals(sortedIntervals,chromosome,position)
	if not found:
		print line.strip()
