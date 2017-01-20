
#!/usr/bin/env bash

NUMCOUNT=$1
#copy first parameter to NUMCOUNT

#echo "a b c d d d sdf dsf " | grep -oE '\w+'
#grep -o: show only matched item
#grep -E:egrep

#echo "a b c d d d sdf dsf " | grep -oE '\w+' | uniq -c
#uniq :delete repeated item. -c :count

#echo "a b c d d d sdf dsf " | grep -oE '\w+' | uniq -c | sort -hr
#sort -h:sort by human way -r: reverse order

grep -oE '\w+' | sort | uniq -c | sort -hr | head -n $NUMCOUNT
