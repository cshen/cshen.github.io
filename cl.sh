#!/bin/bash
#
# Author:        Chunhua Shen {chhshen@gmail.com}
# Creation:      Wednesday 13/08/2008 12:06.
# Last Revision: Saturday 18/05/2013 18:48.


jemdoc=./jemdoc.py


rm -f eqs/*


# Generate the full paper list
cd bin

# split the bibtex file into individual files
./split_bibtex.sh


./bib2jemdoc.py  > fullpaper.jemdoc
mv -f fullpaper.jemdoc ..

./bib2jemdoc2.py  > fullpaper2.jemdoc
mv -f fullpaper2.jemdoc ..

./bib2jemdoc_select.py  > paper.jemdoc
 mv -f paper.jemdoc ..


./bib2jemdoc_select2.py  > paper2.jemdoc
 mv -f paper2.jemdoc ..


cd ..


cd bin
./gcite.sh
./gcite_chart.sh

./count_era.sh
cd ..



for jfile in `ls -1 *jemdoc`
do
   echo '... ... ... processing '$jfile' ...'
   $jemdoc -c cs.conf $jfile
#    tidy -utf8 --wrap 2000 \
#         `basename $jfile .jemdoc`.html > 0
#    mv -f 0 `basename $jfile .jemdoc`.html

done



#
# change <ol> into <ol reversed>
# in paper.html, fullpaper.html, fullpaper2.html
#
cat paper.html | sed s/"<ol>"/"<ol reversed>"/g      | sed s/--3px/3px/g           > _tmp; mv _tmp paper.html
cat paper2.html | sed s/"<ol>"/"<ol reversed>"/g     | sed s/--3px/3px/g           > _tmp; mv _tmp paper2.html

cat fullpaper.html | sed s/"<ol>"/"<ol reversed>"/g  | sed s/--3px/3px/g           > _tmp; mv _tmp fullpaper.html
cat fullpaper2.html | sed s/"<ol>"/"<ol reversed>"/g | sed s/--3px/3px/g           > _tmp; mv _tmp fullpaper2.html

cat index.html | sed s/"INSERT_CHINESE_NAME"/"\&#27784;\&#26149;\&#33775;"/g > _tmp; mv _tmp index.html



#-------------------------------------------------------
# Compile publication list PDF
#
#-------------------------------------------------------
./gen_pdf_list.sh



if [  -z "$1"  ]; then
      echo " . "
      echo " . "
      echo " . "
      echo "... sync ..."
	  ./scp2srv
fi

















