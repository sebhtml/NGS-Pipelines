#!/usr/bin/python


import sys

fastaFile=sys.argv[1]

leftSide=2500
rightSide=2500

sequences={}

name=""
seq=""
for line in open(fastaFile):
	if line[0]=='>':
		if name!="":
			sequences[name]=seq
		name=line.split()[0].replace(">","")
		seq=""
	else:
		seq+=line.strip()

sequences[name]=seq

for i in sequences.items():
	name=i[0]
	seq=i[1]
	i=0
	theLength=len(seq)

	totalGC=0
	total=0
	j=-1
	while j<leftSide:
		position=i-j-1
		if position==-1:
			break
		nucleotide=seq[position]
		if nucleotide=='g' or nucleotide=='G' or nucleotide=='c' or nucleotide=='C':
			totalGC+=1
		total+=1
		j+=1
	j=0
	while j<rightSide:
		position=i+j+1
		if position==theLength:
			break
		nucleotide=seq[position]
	
		if nucleotide=='g' or nucleotide=='G' or nucleotide=='c' or nucleotide=='C':
			totalGC+=1
		total+=1
		j+=1

 	#     i-3	i-2	i-1	i	i+1	i+2	i+3
	while i<theLength:
		if i==0:
			ratio=(totalGC+0.0)/total
			print name+"\t"+str(i+1)+"\t"+str(ratio)+"\t"+str(total)
		else:
			positionToRemove=i-leftSide-1
			positionToAdd=i+rightSide
			if positionToRemove>=0:
				nucleotide=seq[positionToRemove]
				
				if nucleotide=='g' or nucleotide=='G' or nucleotide=='c' or nucleotide=='C':
					totalGC-=1
				total-=1

			if positionToAdd<theLength:
				nucleotide=seq[positionToAdd]
				
				if nucleotide=='g' or nucleotide=='G' or nucleotide=='c' or nucleotide=='C':
					totalGC+=1
				total+=1

			ratio=(totalGC+0.0)/total
			print name+"\t"+str(i+1)+"\t"+str(ratio)+"\t"+str(total)
		i+=1
