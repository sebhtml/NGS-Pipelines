#!/bin/bash

kmerLength=$1
sampleDirectory=$2
processors=$3
outputDirectory=$4

pairs=""

for r1 in $(ls $sampleDirectory|grep R1)
do
	r2=$(echo $r1|sed 's/_R1_/_R2_/g')

	pairs=$pairs" -p $sampleDirectory/$r1 $sampleDirectory/$r2 "
done

command="mpiexec -n $processors Ray -k $kmerLength $pairs -o $outputDirectory"

echo "Command= $command"

eval $command




