#!/bin/bash
#
# Author:        Chunhua Shen [http://cs.adelaide.edu.au/~chhshen/], The University of Adelaide
# Creation:      Saturday 24/11/2012 12:30.
# Last Revision: Saturday 24/11/2012 13:57.


cd ../projects


echo "# jemdoc: addpackage{xcolor},eqsize{100},title{Chunhua Shen | The University of Adelaide}"
echo "= Projects"
echo " "



#
# list=`find . -type d -maxdepth 1 | awk 'NR != 1'`
#
list=`find . | grep index.jemdoc`

for f in $list
do
    dos2unix $f

    link=`echo $f | sed 's/index.jemdoc//g'`
    topic=`head -2 $f | grep "= " | sed 's/=//g'`

    echo -n "-  "
    printf "[./projects/$link"
    printf " "
    echo "$topic]"

done




