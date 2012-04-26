#!/usr/bin/env python

"""
this script takes two files

- gene_association.goa_uniprot (uniprot -> gene ontology)
- idmapping.dat  (uniprot -> EMBL_CDS)

"""

import sys
import os

mapping='idmapping.dat'
associations='gene_association.goa_uniprot'
output="Associations.txt"

print "Commencing."

"""
example of a line:

!gaf-version: 2.0
UniProtKB       A0A000  moeA5           GO:0003824      GO_REF:0000002  IEA     InterPro:IPR015421      F       MoeA5   A0A000_9ACTO|moeA5      protein taxon:35758     20120331        InterPro

"""


"""
example:

Q6GZX4  UniProtKB-ID    001R_FRG3G
Q6GZX4  GI      81941549
Q6GZX4  GI      49237298
Q6GZX4  UniRef100       UniRef100_Q6GZX4
Q6GZX4  UniRef90        UniRef90_Q6GZX4
Q6GZX4  UniRef50        UniRef50_Q6GZX4
Q6GZX4  UniParc UPI00003B0FD4
Q6GZX4  EMBL    AY548484
Q6GZX4  EMBL-CDS        AAT09660.1
Q6GZX4  NCBI_TaxID      654924
Q6GZX4  RefSeq  YP_031579.1
Q6GZX4  RefSeq_NT       NC_005946.1
Q6GZX4  GeneID  2947773
Q6GZX4  ProtClustDB     CLSP2511514

"""


uniprotToCDS={}

loaded=0

print "Loading "+mapping

withoutMapping=0

for line in open(mapping):
	tokens=line.split("\t")
	operationCode=tokens[1]

	if operationCode=="EMBL-CDS":
		uniprotKey=tokens[0]
		emblCdsKey=tokens[2].split(".")[0].strip()

		if emblCdsKey=='-':
			withoutMapping+=1
			continue

		uniprotToCDS[uniprotKey]=emblCdsKey

		if loaded%1000==0:
			print "Loaded "+str(loaded)+" from "+mapping+" "+uniprotKey+" -> "+emblCdsKey
		loaded+=1

print "Loaded "+mapping
print "Without mapping -> "+str(withoutMapping)

f=open(output,"w")

processed=0

lastGoKey=None

for line in open(associations):
	if line[0]=='!':
		continue

	tokens=line.split("\t")

	uniprotKey=tokens[1]

	if processed%1000 == 0:
		print "Processed: "+str(processed)+" from "+associations

	processed+=1
	
	if uniprotKey in uniprotToCDS:
		cdsKey=uniprotToCDS[uniprotKey]
		goKey=tokens[5-1]

		if goKey!=lastGoKey:
			f.write(cdsKey+"	"+goKey+"\n")

		lastGoKey=goKey
	
f.close()

print "Finished processing "+associations
