#!/usr/bin/env python
# encoding: utf-8
# author: Sébastien Boisvert, Université Laval
# license: GPL

import sys

if len(sys.argv)!=5:
	print "Usage"
	print sys.argv[0]+" variations(withGenes).vcf positions.gff codes geneSequences.fasta > variationsWithCodons.txt"
	print "The gff file must be sorted."
	sys.exit()


pileup=sys.argv[1]
positions=sys.argv[2]
codes=sys.argv[3]
geneSequences=sys.argv[4]

def complement(a):
	if a=="A":
		return "T"
	if a=="T":
		return "A"
	if a=="C":
		return "G"
	if a=="G":
		return "C"

sequences={}

name=""
seq=""
# >psu|LmjF20.0460 | organism=Leishmania_major | product=hypothetical protein, conserved | location=Lmjchr20:173910-175037(+) | length=1128
for line in open(geneSequences):
	if line[0]=='>':
		if name!="":
			sequences[name]=seq
		name=line.split()[0].replace('>','').replace("GeneDB|","")
		seq=""
	else:
		seq+=line.strip()
sequences[name]=seq

codeEntries={}
for line in open(codes):
	tokens=line.split()
	a=tokens[0].strip()
	b=tokens[1].strip()
	if a not in codeEntries:
		codeEntries[a]=[]
	codeEntries[a].append(b)

genePositions={}

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

		geneName=tokens[8].split(";")[0].replace('ID=','').replace("rna_","").replace("-1","").replace("apidb|","")

		if chromosome not in genePositions:
			genePositions[chromosome]={}
		genePositions[chromosome][geneName]=[startPosition,endPosition,strand]


#LmjF.01.0800    673     GeneDB|LmjF.01  245206  .       G       T       10.4    .       DP=9;VDB=0.0132;AF1=0.5;AC1=1;DP4=3,3,0,2;MQ=37;FQ=13.2;PV4=0.46,0.43,1,0.15    GT:PL:GQ        0/1:40,0,151:42

# update: 
# vcf
# in gff: apidb|LinJ.01
# in vcf: GeneDB|xyz

# gene	geneposition	GeneDB|LinJ.00  13503   .       G       C 

for line in open(pileup):
	if len(line)==0:
		continue
	if line[0]=='#':
		continue

	tokens=line.split()
	chromosome=tokens[2].replace("GeneDB|","apidb|")
	position=int(tokens[3])
	ref=tokens[5]
	observed=tokens[6]
	geneName=tokens[0].strip()

	if not chromosome in genePositions:
		print "Error "+chromosome+" is not in the gff file"
		continue

	if not geneName in genePositions[chromosome]:
		print "Error "+geneName+" is not in the gff file for chromosome "+chromosome
		continue
		
	geneStart=genePositions[chromosome][geneName][0]
	geneEnd=genePositions[chromosome][geneName][1]
	geneStrand=genePositions[chromosome][geneName][2]


#     ------------------------------------------------------>
#               s                 p                 e

	# position are 1-based
	positionInGene=position-geneStart+1
	if geneStrand=="-":
		positionInGene=geneEnd-position+1

	nucleotidePositionInCodon=(positionInGene-1)%3+1
	codonPosition=positionInGene-nucleotidePositionInCodon+1

	geneNameCorrected=geneName.replace('apidb|rna_','').replace("-1","")

	if not geneNameCorrected in sequences:
		print "Error: "+geneNameCorrected+" is not in the gene fasta file."
		continue

	geneSequence=sequences[geneNameCorrected]

	if positionInGene>=len(geneSequence):
		print "Error: positional error, length="+str(len(geneSequence))+", position="+str(positionInGene)
		continue
	wildNucleotideAccordingToGene=geneSequence[positionInGene-1]
	wildCodonAccordingToGeneSequence=geneSequence[(codonPosition-1):(codonPosition-1)+3]
	if geneStrand=="-":
		ref=complement(ref)
	if wildNucleotideAccordingToGene!=ref:
		print "Error: nucleotide is not the same in the CDS and chromosomes files."
		continue
	if wildCodonAccordingToGeneSequence[nucleotidePositionInCodon-1]!=ref:
		print "Error: nucleotide is not the same in the CDS and chromosomes files."
		continue

	if observed not in codeEntries:
		print "Error: nucleotide code "+observed+" is not in IUPAC"
		continue

	for newNucleotide in codeEntries[observed]:
		if geneStrand=="-":
			newNucleotide=complement(newNucleotide)
		newCodon=wildCodonAccordingToGeneSequence[0:nucleotidePositionInCodon-1]+newNucleotide+wildCodonAccordingToGeneSequence[nucleotidePositionInCodon:3]
		print line.strip()+"\t"+wildCodonAccordingToGeneSequence+"\t"+newCodon
