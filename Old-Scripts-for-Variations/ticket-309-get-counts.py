#!/usr/bin/python

files=[
"20100916_708YKAAXX_s1_r1_iall.fastq.inGene-changes+codons.xls.aa.txt",
"20100916_708YKAAXX_s2_r1_iall.fastq.inGene-changes+codons.xls.aa.txt",
"20100916_708YKAAXX_s3_r1_iall.fastq.inGene-changes+codons.xls.aa.txt",
"20100916_708YKAAXX_s4_r1_iall.fastq.inGene-changes+codons.xls.aa.txt",
"20100916_708YKAAXX_s5_r1_iall.fastq.inGene-changes+codons.xls.aa.txt",
"20100916_708YKAAXX_s6_r1_iall.fastq.inGene-changes+codons.xls.aa.txt",
"20100916_708YKAAXX_s7_r1_iall.fastq.inGene-changes+codons.xls.aa.txt",
"20100916_708YKAAXX_s8_r1_iall.fastq.inGene-changes+codons.xls.aa.txt"
]

table={}

sample=1
for file in files:
	for line in open(file):
		#LmjF01.0480     54    
		tokens=line.split()
		chromosome=tokens[2]
		position=tokens[3]
		change=tokens[4]+"->"+tokens[5]
		key=chromosome+" "+position+" "+change
		#print "Key= "+key
		if key not in table:
			table[key]={}
		table[key][sample]=1
	sample+=1

print "GeneAndPosition\tSample1\tSample2\tSample3\tSample4\tSample5\tSample6\tSample7\tSample8\tCount"

counts={}

for i in table.items():
	key=i[0]
	print key,
	sample=1
	sum=0
	while sample<=8:
		present=0
		if sample in table[key]:
			present=1
		print "\t"+str(present),
		sample+=1
		sum+=present
	print "\t"+str(sum)
	counts[key]=sum
	
f=open("CommonList.xls","w+")
f.write("Gene\tGenePosition\tChromosome\tChromosomePosition\tWildTypeNucleotide\tMutantNucleotide\tWildTypeCodon\tMutantCodon\tProteinPosition\tWildTypeAminoAcid\tMutantAminoAcid\n")
for line in open("20100916_708YKAAXX_s1_r1_iall.fastq.inGene-changes+codons.xls.aa.txt"):
	tokens=line.split()
	chromosome=tokens[2]
	position=tokens[3]
	change=tokens[4]+"->"+tokens[5]
	key=chromosome+" "+position+" "+change
	positionInGene=int(tokens[1])
	positionInProtein=(positionInGene-1)/3+1
	if counts[key]==8:
		f.write(tokens[0])
		i=1
		while i<=5:
			f.write("\t"+tokens[i])
			i+=1
		i=12
		while i<=13:
			f.write("\t"+tokens[i])
			i+=1
		f.write("\t"+str(positionInProtein))
		i=14
		while i<=15:
			f.write("\t"+tokens[i])
			i+=1

		f.write("\n")
f.close()
