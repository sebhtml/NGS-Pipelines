#!/usr/bin/env python

annotations='000-Annotations.txt'  # each line contains emblCdsKey	goKey
sequences='cds.fasta' # EMBL_CDS fasta file from ebi.ac.uk
output='Sequences-With-Annotations.fasta'  #output

withAnnotations={}

for line in open(annotations):
	tokens=line.split("\t")
	key=tokens[0]

	withAnnotations[key]=1

display=False

f=open(output,"w")

for line in open(sequences):
	if line[0]=='>':
		#>EMBL_CDS:CAA00001 CAA00001.1 Bacillus subtilis hypothetical protein

		tokens=line.split(" ")
		group=tokens[0]
		newTokens=group.split(":")
		emblCdsKey=newTokens[1]

		if emblCdsKey in withAnnotations:
			display=True
		else:
			display=False

	if display:
		f.write(line)

f.close()


