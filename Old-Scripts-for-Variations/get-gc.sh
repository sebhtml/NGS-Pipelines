#!/bin/bash

for j in $(seq 1 36)
do
	grep "psu|Lmjchr$j	" LmajorGenomic_TriTrypDB-2.4.fasta.GC > $j.GC
done
