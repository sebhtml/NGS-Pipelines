#!/usr/bin/python

# arguments: 
# - vcf file (possibly filtered for uniqueness)
# - gff file

# the gff file must be sorted beforehand

import sys

variationFile=sys.argv[1]
geneFile=sys.argv[2]


genes={}

def getEntry(blob,key):
	tokens=blob.split(";")
	for i in tokens:
		tokens2=i.split("=")
		if len(tokens2)==2:
			if tokens2[0]==key:
				return tokens2[1]
	return ""


def getName(blob):
	return getEntry(blob,"Name")

def getDescription(blob):
	return getEntry(blob,"description")

# build a database of genes

for line in open(geneFile):
	tokens=line.split()
	if len(tokens) < 3:
		continue
	type=tokens[2]
	if type != 'gene':
		continue

	chromosome=tokens[0].replace("apidb|","")
	startPosition=int(tokens[3])
	endPosition=int(tokens[4])
	strand=tokens[6]
	description=tokens[8]

	if chromosome not in genes:
		genes[chromosome] = []
	genes[chromosome].append([startPosition,endPosition,strand,description])

# open the VCF file

for line in open(variationFile):
	if line[0]=='#':
		continue

	tokens=line.split()
	chromosome=tokens[0].replace("GeneDB|","")
	position=int(tokens[1])
	before=tokens[3]
	after=tokens[4]
	
	entries=genes[chromosome]

	i=0

	# check if the entry is between two genes
	while i<len(entries)-1:
		currentGene=entries[i]
		nextGene=entries[i+1]
		if currentGene[1] < position and position < nextGene[0]:

			# the entry is between 2 genes
	
			# print the vcf as is

			print line.strip()

			break
		i+=1
