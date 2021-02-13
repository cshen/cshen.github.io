#!/usr/bin/env python2


from pybtex.database.input import bibtex
from operator import itemgetter, attrgetter
import pprint
import re
from pathlib import  Path

from helper  import  PrintSelectVenueHeader as  headerinfo



mybibtexfile = '../data/cs.bib'

parser = bibtex.Parser()
bib_data = parser.parse_file( mybibtexfile )





Selected_Conf_List=[ "cvpr", "iccv", "eccv", "icml", "neurips", "tpami", "ijcv", "jmlr"]




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

        if transform:
            y = y + x[ i ].lower()
        else:
            y = y + x[ i ]

        z =''
        z = z + y[0].upper()
        z = z + y[1:len(y)]
    return z

def sort_list_cmp(y, x):


    if 'journal' in x[1].fields and 'journal' not in y[1].fields:
        return 1
    if 'journal' not in x[1].fields and 'journal' in y[1].fields:
        return -1



    if 'booktitle' in x[1].fields and 'booktitle' not in y[1].fields:
        return 1
    if 'booktitle' not in x[1].fields and 'booktitle' in y[1].fields:
        return -1


    yearcmp = int(x[1].fields['year']) - int(y[1].fields['year'])
    if yearcmp != 0:
        return yearcmp

    if x[1].fields['venue'] > y[1].fields['venue']:
        return -1
    elif x[1].fields['venue'] < y[1].fields['venue']:
        return 1

    if x[1].fields['author'] > y[1].fields['author']:
        return -1
    elif x[1].fields['author']  <  y[1].fields['author']:
        return 1



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

def remove_curly_bracket(x):
    x = x.replace('{', '')
    x = x.replace('}', '')


    return x

def bibtex_author_sep(x):
     x = x.replace(',', ' and ')
     return x

def instance_fields( x, fields ):
    if x in fields and len( fields[x]) > 0:
        return fields[x]
    else:
        return ""


def instance_field(x):
    if x in value.fields and len(value.fields[x]) > 0:
        return " " + x + " " + value.fields[x] + ", "
    else:
        return ""



bib_sorted = sorted(bib_data.entries.items(), cmp=sort_list_cmp)

prev_type = "NONE"

idx = 0

j_idx = 0
c_idx = 0

for key, value in bib_sorted:

    citef   = gen_citefields( key )

    v_ = instance_fields('venue', citef)
    if not any( v_.lower() == s for s in Selected_Conf_List ):
        idx = idx + 1
        continue

    t1 = value.fields['title']
    t1 = capitalize_string( t1 )


    t0 = ''
    bibentry=bib_sorted[idx][0].encode('ascii','ignore')



    t2 = remove_curly_bracket( instance_fields('authors', citef) )
    t2 = initialize_name( t2 )
    t2 = bibtex_author_sep(t2)

    strvol = ""



    if 'journal' in value.fields:
        j_idx = j_idx + 1
        print "@article{J"     + str(j_idx) + ","
        print "  journal = {"   + value.fields['journal']  + "},"


    if 'booktitle' in value.fields:
        c_idx = c_idx + 1
        print "@inproceedings{C"  + str(c_idx) + ","
        print "  booktitle = {"   + value.fields['booktitle']  + "},"


    print "  title   = {"   + t1 +  "},"
    print "  author  = {"   + t2 +  "},"
    print "  year    = {"   + value.fields['year'] + "},"

    vv=''
    if 'volume' in value.fields:
        vv = value.fields['volume']
    print "  volume  = {"   + vv   + "},"



    print "}"
    print ""




