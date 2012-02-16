grep  CDS CDS.gff|grep -v gene|awk '{print $1" "$4" "$5" fill_color=red"}'|grep apidb|sed 's/apidb|//g'> circos-files/CDS-track.txt
grep  tRNA tRNA.gff|grep -v gene|awk '{print $1" "$4" "$5" fill_color=purple"}'|grep apidb|sed 's/apidb|//g'> circos-files/tRNA-track.txt
grep  ncRNA ncRNA.gff|grep -v gene|awk '{print $1" "$4" "$5" fill_color=teal"}'|grep apidb|sed 's/apidb|//g'> circos-files/ncRNA-track.txt
grep  snRNA snRNA.gff|grep -v gene|awk '{print $1" "$4" "$5" fill_color=brown"}'|grep apidb|sed 's/apidb|//g'> circos-files/snRNA-track.txt
grep  rRNA rRNA.gff|grep -v gene|awk '{print $1" "$4" "$5" fill_color=pink"}'|grep apidb|sed 's/apidb|//g'> circos-files/rRNA-track.txt
