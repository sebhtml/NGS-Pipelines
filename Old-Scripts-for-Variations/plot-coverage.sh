#!/bin/bash

for i in $(ls *.sam)
do
	(
	Illumina-Lmajor-pipeline/sam-to-coverage $i > $i.cov
	for j in $(seq 1 36)
	do
		grep "psu|Lmjchr$j	" $i.cov > $i-$j.cov
	done
	) &
done

