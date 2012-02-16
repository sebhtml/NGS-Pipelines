for i in $(ls ../../*.sam.bz2)
do
	bunzip2 < $i | python extract-windows.py > $(basename $i).windows &
done

