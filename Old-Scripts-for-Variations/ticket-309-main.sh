 for i in $(ls *codons.xls)
 do
 ../Illumina-Lmajor-pipeline/ticket-309-add-aminoacids.py $i ../Illumina-Lmajor-pipeline/codons.txt > $i.aa.txt
 done

