#!/bin/bash

detectLife(){

group=$1

thresholds="0.0001 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9"
selection=0.5

cat $group-Genomes/* > $group-Genomes.tsv

for i in $thresholds
do
	detected=$(filter.py $group-Genomes.tsv $i|wc -l)
	echo "$i $detected"
done > $group-Genomes-thresholds.tsv

filter.py $group-Genomes.tsv $selection > $group-Genomes-$selection.tsv
}

detectLife Bacteria
detectLife Viruses
