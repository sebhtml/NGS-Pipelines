for i in $(ls ../*windows)
do
	signals=$i".norm"
	ratios=$i".log2ratio"
	rm -f ratios.txt
	ln -s $ratios ratios.txt
	rm -f signals.txt
	ln -s $signals signals.txt
	/software/circos-0.54/bin/circos -conf circos.conf
	output=$(basename $i)
	mv test.png $output.png
done

