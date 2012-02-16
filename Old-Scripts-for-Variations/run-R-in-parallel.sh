#!/bin/bash

rm *.running
rm *.completed

function countRunningInstances {
	ps aux|grep '\.running'|grep -v grep|wc -l
}

function countCompletedInstances {
	ls *.completed  2>/dev/null|wc -l
}

function countTotalInstances {
	echo $((8*36))
}

slots=23

while test $(countCompletedInstances) -lt $(countTotalInstances)
do
	for sample in $(seq 4 8)
	do
		for chromosome in $(seq 1 36)
		do
			sleep 1
			echo "$(countRunningInstances)/$slots  ($(countCompletedInstances)/$(countTotalInstances))"
			file="$sample-$chromosome.running"
			if test -f $file
			then
				echo "">/dev/null
			else
				# instance is not running and is not completed.
				if test $(countRunningInstances) -lt $slots
				then
					cp Illumina-Lmajor-pipeline/test-smoothing.R "$sample-$chromosome.running"
					sed -i "s/__SAMPLE__/$sample/g" "$sample-$chromosome.running"
					sed -i "s/__CHROMOSOME__/$chromosome/g" "$sample-$chromosome.running"
					(
					./"$sample-$chromosome.running" &>/dev/null
					touch "$sample-$chromosome.completed"
					) &
				fi
			fi
		done
	done
done

cp 1-1.html index.html

