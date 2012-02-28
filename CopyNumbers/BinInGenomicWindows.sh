#!/bin/bash
# author: Sébastien Boisvert

bamFiles=$@
arguments=0

for i in $bamFiles
do
	arguments=$(($arguments+1))
done 

windowLength=1000
outputDirectory=BinInGenomicWindows

if test $arguments = 0
then
	echo "Usage"
	echo "BinInGenomicWindows.sh file1.bam [other bam files]"
	exit
fi

if test $arguments = 1
then
	samtools view -h $bamFiles |  BinInGenomicWindows.py $windowLength $outputDirectory
else
	samtools merge - $bamFiles | samtools view - -h | BinInGenomicWindows.py $windowLength $outputDirectory
fi

