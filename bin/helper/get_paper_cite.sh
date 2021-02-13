


url='https://scholar.google.com/scholar?lr&ie=UTF-8&oe=UTF-8&q='"$1"

param='  -useragent="Mozilla/5.0"'

 out=`lynx $param  -dump $url    2>/dev/null       \
    | grep 'Cited by' | tr -d 'Cited' | tr -d 'by' \
    | tr -d '\n'  | awk '{print $2}'`




# [[ $out == ?(-)+([0-9]) ]] && echo "$out is an integer"

[[ 'x'$out == 'x' ]] && out=0


if ! [[ "$out" =~ ^[0-9]+$ ]]
then
        echo 0
    else
        echo $out
fi

