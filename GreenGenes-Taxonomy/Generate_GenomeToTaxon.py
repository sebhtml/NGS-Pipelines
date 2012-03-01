#!/usr/bin/env python
# encoding: utf-8
# author: Sébastien Boisvert
# license: GPLv3

"""
usage:

Generate_GenomeToTaxon.py \
sequences_16S_all_gg_2011_1_unaligned.fasta \
gi_to_accession.txt \
Taxons.tsv \
WholeGenome_GenomeToTaxon.tsv \
GreenGene_GenomeToTaxon.tsv \
GreenGenes.fasta


Purposes

1. plugin NCBI genomes in the GreenGenes taxonomy
2. make a namespace for GreenGenes sequences



Inputs

1.
sequences_16S_all_gg_2011_1_unaligned.fasta

contains sequences from Greengenes


2.
gi_to_accession.txt 

contains lines. Each line is:

Genome Identifier	NCBI accession

3.
Taxons.tsv

This is the taxons of the GreenGenes taxonomy.
(converted from the original format)

This file contains lines, each line is:

taxon identifier	taxon name	taxonomic rank


Outputs

1.

WholeGenome_GenomeToTaxon.tsv 

each line will be like:


Genome identifier	Taxon identifier

This is for the NCBI genomes.


2.

GreenGene_GenomeToTaxon.tsv

Each line is like:

Genome identifier	Taxon identifier


Genome identifiers for GreenGenes sequences are namespaced with 100000000000


so 4 is 100000000000 + 4

The maximum value for GenomeToTaxon in NCBI is 373445154 so we are safe.

3. 

GreenGenes.fasta

Fasta file containing things from sequences_16S_all_gg_2011_1_unaligned.fasta

but header are rewritten like this:

>4 bla bla bla

to 

>gi|100000000004| bla bla

Ray will pick up the gi|xxx| thing.

"""

import sys

if len(sys.argv)!=7:
	print __doc__
	sys.exit(1)


greenGeneTaxonNames={}
greenGeneTaxonRanks={}
greenGeneKeyToNumber={}

greenGeneTaxonFile=sys.argv[3]

ranks={}
ranks['k__']='kingdom'
ranks['p__']='phylum'
ranks['c__']='class'
ranks['o__']='order'
ranks['f__']='family'
ranks['g__']='genus'
ranks['s__']='species'

reverseTable={}

for i in ranks.items():
	reverseTable[i[1]]=i[0]

i=0
for line in open(greenGeneTaxonFile):
	tokens=line.split("\t")
	identifier=int(tokens[0])
	name=tokens[1].strip()
	rank=tokens[2].strip()

	code=reverseTable[rank]

	key=code+name

	greenGeneKeyToNumber[key]=identifier
	greenGeneTaxonNames[key]=name
	greenGeneTaxonRanks[key]=rank

	i+=1

print "loaded "+str(i)+" greengenes taxons"

accessionToIdentifier={}

identifierToAccessionFile=sys.argv[2]

i=0
for line in open(identifierToAccessionFile):
	tokens=line.split()
	genomeIdentifier=int(tokens[0])
	ncbiAccession=tokens[1].strip()

	accessionToIdentifier[ncbiAccession]=genomeIdentifier
	i+=1

print "loaded "+str(i)+" NCBI accessions"


# >14 AF068820.2 hydrothermal vent clone VC2.1 Arc13 k__Archaea; p__Euryarchaeota; c__Thermoplasmata; o__Thermoplasmatales; f__Aciduliprofundaceae; otu_204

fastaFile=sys.argv[1]

header=""
parity=0

genomeToTaxonForNCBI=open(sys.argv[4],"w")
genomeToTaxonForGreenGenes=open(sys.argv[5],"w")
fastaFileWithNamespace=open(sys.argv[6],"w")

namespace=100000000000

keyNotFound=0
debug=False

processed=0
PERIOD=1000

# assume 2 lines per sequence
for line in open(fastaFile):
	if parity==1:
		sequence=line.strip()
		parity=0

		# process the sequence
		tokens=header.split()
		accession=tokens[1]

		greenGeneGenomeNumber=int(tokens[0].replace('>',''))

		if debug:
			print header

		start=header.find("k__")

		tokens=header[start:].split(";")

		deepestKey=None
		for part2 in tokens:
			part=part2.strip()

			if len(part)<=3:
				continue

			code=part[0:3]

			if code in ranks:
				key=part.replace(";","")
				deepestKey=key

		if debug:
			print "key= "+deepestKey

		if deepestKey not in greenGeneKeyToNumber:
			print "key= "+deepestKey
			print "Warning: not in green genes taxonomy:"
			print header.strip()
			keyNotFound+=1
			continue

		taxonNumber=greenGeneKeyToNumber[deepestKey]

		if accession in accessionToIdentifier:
			genomeIdentifier=accessionToIdentifier[accession]
	
			genomeToTaxonForNCBI.write(str(genomeIdentifier)+"	"+str(taxonNumber)+"\n")

		greenGeneGenomeNumber+=namespace

		genomeToTaxonForGreenGenes.write(str(greenGeneGenomeNumber)+"	"+str(taxonNumber)+"\n")

		fastaFileWithNamespace.write(">gi|"+str(greenGeneGenomeNumber)+"| "+header.strip().replace(">","")+"\n")
		fastaFileWithNamespace.write(sequence+"\n")
				
	elif parity==0:
		processed+=1

		if processed % PERIOD == 0:
			print "Processed "+str(processed)

		header=line.strip()
		parity=1

genomeToTaxonForGreenGenes.close()
genomeToTaxonForNCBI.close()
fastaFileWithNamespace.close()

print "keyNotFound= "+str(keyNotFound)

