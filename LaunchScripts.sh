#!/bin/bash

group=$1

for i in $(cat SampleList.txt)
do
	qsub $group$i.sh
done
	
