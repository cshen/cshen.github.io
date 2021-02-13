#!/bin/bash
#
# Grab abstract from arXiv

start=0

url="$1"
lynx --dump $url > _t

while read line
do

    echo $line | grep -q "Abstract: "
    if [ $? -eq 0 ]
    then
        start=1
    fi

    echo $line | grep -q "Subjects: "
    if [ $? -eq 0 ]
    then
        start=0
        continue
    fi


    if [ $start -eq 1 ]
    then
        echo $line
    fi

done < _t

rm -f _t


