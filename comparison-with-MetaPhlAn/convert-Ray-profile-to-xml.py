#!/usr/bin/env python
# encoding: utf-8

import sys

#print '<?xml version="1.0" encoding="UTF-8"?>'
#print "<profile>"
#print "<method>Ray v2.0.0</method>"

samples=[]

import sys

data={}

samples=[]

sample=sys.argv[1]
rayOutput=sys.argv[2]

samples.append(sample)

data[sample]=[]

path=rayOutput+"/BiologicalAbundances/"

types=["kingdom","phylum","class","order","family","genus","species"]

for item in types:
	file=path+"/"+"0.Profile.TaxonomyRank="+item+".tsv"
	
	for line in open(file):
		if line[0]=='#':
			continue

		tokens=line.split("\t")

		typeName=tokens[2].strip()
		value=100.0*float(tokens[3])
		name=tokens[1].replace(" (class)","").strip()

		data[sample].append([name,typeName,str(value)])


for sample in samples:
	print "<sample><name>"+sample+"</name>"
	print "<taxons>"

	for item in data[sample]:
		print "<taxon><rank>"+item[1]+"</rank><name>"+item[0]+"</name><value>"+item[2]+"</value></taxon>"

	print "</taxons>"
	print "</sample>"

#print "</profile>"
