#!/bin/bash
# author: Sébastien Boisvert

bamFiles=""
arguments=0

k=0
# $@ is the argument list
for i in $@
do
	if test $k -ge 2
	then
		arguments=$(($arguments+1))
		bamFiles=$bamFiles" $i"
	fi

	k=$(($k+1))
done 

if test $arguments = 0
then
	echo "Usage"
	echo "BinInGenomicWindows.sh windowLength outputDirectory file1.bam [other bam files]"
	exit
fi

windowLength=$1
outputDirectory=$2

echo "windowLength= $windowLength"
echo "outputDirectory= $outputDirectory"
echo "bamFiles= $bamFiles"

if test $arguments = 1
then
	samtools view -h $bamFiles |  BinInGenomicWindows.py $windowLength $outputDirectory
else
	samtools merge - $bamFiles | samtools view - -h | BinInGenomicWindows.py $windowLength $outputDirectory
fi

