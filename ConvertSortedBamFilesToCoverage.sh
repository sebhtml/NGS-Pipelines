#!/bin/bash
# author: Sébastien Boisvert

bamFiles=$@
arguments=0

for i in $bamFiles
do
	arguments=$(($arguments+1))
done 

if test $arguments = 1
then
	samtools view -h $bamFiles | ConvertSamStreamToCoverage.py
else
	samtools merge - $bamFiles | samtools view - -h | ConvertSamStreamToCoverage.py
fi

