#!/bin/bash
# automatically create html reports from XML data files
# author Sébastien Boisvert
# needs xsltproc

project=$1

echo "Project: $project"

for i in $(ls $project)
do 
	#echo "Sample: $i"
	#for j in $(find $project/$i|grep SequenceAbundances.xml$)
	#do
		#echo "File: $j"
		#xsltproc /home/sboisver12/git-clones/ray/scripts/xsl-xml/SequenceAbundances-to-html.xsl $j > $j-entries.html
		#xsltproc /home/sboisver12/git-clones/ray/scripts/xsl-xml/SequenceAbundances-to-html-tables.xsl $j > $j-tables.html
	#done

	for j in $(find $project/$i|grep Taxons.xml$)
	do
		echo "File: $j"
		xsltproc /home/sboisver12/git-clones/ray/scripts/xsl-xml/Taxons-to-html.xsl $j > $j-entries.html
		xsltproc /home/sboisver12/git-clones/ray/scripts/xsl-xml/Taxons-to-html-tables.xsl $j > $j-tables.html
	done
done
