#!/bin/bash

group=$1
# assuming 32 cores per job, this is 512 cores
maximumJobs=16

userName=$(whoami)

for i in $(cat SampleList.txt)
do
	# wait until some jobs finish
	while test $(qstat|grep $userName|wc -l) -gt $(($maximumJobs-1))
	do	
		sleep 1
	done

	echo "$(date) Launching job"
	qsub $group$i.sh
done
	
