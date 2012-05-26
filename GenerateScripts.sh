#!/bin/bash
# Sébastien Boisvert
# this script is called as follows:

# GenerateScripts.sh Template.sh SampleList.txt schedulerCommand
# examples:

# GenerateScripts.sh GreenRayTemplate.sh SampleList.txt msub
# GenerateScripts.sh GreenRayTemplate.sh SampleList.txt qsub

template=$1
list=$2
schedulerCommand=$3

massiveSubmit=$template"-Launch.sh"

echo ""> $massiveSubmit

for i in $(cat $list)
do
	command="s/__SAMPLE__/$i/g"
	item=$template-$i.sh
	cp $template $item
	sed -i $command $item
	echo $schedulerCommand $item >> $massiveSubmit
done


