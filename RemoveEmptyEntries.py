#!/usr/bin/python

import sys

# this script remove empty sequences
# from a fastq sequence provided in
# stdin

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
	
		if len(l1)>0:
			print l0
			print l1
			print l2
			print l3
	i+=1
	if i==4:
		i=0


