# encoding: utf-8
# Sébastien Boisvert
# for Adriano & Angana
# 2011-04-19

#lines with lengths:
# @SQ     SN:psu|Lmjchr1  LN:268984

windowSize=4000

chromosomeLengths={}

chromosomeWindows={}

i=0

import sys
for line in sys.stdin:
	tokens=line.split()
	# example:
	# GA6_00013:1:1:1276:945#0        16      psu|Lmjchr36    2636591 37      76M     *       0       0       TCGCTGCATCATTACTCGCCCACCACAACTTGCTCACGAGTCGCATACCTCGACCACGCCACGANCTGGAAGCGCN    ############################################################################    XT:A:U  NM:i:2  X0:i:1  X1:i:0  XM:i:2  XO:i:0  XG:i:0  MD:Z:64A10A0
	if len(tokens)==3:
		name=tokens[1].replace("SN:","").strip()
		length=int(tokens[2].replace("LN:",""))
		chromosomeLengths[name]=length
	elif len(tokens)>3:
		chromosome=tokens[2].strip()
		if chromosome not in chromosomeLengths:
			continue
		position=int(tokens[3])
		windowNumber=((position-1)/windowSize)*windowSize+1
		if chromosome not in chromosomeWindows:
			chromosomeWindows[chromosome]={}
		if windowNumber not in chromosomeWindows[chromosome]:
			chromosomeWindows[chromosome][windowNumber]=0

		chromosomeWindows[chromosome][windowNumber]+=1
	i+=1

chromosomes=chromosomeWindows.keys()
chromosomes.sort()

for i in chromosomes:
	positions=chromosomeWindows[i].keys()
	positions.sort()
	for j in positions:
		position2=j+windowSize-1
		if position2>chromosomeLengths[i]:
			position2=chromosomeLengths[i]
		count=chromosomeWindows[i][j]
		print i+"\t"+str(j)+"\t"+str(position2)+"\t"+str(count)
