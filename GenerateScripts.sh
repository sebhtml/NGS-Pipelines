group=$1

for i in $(cat SampleList.txt)
do
	command="s/__SAMPLE__/$i/g"
	cp $group"Template.sh" $group$i.sh
	sed -i $command $group$i.sh
done

for i in $(cat SampleList.txt)
do
	echo "qsub $group$i.sh"
done > $group"Launch".sh


