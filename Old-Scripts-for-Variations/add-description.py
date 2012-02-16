#!/usr/bin/python

import sys

gffFile=sys.argv[1]
pileup=sys.argv[2]
out=sys.argv[3]

# apidb|Lmjchr1   ApiDB   mRNA    149669  151648  .       +       .       ID=apidb|rna_LmjF01.0540-1;Name=LmjF01.0540-1;description=hypothetical+protein%2C+conserved;size=1980;Parent=apidb|LmjF01.0540;Dbxref=ApiDB:LmjF01.0540,NCBI_gi:157878873,NCBI_gi:1617561,Sanger:LmjF01.0540,taxon:5664


descriptions={}

for i in open(gffFile):
	t=i.split()
	if len(t)<3:
		continue
	if t[2]!="mRNA":
		continue
	text=t[8]
	id=text.split(";")[0].split("=")[1].replace("apidb|rna_","").replace("-1","").strip()
	product=text.split(";")[2].split("=")[1].replace("+"," ").replace("%2C",",").strip()
	descriptions[id]=product

w=open(out,"w+")

for i in open(pileup):
	t=i.split()
	key=t[0]
	description=descriptions[key]
	w.write(i.replace(key,key+"\t"+description))

w.close()

