#!/bin/bash
#
# Author:        Chunhua Shen [http://cs.adelaide.edu.au/~chhshen/], The University of Adelaide
# Creation:      Wednesday 04/07/2012 13:45.
# Last Revision: Wednesday 04/07/2012 14:36.

echo "... extracting citation chart from google scholar ..."
lynx --dump "http://scholar.google.com/citations?hl=en&user=Ljk2BvIAAAAJ&view_op=list_works&pagesize=20"  > _t



# yy=`date +"%Y"`
# yy0=`echo $yy - 1 | bc`

# cat _t | grep -2 201520162017  |  tail -3 | tr -d '\r\n '  | gsed 's/\[..\]/ /g'   \
#   | awk -F$yy0$yy      '{ print $2 }' \
#  > _chart


 cat _t | grep -2 201520162017  |  tail -3 | tr -d '\r\n '  | gsed 's/\[..\]/ /g'   \
   | awk -F" "      '{ $1=""; print $0 }' \
  > _chart


cat _t | grep -2 201520162017  |  tail -3 | tr -d '\r\n '  | gsed 's/\[..\]/ /g'   \
   | awk -F" "      '{ print $1 }' \
  > _year



rm -f _t

N=0
for i in `cat _chart | xargs`
do
 let N+=1
 cite[ N ]=$i
done



echo "your citations in recent years are:"
for i in `jot $N`
do
    echo ${cite[ $i ]}
done

year_start=`cat _year | cut -c1-4`


echo "update the json file ..."
# {
#     "data": [[1999, 1], [2000, 0.23], [2001, 3], [2002, 4]]
# }

JFILE=cs_cite.json
echo "{" >         $JFILE
echo '"data":[' >> $JFILE


for i in `jot $N`
do
    echo -n  "["$year_start", "${cite[ $i ]}"] "  >> $JFILE

    if [ "$i" -ne  "$N" ]
    then
        echo ","       >> $JFILE
    fi

    let year_start+=1
done

echo "]}"      >> $JFILE

mv -f $JFILE ../data/

rm -f _chart _ycite
rm -f _year


# generate a PDF plot of the citation from the JSON file
./pdf_cite_chart.py

[ -f ./cs_cite.pdf  ] && mv -f ./cs_cite.pdf ../data/



