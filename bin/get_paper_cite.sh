

url='https://scholar.google.com/scholar?lr&ie=UTF-8&oe=UTF-8&q='"$1"

lynx -dump $url | grep 'Cited by' | tr -d 'Cited' | tr -d 'by' \
    | awk '{print $2}'


