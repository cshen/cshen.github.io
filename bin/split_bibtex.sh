#!/bin/bash
#
# Author:        Chunhua Shen [http://cs.adelaide.edu.au/~chhshen/], The University of Adelaide
# Creation:      Tuesday 11/12/2012 19:48.
# Last Revision: Thursday 28/03/2013 15:00.

BIBFILE=../data/cs.bib
BIBDIR=../data/bibtex


Gawk=awk
[[ "$OSTYPE" == "darwin"* ]] && Gawk=gawk




mkdir -p $BIBDIR

echo "- Split the bibtex file $BIBFILE into individual files ..."

grep @  $BIBFILE  | gsed s/{/" "/g  | gsed s/,//g | $Gawk '{print $2}' | tr -d '\r' > _biblist
for bibentry in `cat _biblist`
do

    # if the invidual file exisits, skip
    if [ ! -f $BIBDIR/$bibentry.bib ];
    then
    	echo "generating:  "$bibentry

    	bb=`echo $bibentry | tr -d '\r' | tr -d '\n' `

        ./bibextract.sh  ""  $bb  ../data/cs.bib     > $BIBDIR/$bb.bib
    fi
done

echo "done."


