#!/usr/bin/python
# custom filter for pileup files created by samtools.

import sys

# http://samtools.sourceforge.net/cns0.shtml
for line in open(sys.argv[1]):
	tokens=line.split()
	quality=int(tokens[5])
	if quality<20:
		continue
	numberOfReads=int(tokens[0x8-0x1])
	if numberOfReads<10:
		continue

	type=tokens[3]
	if type.find("+")>=0 or type.find("-")>=0:
		
		var1=tokens[8]
		var2=tokens[9]
		count1=int(tokens[10])
		count2=int(tokens[11])
		# #1 is the reference-like bit
		if var1.find("+")>=0 or var1.find("-")>=0:
			t=var1
			var1=var2
			var2=t
			t=count1
			count1=count2
			count2=t
		if count2>=count1/3 and count1+count2>=10:
			print line.strip()
	else:
		print line.strip()

