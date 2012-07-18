#!/bin/bash

for i in $(cat processed-samples)
do

	path=$(grep $i entries|sed 's=OutputNumbers.txt==g')

	~/git-clones/NGS-Pipelines/comparison-with-MetaPhlAn/convert-Ray-profile-to-xml.py $i $path

done > ray.xml
