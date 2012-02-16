
module load compilers/gcc/4.4.2 

export PATH=.:$PATH

for i in $(seq 1 8)
do
	(
	samtools view -ub  ../Alignments/$i.fastq.sorted.bam | samstat -f bam -n $i
	mv $i.html ../QualityControl
	)&
done

wait
