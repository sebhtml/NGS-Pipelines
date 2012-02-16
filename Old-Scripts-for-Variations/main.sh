#!/bin/bash

# first version utilises:

# samtools Version: 0.1.7 (r510)
# samtools.pl  Version: 0.3.3
# bwa Version: 0.5.7 (r1310)

# current version utilises symbolic links. yay!



export PATH=.:$PATH

reference=../Chromosomes.fasta

type bwa

#bwa index $reference

echo "Starting main loop"

for i in $(ls ../Reads)
do  
	(
	echo "Aligning $i"
	#bwa aln $reference ../Reads/$i > ../Alignments/$i.sai 2> ../Logs/$i-aln.log 
	echo "Running samse for $i"
	#bwa samse $reference ../Alignments/$i.sai ../Reads/$i > ../Alignments/$i.sam 2> ../Logs/$i-samse.log 
	
	#samtools view -bS -o ../Alignments/$i.bam ../Alignments/$i.sam 
	#samtools flagstat ../Alignments/$i.bam &> ../Logs/$i.flagstat 
	#samtools sort ../Alignments/$i.bam ../Alignments/$i.sorted 

	#samtools mpileup -cv -f $reference ../Alignments/$i.sorted.bam > ../Variations/$i.pileup
	#samtools.pl varFilter ../Variations/$i.pileup > ../Variations/$i.varFilter
	#Illumina-Lmajor-pipeline/custom-filter.py $i.varFilter > $i.f2

	# http://samtools.sourceforge.net/mpileup.shtml
	#samtools mpileup -ugf $reference ../Alignments/$i.sorted.bam | bcftools view -bvcg - > ../Variations/$i.bcf
	#bcftools view ../Variations/$i.bcf | vcfutils.pl varFilter -d 10 -D 100 > ../Variations/$i.vcf  

	Illumina-Lmajor-pipeline/get-gene-mutations.py ../Variations/$i.vcf ../Genes.gff > ../Variations/$i.inGene 
	Illumina-Lmajor-pipeline/classify-indel.py ../Variations/$i.inGene 

	Illumina-Lmajor-pipeline/extract-codons.py ../Variations/$i.inGene-changes.xls ../Genes.gff Illumina-Lmajor-pipeline/IUPAC-code.txt ../Genes.fasta > ../Variations/$i.Codons
	cat ../Variations/$i.Codons |grep -v Error > ../Variations/$i.inGene-changes+codons.xls

	Illumina-Lmajor-pipeline/split.py ../Variations/$i.inGene-changes+codons.xls 

	Illumina-Lmajor-pipeline/keep-non-synonymous.py ../Variations/$i.inGene-changes+codons.xls-homozygous.xls Illumina-Lmajor-pipeline/codons.txt \
		> ../Variations/$i.inGene-changes+codons-homozygous-non-synonymous.xls

	Illumina-Lmajor-pipeline/keep-non-synonymous.py ../Variations/$i.inGene-changes+codons.xls-heterozygous.xls Illumina-Lmajor-pipeline/codons.txt \
		> ../Variations/$i.inGene-changes+codons-heterozygous-non-synonymous.xls

	cat $i.data|awk '{print $11}'|sort|uniq > $i.genes

	touch ../Finished/$i.1

	) # &
done 

echo "Waiting"
# wait for things to be done...
while test $(ls ../Reads|wc -l) -lt $(ls ../Finished|wc -l)
do
	# re-evaluate in 20 seconds.
	sleep 20
done

echo "Done waiting"

# the computation of 2-8 depends on the computation of 1

Illumina-Lmajor-pipeline/compare.py ../Variations/*-changes+codons-homozygous-non-synonymous.xls > ../Comparisons/summary-homozygous-changes.html
Illumina-Lmajor-pipeline/compare.py ../Variations/*-changes+codons-heterozygous-non-synonymous.xls > ../Comparisons/summary-heterozygous-changes.html
Illumina-Lmajor-pipeline/compare.py ../Variations/*-deletions.xls > ../Comparisons/summary-deletions.html
Illumina-Lmajor-pipeline/compare.py ../Variations/*-insertions.xls > ../Comparisons/summary-insertions.html

# add descriptions
for i in $(ls *.3)
do
	Illumina-Lmajor-pipeline/add-description.py ../Genes.gff $i $i.desc
done

Illumina-Lmajor-pipeline/plot-coverage.sh
