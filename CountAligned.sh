#!/bin/bash

token=$1

for i in $(find .|grep sorted.bam)
do  
	total=$(/rap/nne-790-ab/software/samtools-0.1.18/samtools view $i|wc -l)
	aligned=$( /rap/nne-790-ab/software/samtools-0.1.18/samtools view $i|grep $token|wc -l)
	ratio=$(echo "scale=4;100*$aligned/$total"|bc)
	name=$i

	echo "$name $total $aligned $ratio%"
done
