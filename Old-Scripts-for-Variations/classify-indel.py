#!/usr/bin/python
#encoding=utf-8
# classify entries in pileup as being indels or nucleotide changes

# author: Sébastien Boisvert
# 5 octobre 2010

import sys

pileup=sys.argv[1]



deletions=open(pileup+"-deletions.xls","w+")
insertions=open(pileup+"-insertions.xls","w+")
nucleotideChanges=open(pileup+"-changes.xls","w+")

# GeneDB|LmjF.01  69906   .       ATCTCTCTCTCTCTCTCTCTCTCTCTCTCTCTC       ATCTCTCTCTCTCTCTCTCTCTCTCTCTCTC 110     .       INDEL;DP=83;VDB=0.0520;AF1=0.5;AC1=1;DP4=21,9,6,7;MQ=37;FQ=113;PV4=0.18,0.33,1,1        GT:PL:GQ        0/1:148,0,255:99

for i in open(pileup):

	tokens=i.split()

	before=tokens[3+2]
	after=tokens[2+4]


	if len(after) > len(before):
		insertions.write(i)
	elif len(after) < len(before):
		deletions.write(i)
	else: # not an indel
		nucleotideChanges.write(i)

nucleotideChanges.close()
insertions.close()
deletions.close()

