#!/usr/bin/env python
# encoding: utf-8

print '<?xml version="1.0" encoding="UTF-8"?>'
print "<profile>"
print "<method>MetaPhlAn version 1.1.0 (March 2012) from http://www.hmpdacc.org/HMSMCP</method>"

samples=[]

import sys

data={}

samples=[]

types={}
types["k"]="kingdom"
types["p"]="phylum"
types["c"]="class"
types["o"]="order"
types["f"]="family"
types["g"]="genus"
types["s"]="species"

for line in open("HMP.ab.txt"):
	tokens=line.split("\t")

	if tokens[0]=='sid':
		i=1

		while i<len(tokens):
			sample=tokens[i].strip()

			data[sample]=[]

			samples.append(sample)
	
			i+=1
	else:

		tokens2=tokens[0].split("|")
		taxon=tokens2[len(tokens2)-1]
		newTokens=taxon.split("__")
		theType=newTokens[0]

		typeName=types[theType]

		name=newTokens[1].replace("_"," ")

		#typeName+" "+name

		i=1
		while i<len(tokens):
			sample=samples[i-1]

			value=tokens[i].strip()

			i+=1

			if value=="0.0":
				continue

			data[sample].append([name,typeName,value])

for sample in samples:
	print "<sample><name>"+sample+"</name>"
	print "<taxons>"

	for item in data[sample]:
		print "<taxon><rank>"+item[1]+"</rank><name>"+item[0]+"</name><value>"+item[2]+"</value></taxon>"

	print "</taxons>"
	print "</sample>"

print "</profile>"
