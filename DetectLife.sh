#!/bin/bash

detectLife(){

	group=$1
	
	thresholds="0.0001 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9"
	selection=0.5
	
	cat $group/* > $group.tsv
	
	for i in $thresholds
	do
		detected=$(filter.py $group.tsv $i|wc -l)
		echo "$i $detected"
	done > $group-thresholds.tsv
	
	filter.py $group.tsv $selection > $group-$selection.tsv
}

detectLife Bacteria-Genomes
detectLife Bacteria-ProteinCodingGenes
detectLife Bacteria-RNAGenes
detectLife Viruses-Genomes
detectLife Viruses-ProteinCodingGenes
detectLife Viruses-RNAGenes

