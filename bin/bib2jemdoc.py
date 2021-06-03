#!/usr/bin/env python3
# Author:        Chunhua Shen {chhshen@gmail.com}
# Creation:      Saturday 09/07/2011 21:55.
# Last Revision: Saturday 18/05/2013 18:43.
#
# You need to install pybtex first
#

import pkg_resources
pkg_resources.require("pybtex==0.18")
from pybtex.database.input import bibtex




from operator import itemgetter, attrgetter
import pprint
import re

from functools import cmp_to_key

# from IPython.core.debugger import Tracer
# debug_here = Tracer()

from pathlib import Path
from helper import ParsePDFLink as pdl

pdflink_dict, __x, __y = pdl.readlinkfile('_PDFLink.txt')



print ('# jemdoc: title{Chunhua Shen}, addcss{css/full_publication.css}' )
print ('= Publications (Full List)' )


parser = bibtex.Parser()
bib_data = parser.parse_file('../data/cs.bib')


num_papers = len(bib_data.entries)
# print '== Categorised [fullpaper2.html by type], [fullpaper.html by year]; *' + str(num_papers) +   '*  papers (_ERA_ASTAR_ [http://www.arc.gov.au/era/era_2010/archive/era_journal_list.htm ERA] A* journals, _ERA_A_ ERA A journals, _ERA_ACONF_ ERA A conferences). \n'

print ("== Categorised [fullpaper2.html by venue {{<i class='fa fa-location-arrow' aria-hidden='true'></i>}}],  [fullpaper.html by year {{<i class='fa fa-clock-o' aria-hidden='true'></i>}}]. *" + str(num_papers) + "*  papers.  \n" )



# print 'I wrote some [https://www.dropbox.com/sh/6vj10tiodqt2ht1/xJLnlUv5Eh/bib2web  python script] to generate this page and [./cshen_papers.pdf a list in pdf]  from [data/cs.bib my bibtex file].  {[./copyright.txt copyright]}\n'

print ( "[http://scholar.google.com/citations?hl=en&user=Ljk2BvIAAAAJ&view_op=list_works&pagesize=100 Google scholar (XXX citations)  {{<i class='ai ai-google-scholar'   aria-hidden='true'></i>}}]," )
print ( "[http://dblp.uni-trier.de/pers/hd/s/Shen:Chunhua DBLP {{<i class='ai ai-dblp ai-1x'></i>}}]," )
print ( "[https://tinyurl.com/ww4dlqm   arXiv {{<i class='ai ai-biorxiv ai-1x'></i>}}]." )



print ( '{{<div id="citation_plot_holder"></div>}}\n' )



def capitalize_string(x):
    y=''
    transform = 1
    for i in range(len(x)):
        if x[ i ] == "{":
            transform = 0
            continue

        if x[ i ] == "}":
            transform = 1
            continue

        # CS: May 2021
        # escape + ---> \+
        if x[i] == "+":
            y = y + "\\"   # + x[ i ]

        if transform:
            y = y + x[ i ].lower()
        else:
            y = y + x[ i ]

        z =''
        z = z + y[0].upper()
        z = z + y[1:len(y)]
    return z



def sort_list_cmp(y, x):
    yearcmp = int(x[1].fields['year']) - int(y[1].fields['year'])
    if yearcmp != 0:
        return yearcmp

    if 'journal' in x[1].fields and 'journal' not in y[1].fields:
        return 1
    if 'journal' not in x[1].fields and 'journal' in y[1].fields:
        return -1

    if 'booktitle' in x[1].fields and 'booktitle' not in y[1].fields:
        return 1
    if 'booktitle' not in x[1].fields and 'booktitle' in y[1].fields:
        return -1

    if x[1].fields['venue'] > y[1].fields['venue']:
        return -1
    if x[1].fields['venue'] < y[1].fields['venue']:
        return 1

    if x[1].fields['author'] > y[1].fields['author']:
        return 1
    else:
        return -1

def load_citekey(citekey):
# Get the info corresponding to specific citekey
    entry = bib_data.entries[citekey]
    return entry

def gen_citefields(citekey):
# Rearrange the bib entries into something more useful.
    entry = load_citekey(citekey)
    D = entry.fields

    authors = [" ".join( p.first()  + p.prelast() + p.last()  ) for p in entry.persons['author']]
    D['authors'] = ", ".join(authors)
    return D


def initialize_name2(x):
# x is in the format of "Shen, Chunhua and Brooks, Michael J. ..."
# return "Shen, C. and Brooks, M. J."
    change = 0
    s = ''
    for i in range(len(x)):

        if change == -1 and i < len(x) and x[i] == " ":
           change = 0

        if change == 0:
            s = s + x[i]

        if change == 1 and x[i] != " " :
            s = s + x[i]
            s = s + "."
            change = -1 # ignore the rest of the given name

        if x[i] == "," and x[i+1] == " ":
            change = 1
            s = s + " "
    return s


def initialize_name(x):
# x is in the format of "Chunhua Shen, X XX ..."
# return "C. Shen, X. XX"
    change = 1
    s = ''
    for i in range(len(x)):

        if change == -1 and i < len(x) and x[i] == " ":
            change = 0

        if change == 0:
            s = s + x[i]

        if change == 1 and x[i] != " " :
            s = s + x[i]
            s = s + "."
            change = -1 # ignore the rest of the given name

        if x[i] == "," and x[i+1] == " ":
            change = 1
            s = s + " "
    return s


def instance_field(x):
    if x in value.fields and len(value.fields[x]) > 0:
        return " " + x + " " + value.fields[x] + ", "
    else:
        return ""

def remove_curly_bracket(x):
    x = x.replace('{', '')
    x = x.replace('}', '')
    return x


def instance_fields( x, fields ):
    if x in fields and len( fields[x]) > 0:
        return fields[x]
    else:
        return ""



bib_sorted = sorted(bib_data.entries.items(), key=cmp_to_key( sort_list_cmp) )

prev_year = -100

idx = 0
for key, value in bib_sorted:
    # print year
    if value.fields['year'] != prev_year:
        print ( "\n= " + value.fields['year'] )

        prev_year = value.fields['year']
        prev_type = 'NONE'

    # print journal/conference/other
    if 'journal' in value.fields and prev_type != 'Journal':
        prev_type = 'Journal'
        print ( '== Journal' )
    elif 'booktitle' in value.fields and prev_type != 'Conference':
        prev_type = 'Conference'
        print ( '== Conference' )
    elif 'journal' not in value.fields and 'booktitle' not in value.fields and prev_type != 'Other':
        prev_type = 'Other'
        print ( '== Other' )


    t1 = value.fields['title']
    t1 = capitalize_string( t1 )

# Check if print the PDF thumb image
#    {{<img class="imgP  right"    src="shen2.jpg">}}

    t0 = ''
    bibentry=bib_sorted[idx][0].encode('ascii', 'ignore')

    imgURL = 'data/thumbnail/' + bibentry.decode("UTF-8") + '_arXiv.jpg'



    tfile = Path( "../"  +  imgURL )
    if tfile.is_file():                     # if the img file exists
        t0 =    '<img class="imgP  right"   src="'   +   imgURL    +  '">'

        hyperlink = pdflink_dict.get( bibentry.decode("UTF-8") + '_arXiv.jpg', '')
        if len(hyperlink) > 0:
            t0 = '<a class="imglink"  target="_blank" href="'+ hyperlink +'">' + t0 + '</a>'
        t0 = '{{' + t0 +'}}'

    imgURL  = 'data/thumbnail/' + bibentry.decode("UTF-8") + '_PDF.jpg'

    tfile   = Path( "../"  +  imgURL )
    if tfile.is_file():                     # if the img file exists
        t0  =    '<img class="imgP  right"   src="'   +   imgURL    +  '">'

        hyperlink = pdflink_dict.get( bibentry.decode("UTF-8") + '_PDF.jpg', '')
        if len(hyperlink) > 0:
            t0 = '<a class="imglink"  target="_blank" href="'+ hyperlink +'">' + t0 + '</a>'
        t0 = '{{' + t0 +'}}'

    print ( ". "  + t0 +  "*" + t1 + "*   " )

    # t2 = value.fields['author']
    # t2 = initialize_name(t2)
    # t2 = t2.replace('{', '')
    # t2 = t2.replace('}', '')
    # t2 = re.sub(" *and",  "; ", t2)



    citef   = gen_citefields( key )
    t2 = remove_curly_bracket( instance_fields('authors', citef) )
    t2 = initialize_name( t2 )

    print ( "\\n$\cdot$ /" + t2 + "/." )


    # strvol = instance_field('volume') + instance_field('number') + instance_field('pages')
    # disable volume, page etc
    strvol = ""


    if 'journal' in value.fields:
        # print "\\n    /"  + value.fields['journal']  + ", " + strvol + value.fields['year'] + "/."
        print ( "\\n$\cdot$ /"       + value.fields['journal']  + " (" + value.fields['venue']  +  "), " + strvol + value.fields['year'] + "/." )
    if 'booktitle' in value.fields:
        print ( "\\n$\cdot$ /Proc. "  + value.fields['booktitle']  + ", " + strvol + value.fields['year'] + "/." )

    if  value.fields['venue'] == "book":
        _tmp=""
        if 'publisher' in value.fields and  len( value.fields['publisher'] ) >0:
            _tmp = value.fields['publisher']  + ", "

        print ( "\\n$\cdot$   /"  + _tmp + value.fields['year'] + "/." )


    # print arXiv, if any
    printreturn = 1
    s = ''
    if 'eprint' in value.fields and len(value.fields['eprint']) > 0:
        arXiv_link = "http://arxiv.org/abs/" + value.fields['eprint']
        s = s + "\\n$\cdot$ [" + arXiv_link + "    arXiv]"
        printreturn = 0

    if 'url' in value.fields and len(value.fields['url']) > 0:
        if printreturn:
            s = s + "\\n$\cdot$ "
            printreturn = 0
        s = s + "[" + value.fields['url'] + "  link]"

    if 'pdf' in value.fields and len(value.fields['pdf']) > 0:
        if printreturn:
            s = s + "\\n$\cdot$ "
            printreturn = 0
        s = s + "[" + value.fields['pdf'] + "  pdf]"

    # print bibtex link
    bibentry=bib_sorted[idx][0].encode('ascii','ignore')
    if printreturn:
        s = s + "\\n$\cdot$ "
        printreturn = 0
    s = s + "[data/bibtex/" + bibentry.decode("UTF-8") + ".bib  " + "  bibtex]"

    idx = idx + 1


    # print google search
    if printreturn:
        s = s + "\\n$\cdot$"
        printreturn = 0

    # google scholar
    # pre_str="http://www.google.com/search?lr=&ie=UTF-8&oe=UTF-8&q="

    pre_str="https://scholar.google.com/scholar?lr&ie=UTF-8&oe=UTF-8&q="
    t1 = value.fields['title'] + "+" + value.fields['author']
    t2 = pre_str + re.sub(r' +', '+', t1.strip() )
    t2 = t2.replace("$","")
    s = s + "[" + t2 + " google scholar]"

    # semantic scholar, 10 March 2021
    pre_str="https://www.semanticscholar.org/search?q="
    t1 = value.fields['title']                                # + "+" + value.fields['author']
    t2 = pre_str + re.sub(r' +', '+', t1.strip() )
    t2 = t2.replace("$","")
    s = s + "[" + t2 + " semantic scholar]"



    # print project link, if any
    if 'project' in value.fields and len(value.fields['project']) > 0:
        if printreturn:
        #    s = s + "\\n"
            s = s + "\\n$\cdot$ "
            printreturn = 0
        s = s + "[" + value.fields['project'] + "   project webpage]"


    print(s)

    # print note at the end
    if 'note' in value.fields and len(value.fields['note']) > 0:
        t0 = value.fields['note']
        # cannot have [ ] in the note; replace them with { }
        # t0 = re.sub('^\[', '{', t0)
        # t0 = re.sub('\]$', '}', t0)
        t0 = re.sub( '\\\\n', '\\n', t0)
        if t0[0:3] != '.. ':
            t0 = '.. ' + t0

        if t0[-1] != '.':
            t0 = t0 + '.'

        print ( "        " + t0 )

#   debug_here()

