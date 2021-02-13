#!/bin/bash
#
# Compared with extract_pdf_thumbnail.sh,  this script also generate the PDF files' links in an
# associated text file 
#




if ! hash pdfseparate 2>/dev/null
then
    brew install popller
fi



BIBDir=../data/bibtex
TD=../data/thumbnail/
_LinkFile="_PDFLink.txt"



# WorkD=$(mktemp -d)

WorkD=$HOME/Downloads/00_download_my_papers

[  -d $WorkD  ] && rm -fr   $WorkD
mkdir -p $WorkD

echo $WorkD"  is the temp working dir."



function download_pdf()
{

kk=0

echo "" > $_LinkFile

for ff in `ls -1 $BIBDir/*.bib`
do
    PDF=''
    PDFURL=''

    PDF=`cat $ff | grep pdf | grep = | grep -v project  | cut -d "{" -f2 | cut -d "}" -f1`
    eURL=`cat $ff | grep eprint | grep -v project  | cut -d "{" -f2 | cut -d "}" -f1`

    # echo "-----------"
    # echo $ff
    # echo $eURL
    # echo "-----------"

    [ x"$eURL" != 'x'  ] && PDFURL=https://arxiv.org/pdf/$eURL.pdf

    F1=`basename $ff  .bib`_PDF.pdf
    F2=`basename $ff  .bib`_arXiv.pdf

    J1=`basename $ff  .bib`_PDF.jpg
    J2=`basename $ff  .bib`_arXiv.jpg


    echo $PDF | grep http 2>/dev/null

    [  $?  ] && [  x$PDF != 'x'  ]  && [ ! -f  $TD/`basename $ff  .bib`_PDF.jpg  ]  &&  \
                echo "PDF downloading:  $PDF"   &&  curl -L -o     $WorkD/$F1  $PDF &&  \
                echo -n -e $J1" \t | " >> $_LinkFile    && echo "$PDF" >> $_LinkFile


    [ ! -f  $TD/`basename $ff  .bib`_arXiv.jpg    ]   &&    [ x$PDFURL != 'x' ]           &&  \ 
                echo "arXiv downloading:  $PDFURL" &&  curl -L -o     $WorkD/$F2  $PDFURL &&  \
                echo -n -e $J2" \t | " >> $_LinkFile    && echo "$PDFURL" >> $_LinkFile

    
    kk=`echo "$kk + 1" | bc `
    echo "."
    echo "."
    echo "$kk"


done

}

function gen_jpg()
{
    WD=$1      #working dir

    for ff in `ls -1 $WD/*.pdf`
    do

        F=`basename $ff .pdf`

        echo "processing "$F

        # SOMEHOW PDFTK doesn't always work, Nov 2018.   Use pdfseparate
        # pdftk   $ff   cat  1-1   output   _1.pdf
        #
        pdfseparate -f 1 -l 1    $ff        _%d.pdf    \
           \
        && \
        convert -thumbnail "900x600>" -density 300 -background white -alpha remove  _1.pdf  _out.jpg \
        && \
        mv _out.jpg $F.jpg  &&  rm  -f  _1.pdf  

    done

    [ -d $WD/thumbnail ] && rm -fr $WD/thumbnail
    mkdir -p $WD/thumbnail && mv *jpg $WD/thumbnail

}


download_pdf
CurD=`pwd`



cd $WorkD
gen_jpg .


cd $CurD
mkdir -p  ../data/thumbnail/
mv $HOME/Downloads/00_download_my_papers/thumbnail/*   $TD


# EoF 
