#!/usr/bin/env python
# encoding: utf-8
# author: Sébastien Boisvert, Université Laval
# license: GPL

# takes a VCF file and a GFF file

import sys

if len(sys.argv)!=3:
	print "Usage"
	print sys.argv[0]+" input.vcf input.gff > output.vcf"
	print "The gff file must be sorted."
	sys.exit()

pileup=sys.argv[1]
positions=sys.argv[2]

# apidb|Lmjchr1   ApiDB   gene    172000  172731  .       +       .       ID=apidb|LmjF01.0610;Name=LmjF01.0610;description=DNA-damage+inducible+protein+DDI1-like+protein;size=732;web_id=LmjF01.0610;locus_tag=LmjF01.0610;size=732;Alias=LmjF1.0610

genePositions={}

geneStartAndEnd={}


for line in open(positions):
	tokens=line.split()
	if len(tokens)!=9:
		continue
	type=tokens[2]
	if type=="mRNA":
		chromosome=tokens[0]
		startPosition=int(tokens[3])
		endPosition=int(tokens[4])
		strand=tokens[6]
		geneName=tokens[8].split(";")[0].replace('ID=','')
		i=startPosition
		if chromosome not in genePositions:
			genePositions[chromosome]={}
		while i<=endPosition:
			genePositions[chromosome][i]=geneName
			i+=1
		geneStartAndEnd[geneName]=[startPosition,endPosition,strand]


#psu|Lmjchr1     25910   *       */-CT   91      91      37      77      *       -CT     76      1       0       0       0

for line in open(pileup):
	if line[0]=="#":
		continue

	tokens=line.split()
	chromosome=tokens[0].replace("GeneDB|","apidb|")
	position=int(tokens[1])
	if chromosome in genePositions:
		if position in genePositions[chromosome]:
			geneName=genePositions[chromosome][position]
			positionInGene=position-geneStartAndEnd[geneName][0]+1
			if geneStartAndEnd[geneName][2]=="-":
				positionInGene=geneStartAndEnd[geneName][1]-position+1
			print geneName.replace("apidb|rna_","").replace("-1","")+"\t"+str(positionInGene)+"\t"+line.strip()
