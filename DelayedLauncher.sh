#!/bin/bash

group=$1
maximumNumberOfCores=512

userName=$(whoami)

for i in $(cat SampleList.txt)
do
	# wait until some jobs finish
	while test $(colosse-info|grep slots|grep using|awk '{print $5}') -ge $(($maximumNumberOfCores))
	do	
		sleep 1
	done

	echo "$(date) Launching job"
	qsub $group$i.sh
done
	
