##!/bin/bash
#$ -N read-depth-2011-10-31.7
#$ -P nne-790-ab
#$ -l h_rt=2:00:00
#$ -pe default 8
#$ -cwd

module load compilers/gcc/4.4.2 


for i in $(seq 1 8)
do
	(
	#../../../software/samtools-0.1.18/samtools view -h ../Alignments/$i.fastq.sorted.bam | \
	#	Illumina-Lmajor-pipeline/sorted-sam-to-coverage-stream.py | \
	#	Illumina-Lmajor-pipeline/split-by-column.py ../ReadDepth/$i 1

	cat ../ReadDepth/$i.*|awk '{print $3}'|sort -n|uniq -c|awk '{print $2" "$1}' > ../ReadDepth/$i-frequencies
	)&
done

