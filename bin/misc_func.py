import pybtex
from pybtex.database.input import bibtex
from operator import itemgetter, attrgetter
import pprint
import re

from functools import cmp_to_key





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

def load_citekey(bibdata, citekey):
# Get the info corresponding to specific citekey
    entry = bibdata.entries[citekey]
    return entry

def gen_citefields( bibdata, citekey):
# Rearrange the bib entries into something more useful.
    entry = load_citekey(bibdata, citekey)
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


