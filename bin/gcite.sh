#!/bin/bash
#
# Author:        Chunhua Shen {chhshen@gmail.com}, University of Adelaide
# Creation:      Friday 27/01/2012 13:33.
# Last Revision: Saturday 28/01/2012 20:05.


echo " ... extracting google citation number ..."


lynx -dump \
"http://scholar.google.com/citations?hl=en&user=Ljk2BvIAAAAJ&view_op=list_works&pagesize=20" \
   > _tmp



citation=` cat _tmp  \
     | grep 'Citations *[0-9]' | awk '{print $2}'`


echo "In total: "$citation" citations"
echo $citation > gcitation_num.text 

Hindex=`cat _tmp  | grep h-index | awk '{ print $2 }'`
echo "H-index: $Hindex"
echo $Hindex > gcitation_HIndex.text

rm -f _tmp


# cat ../paper0.jemdoc | sed s/XXX/$citation/g > ../_tmp
# mv    -f ../_tmp ../paper.jemdoc

cat ../fullpaper.jemdoc | sed s/XXX/$citation/g > ../_tmp
mv  -f ../_tmp ../fullpaper.jemdoc

cat ../fullpaper2.jemdoc | sed s/XXX/$citation/g > ../_tmp
mv  -f ../_tmp ../fullpaper2.jemdoc


cat ../paper.jemdoc | sed s/XXX/$citation/g > ../_tmp
mv  -f ../_tmp ../paper.jemdoc

cat ../paper2.jemdoc | sed s/XXX/$citation/g > ../_tmp
mv  -f ../_tmp ../paper2.jemdoc



