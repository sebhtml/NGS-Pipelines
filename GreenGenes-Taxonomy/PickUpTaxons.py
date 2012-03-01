#!/usr/bin/env python
#encoding: UTF-8
# author: Sébastien Boisvert
# license: GPLv3

"""
PickUpTaxons.py NCBI-genome-fasta-headers.txt Taxon-Names.tsv  NCBI-genome-and-GreenGenes-Genome-to-Taxons.tsv 


This program picks the best taxon for each header line in NCBI-genome-fasta-headers.txt.

Example:

Query= >gi|158333233|ref|NC_009925.1| Acaryochloris marina MBIC11017 chromosome, complete genome
best= Acaryochloris marina difficult=False


With the NCBI genomes from 2011-12-23 and GreenGenes 2011_1:

2735 NCBI-genome-fasta-headers.txt


   78 no-hit.txt (mostly archea like Halophilic archaeon DL31)

   37 difficult.txt (half are species like Candidatus Accumulibacter)

In Greengenes, there is no Candidatus genus and some like  Candidatus Accumulibacter are missing.

A difficult is an entry with more than 1 hit that have the same word hits and the same complexity.

Output:

2657 NCBI-genome-and-GreenGenes-Genome-to-Taxons.tsv

"""

import sys

debug=False

if len(sys.argv)!=4:
	print __doc__
	sys.exit(1)

database={}

taxonNames={}
taxonRanks={}

numberCounts={}

for line in open(sys.argv[2]):
	tokens=line.split("\t")
	number=int(tokens[0])
	name=tokens[1]
	rank=tokens[2].strip()

	taxonNames[number]=name
	taxonRanks[number]=rank

	words=name.split()

	for j in words:
		i=j.lower()
		if i not in database:
			database[i]=[]
		database[i].append(number)

	numberCounts[number]=len(words)

out=open(sys.argv[3],"w")

numberToTaxon={}

for line in open(sys.argv[1]):
	header=line

	tokens=line.split()

	votes={}

	done={}

	for word1 in tokens:
		word=word1.lower()

		if word in done:
			continue

		if word.find("(")>=0 or word.find(")")>=0:
			continue

		if word=="sp.":
			continue

		done[word]=1

		if word in database:
			for number in database[word]:
				if number not in votes:
					votes[number]=0
				votes[number]+=1

	if debug:
		for i in votes.items():
			print taxonNames[i[0]]+" "+str(i[0])+" has "+str(i[1])+" votes"

	best=None
	difficult=False

	for i in votes.items():
		number=i[0]
		inFavor=i[1]
		complexity=numberCounts[number]

		if best==None:
			print ""
			print "Query= "+line.strip()
			print "Previous has None"
			print "taxon= "+taxonNames[number]+" votes= "+str(inFavor)+" complexity= "+str(complexity)
			best=number

		elif inFavor > votes[best]:
			best=number
			difficult=False
			print "best= "+taxonNames[number]+" difficult=False"
			print "taxon= "+taxonNames[number]+" votes= "+str(inFavor)+" complexity= "+str(complexity)

		elif inFavor == votes[best]:
			if complexity== numberCounts[best]:
				difficult=True
				print "difficult=True, current "+taxonNames[number]+" best= "+taxonNames[best]
				print "taxon= "+taxonNames[number]+" votes= "+str(inFavor)+" complexity= "+str(complexity)
			elif complexity < numberCounts[best]:
				best=number
				difficult=False

	if best==None:
		print "***"
		print "Warning: no hit found for :"+line.strip()
		continue

	if difficult:
		print "***"
		print "Warning: this entry is difficult: "+line.strip()
		print "Selected taxon -> "+taxonNames[best]+" rank= "+taxonRanks[best]
		
		print "votes"
		for i in votes.items():
			count=i[1]
			if count==votes[best]:
				print taxonNames[i[0]]+" "+str(i[0])+" has "+str(count)+" votes"

	if debug:
		print ""
		print line.strip()
		print "Selected taxon -> "+taxonNames[best]+" rank= "+taxonRanks[best]

	genomeIdentifier=header.split("|")[1]
	out.write(genomeIdentifier+"	"+str(best)+"\n")

out.close()
