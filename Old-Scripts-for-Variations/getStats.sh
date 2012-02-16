
# check how many variations are present on each chromosome

for i in $(ls *.unique); do awk '{print $1}' $i|sort|uniq -c |sed 's/psu|Lmjchr//'|awk '{print $2" "$1}'|sort -n> $i.stats; done

