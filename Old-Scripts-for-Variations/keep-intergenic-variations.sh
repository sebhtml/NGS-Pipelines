

./Illumina-Lmajor-pipeline/keep-only-unique-entries.py $(ls ../Variations/*.fastq.vcf)


for i in $(seq 1 8)
do  

	# remove indels as they contain mostly low-complexity bits
	grep -v INDEL ../Variations/$i.fastq.vcf.unique > ../Variations/$i-unique-not-INDEL.vcf


	Illumina-Lmajor-pipeline/keep-intergenic-variations.py ../Variations/$i-unique-not-INDEL.vcf ../Genes.gff \
	> ../IntergenicVariations/$i.xls

	# also dump the same information with the VCF format
	Illumina-Lmajor-pipeline/keep-intergenic-variations-vcf.py ../Variations/$i-unique-not-INDEL.vcf ../Genes.gff \
	> ../IntergenicVariations/$i.vcf.xls
done

