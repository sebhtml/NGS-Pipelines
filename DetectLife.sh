#!/bin/bash

detectLife(){
	group=$1
	echo "[DetectLife] detecting things in $group"
	
	cat $(ls $group/*|grep -v Identifi) |grep '^#'|head -n1 > $group.tsv

	cat $(ls $group/*|grep -v Identifi) |grep -v '^#' >> $group.tsv
}

for i in $(ls|grep -v tsv|grep -v DeNovoAssembly)
do
	detectLife $i
done
