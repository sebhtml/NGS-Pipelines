#!/bin/bash
# Sébastien Boisvert

if test $# != 3
then
	echo "Welcome !"
	echo "this script is called as follows:"

	echo "GenerateScripts.sh Template.sh SampleList.txt schedulerCommand"
	echo "examples:"
	echo 
	echo "GenerateScripts.sh GreenRayTemplate.sh SampleList.txt msub"
	echo "GenerateScripts.sh GreenRayTemplate.sh SampleList.txt qsub"
	exit
fi

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


