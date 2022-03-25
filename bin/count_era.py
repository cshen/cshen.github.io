#!/usr/bin/env python3

# Author:        Chunhua Shen {chhshen@gmail.com}
# Creation:      Saturday 09/07/2011 21:55.
# Last Revision: Wednesday 03/04/2013 09:12.
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

parser = bibtex.Parser()
bib_data = parser.parse_file('../data/cs.bib')


Conf_A  = ["icml", "neurips", "cvpr", "iccv", "eccv", "aaai", "ijcai", "miccai", "icra", "acmmm"]
J_Astar = ["tpami", "ijcv", "tip", "tnn", "tnnls", "jasa",  "pr", "jbhi" ]
J_A     = ["tmm", "jmlr", "nn","tkde", "plme"]




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


def sort_list_cmp(y, x):

    if 'booktitle' in x[1].fields and 'booktitle' not in y[1].fields:
        return 1
    if 'booktitle' not in x[1].fields and 'booktitle' in y[1].fields:
        return -1

    if 'journal' in x[1].fields and 'journal' not in y[1].fields:
        return 1
    if 'journal' not in x[1].fields and 'journal' in y[1].fields:
        return -1


    yearcmp = int(x[1].fields['year']) - int(y[1].fields['year'])
    if yearcmp != 0:
        return yearcmp


    if x[1].fields['venue'] > y[1].fields['venue']:
        return -1
    else:
        return 1

    if x[1].fields['author'] > y[1].fields['author']:
        return 1
    else:
        return -1


bib_sorted = sorted(bib_data.entries.items(), key=cmp_to_key( sort_list_cmp) )


num_conf_A = 0
num_j_Astar = 0
num_j_A = 0

for key, value in bib_sorted:
    citef   = gen_citefields( key )
    v_ = instance_fields('venue', citef)
    v_ = v_.lower()

    if  any( v_ == s for s in Conf_A ):
        num_conf_A = num_conf_A + 1

    if  any( v_ == s for s in J_Astar ):
        num_j_Astar = num_j_Astar + 1

    if  any( v_ == s for s in J_A ):
        num_j_A = num_j_A + 1



print( num_j_Astar )
print( num_j_A )
print( num_conf_A )

