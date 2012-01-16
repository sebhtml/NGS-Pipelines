#!/bin/bash

detectLife(){

	group=$1
	echo "[DetectLife] detecting things in $group"
	
	thresholds="0.0001 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9"
	selection=0.5
	
	cat $group/* |grep '^#'|head -n1 > $group.tsv

	cat $group/* |grep -v '^#' >> $group.tsv
	
	for i in $thresholds
	do
		detected=$(filter.py $group.tsv $i|wc -l)
		echo "$i $detected"
	done > $group-thresholds.tsv
	
	filter.py $group.tsv $selection > $group-$selection.tsv
}

for i in $(ls|grep -v tsv|grep -v DeNovoAssembly)
do
	detectLife $i
done
