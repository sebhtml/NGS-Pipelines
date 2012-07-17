#!/usr/bin/env python
# encoding: utf-8
# usage: ./filter-by-allele-frequency.py var.raw.vcf " frequency >= 0.0 "|wc -l


import sys

arguments=sys.argv

file=arguments[1]
condition=arguments[2]

stream=open(file)

for line in stream:
	# GeneDB|LinJ.00  13510   .       C       G       999     .       DP=17;VDB=0.0145;AF1=1;AC1=14;DP4=0,0,7,10;MQ=47;FQ=-34.1       GT:PL:GQ        1/1:0,0,0:12
	if line[0]=='#':
		print line,

	else:

		tokens=line.split("\t")

		features=tokens[7].split(";")
	
		for item in features:
			newTokens=item.split("=")

			if len(newTokens)!=2:
				continue

			key=newTokens[0]
			value=newTokens[1]

			if key=='AF1':
				frequency=float(value)

		if eval(condition):
			print line,
			
stream.close()
