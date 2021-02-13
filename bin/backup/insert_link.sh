#!/bin/bash

[ -z $1 ] && echo "an input HTML file is needed." && exit 1


echo "-------------------------"
echo "Inserting hyperlinks into $1 "
echo "-------------------------"


cp -f "$1" _tmp

# Array pretending to be a Pythonic dictionary
ARRAY=( "Yao Li|http://www.cs.adelaide.edu.au/~yaoli/"
        "David Suter|http://www.cs.adelaide.edu.au/~dsuter/"
        "Anton van den Hengel|http://cs.adelaide.edu.au/~hengel/"
        "Anthony Dick|https://cs.adelaide.edu.au/~ard/"
        "Ian Reid|http://cs.adelaide.edu.au/~ianr/"
        "Lei Wang|http://www.uow.edu.au/~leiw/"
        "Luping Zhou|http://www.uow.edu.au/~lupingz/"
        "Sakrapee Paul Paisitkriangkrai|http://cs.adelaide.edu.au/~paulp/"
        "Lingqiao Liu|https://sites.google.com/site/lingqiaoliu83/"
        "Guosheng Lin|https://sites.google.com/site/guoshenglin/"
        "Fumin Shen|http://bmc.uestc.edu.cn/~fshen/"
        "Tong He|http://tonghe90.github.io/"
        "Bohan Zhuang|https://sites.google.com/view/bohanzhuang"
        "Xiu-Shen Wei|http://lamda.nju.edu.cn/weixs/"
        "Fayao Liu|https://sites.google.com/site/fayaoliu/"
        "Chao Ma|https://sites.google.com/site/chaoma99/"
        "University of Adelaide|http://www.adelaide.edu.au"
        "Australian National University|http://www.anu.edu.au"
        "Beijing Institute of Technology|http://en.wikipedia.org/wiki/Beijing\_Institute\_of\_Technology"
        "National University of Defense Technology|http://en.wikipedia.org/wiki/National\_University\_of\_Defense\_Technology"
        "Nanjing University of Science and Technology|http://en.wikipedia.org/wiki/Nanjing\_University\_of\_Science\_and\_Technology"
        "Beihang University|http://en.wikipedia.org/wiki/Beihang\_University"
        "University of Queensland|http://www.uq.edu.au"
        "ANU|http://www.anu.edu.au"
        "UNSW|http://www.unsw.edu.au"
        "ACVT|http://blogs.adelaide.edu.au/acvt/"
        "NICTA|https://en.wikipedia.org/wiki/NICTA"
        "DSTO|http://www.dsto.defence.gov.au"
        "ATO|https://www.ato.gov.au"
        "ACRV|http://roboticvision.org"
        "IBM|http://www.ibm.com"
        "ETH|https://www.ethz.ch"
        )





for p in "${ARRAY[@]}" ; do

    KEY="${p%%|*}"
    VAL="${p##*|}"

    printf "   -->   %s --- %s\n" "$KEY" "$VAL"

    cat _tmp | sed 's_'"$KEY"_'<a href=\"'"$VAL"\"'>&</a>_g' > _tmp1

    mv -f _tmp1 _tmp
done

mv -f _tmp "$1"



