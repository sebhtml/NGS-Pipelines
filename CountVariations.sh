#!/bin/bash

for i in $(find .|grep vcf)
do
	echo "$i $(grep -v "^#" $i|wc -l)"
done|sort
