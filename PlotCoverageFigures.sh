#!/bin/bash

SLOTS=$1

j=0

for i in $(seq 0 $(($SLOTS-1)))
do
	echo "">$i.list
done

for i in $(ls Depths/*.CoverageDepth.tsv)
do
	core=$(($j % $SLOTS))

	echo $i >> $core.list

	j=$(($j+1))
done

for j in $(ls *.list)
do
	(

	for i in $(cat $j)
	do
		outputFile=$(echo $i|sed 's/\.tsv/.pdf/g')

		referenceName=$(basename $i|sed 's/\.CoverageDepth\.tsv//g')
		length=$(tail -n1 $i|awk '{print $1}')

		echo "

r=read.table('$i')
pdf('$outputFile')
plot(r[[1]],r[[2]],type='l',col='blue',xlab='Reference nucleotide position',
	ylab='Read depth',main='Read depth for reference $referenceName\nLength in nucleotides: $length')
dev.off()
"| R --vanilla

	done

	) &

done

wait

