#!/usr/bin/env python
#
# Author:        Chunhua Shen {chhshen@gmail.com}, University of Adelaide
# Creation:      Tuesday 13/03/2012 10:24.
# Last Revision: Tuesday 13/03/2012 10:29.


import urllib, hashlib
email = "chhshen@gmail.com"
default = "identicon"
size = 40
# construct the url

gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

print "<img src='" + gravatar_url + "'  />"




