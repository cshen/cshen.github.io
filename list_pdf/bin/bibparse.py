#!/usr/bin/env python3
#
# Author:        Chunhua Shen [http://cs.adelaide.edu.au/~chhshen/], The University of Adelaide
# Creation:      Tuesday 08/01/2013 19:15.
# Last Revision: Monday 11/02/2013 11:43.
# CS, 11 Feb 2013, add link to the title
# CS, 2020 July, now using Python3

from __future__ import print_function
import pkg_resources
pkg_resources.require("pybtex==0.18")



try:
    from pybtex.database.input.bibtex import Parser
except ImportError:
    print("You need to install pybtex first!")

import re
# from datetime import datetime
# import os.path
# from IPython.core.debugger import Tracer
# debug_here = Tracer()

from functools import cmp_to_key

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
    else:
        return 1

    if x[1].fields['title'] > y[1].fields['title']:
        return 1
    else:
        return -1


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


# highlight = "C. +Shen"
def highlight_name( strx,  highlight  ):

    x = highlight.replace('+', '')
    x = r"\\highlight{" + x + "}"
    s = re.sub( highlight, x, strx )

    return s



def capitalize_string(x):

    # x = x.decode('ascii', 'ignore')

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


def remove_curly_bracket(x):
    x = x.replace('{', '')
    x = x.replace('}', '')
    return x


def single_dash(x):
    for i in range(10):
        x = x.replace('--', '-')

    x = x.replace('-', '$-$')
    return x


def instance_fields( x, fields ):
    if x in fields and len( fields[x]) > 0:
        return fields[x]
    else:
        return ""


BIBFILE = 'cs.bib'


jfile = open('journal.text', 'w')
cfile = open('conf.text', 'w')

cfile_selected = open('conf_selected.text', 'w')
cfile_selected2 = open('conf_selected2.text', 'w')

cfile_other    = open('conf_other.text', 'w')


parser = Parser()
bib_data = parser.parse_file( BIBFILE )
bib_sorted = sorted(bib_data.entries.items(), key=cmp_to_key( sort_list_cmp))

jnumber = 0
jyear   = 9999
print_jyear = 0

cnumber = 0
cyear   = 9999
print_cyear = 0

cnumber_select = 0
cyear_select   = 9999
print_cyear_select = 0

cnumber_select2 = 0
cyear_select2   = 9999
print_cyear_select2 = 0



cnumber_other = 0
cyear_other   = 9999
print_cyear_other = 0


Selected_Conf_List=["icml", "neurips", "cvpr", "iccv", "eccv"]

# 2019 March
Selected_Conf_List2=["aaai", "ijcai", "icra", "bmvc", "kdd", "miccai", "acmmm"]





for key, value in bib_sorted:
    citef   = gen_citefields( key )
    author_ = remove_curly_bracket( instance_fields('authors', citef) )
    author_ = initialize_name( author_ )
    author_ = highlight_name( author_, "C. +Shen" )

    year_   = instance_fields('year', citef)

    title_  = capitalize_string( instance_fields('title', citef) )

    # Google search
    pre_str = "http://www.google.com/search?lr=&ie=UTF-8&oe=UTF-8&q="
    t1 = remove_curly_bracket(value.fields['title']) + "+" + remove_curly_bracket(value.fields['author'])
    t2 = pre_str + re.sub(r' +', '+', t1.strip() )
    title_ = "\href{" + t2 + "}{" + title_ + "}"


    pages_  = instance_fields('pages', citef)
    pages_  = single_dash( pages_ )

    vol_    = instance_fields('volume', citef)

    # if (len(pages_) > 0 ):
    #   pages_ = ": " + pages_

    if 'article' == bib_data.entries[ key ].type:
        jnumber = jnumber + 1

        y = int( citef['year'] )
        if y != jyear:
            jyear = y
            print_jyear = 1
        else:
            print_jyear = 0

        journal_  = instance_fields('journal', citef)

        print("%%", file=jfile )
        print("%% " + key, file=jfile )


        if print_jyear == 1:
            print("\id{" + str(jnumber) + "~~" + str( y ) + "}", file=jfile, end='')
        else:
            print("\id{" + str(jnumber) + "}",  file=jfile, end='')

        print("\decoauthor{" + author_ +  "}",  file=jfile )
        print("\decoyear{" + year_ +  "}",  file=jfile, end='')
        print("\decotitle{" + title_ +  "}",  file=jfile)
        print("\decojournal{" + journal_ + "}",  file=jfile, end='')
        print("\decovolume{" + vol_ +   "}",  file=jfile, end='')
        print("\decopage{" + pages_ +   "}",  file=jfile, end='')
        print("\\\\[.125cm]",  file=jfile)

    elif 'inproceedings' == bib_data.entries[ key ].type:

        cnumber = cnumber + 1
        y = int( citef['year'] )
        if y != cyear:
            cyear = y
            print_cyear = 1
        else:
            print_cyear = 0

        conf_  = instance_fields('booktitle', citef)

        print("%%", file=cfile )
        print("%% " + key, file=cfile )

        if print_cyear == 1:
            print("\id{" + str(cnumber) + "~~" + str( y ) + "}", file=cfile, end='')
        else:
            print("\id{" + str(cnumber) + "}",  file=cfile, end='')

        print("\decoauthor{" + author_ +  "}",  file=cfile )
        print("\decoyear{" + year_ +  "}",  file=cfile, end='')
        print("\decotitle{" + title_ +  "}",  file=cfile)
        print("\decoconf{" + conf_ + "}",  file=cfile, end='')
        # print("\decovolume{" + vol_ + "}",  file=cfile, end='')
        print("\decopage{" + pages_ +   "}",  file=cfile, end='')
        print("\\\\[.125cm]",  file=cfile)

        if any( citef['venue'].lower() == s for s in Selected_Conf_List ):
            print("%%", file=cfile_selected )
            print("%% " + key, file=cfile_selected )

            cnumber_select = cnumber_select + 1

            if y != cyear_select:
                cyear_select = y
                print_cyear_select = 1
            else:
                print_cyear_select = 0

            if print_cyear_select == 1:
                print("\id{" + str(cnumber_select) + "~~" + str( y ) + "}",
                        file=cfile_selected, end='')
            else:
                print("\id{" + str(cnumber_select) + "}",   file=cfile_selected, end='')

            print("\decoauthor{" + author_ +  "}",  file=cfile_selected )
            print("\decoyear{" + year_ +  "}",  file=cfile_selected, end='')
            print("\decotitle{" + title_ +  "}",  file=cfile_selected)
            print("\decoconf{" + conf_ + "}",  file=cfile_selected, end='')
            # print("\decovolume{" + vol_ + "}",  file=cfile_selected, end='')
            print("\decopage{" + pages_ +   "}",  file=cfile_selected, end='')
            print("\\\\[.125cm]",  file=cfile_selected)





# Part 2 Conf.  AAAI, IJCAI, ICRA


        elif any( citef['venue'].lower() == s for s in Selected_Conf_List2  ):
            print("%%", file=cfile_selected2 )
            print("%% " + key, file=cfile_selected2 )

            cnumber_select2 = cnumber_select2 + 1

            if y != cyear_select2:
                cyear_select2 = y
                print_cyear_select2 = 1
            else:
                print_cyear_select2 = 0

            if print_cyear_select2 == 1:
                print("\id{" + str(cnumber_select2) + "~~" + str( y ) + "}",
                        file=cfile_selected2, end='')
            else:
                print("\id{" + str(cnumber_select2) + "}",   file=cfile_selected2, end='')

            print("\decoauthor{" + author_ +  "}",  file=cfile_selected2 )
            print("\decoyear{" + year_ +  "}",  file=cfile_selected2, end='')
            print("\decotitle{" + title_ +  "}",  file=cfile_selected2)
            print("\decoconf{" + conf_ + "}",  file=cfile_selected2, end='')
            # print("\decovolume{" + vol_ + "}",  file=cfile_selected2, end='')
            print("\decopage{" + pages_ +   "}",  file=cfile_selected2, end='')
            print("\\\\[.125cm]",  file=cfile_selected2)



        else:

            print("%%", file=cfile_other )
            print("%% " + key, file=cfile_other )

            cnumber_other = cnumber_other + 1

            if y != cyear_other:
                cyear_other = y
                print_cyear_other = 1
            else:
                print_cyear_other = 0

            if print_cyear_other == 1:
                print("\id{" + str(cnumber_other) + "~~" + str( y ) + "}",
                        file=cfile_other, end='')
            else:
                print("\id{" + str(cnumber_other) + "}",    file=cfile_other, end='')

            print("\decoauthor{" + author_ +  "}",  file=cfile_other )
            print("\decoyear{" + year_ +  "}",  file=cfile_other, end='')
            print("\decotitle{" + title_ +  "}",  file=cfile_other)
            print("\decoconf{" + conf_ + "}",  file=cfile_other, end='')
            # print("\decovolume{" + vol_ + "}",  file=cfile_other, end='')
            print("\decopage{" + pages_ +   "}",  file=cfile_other, end='')
            print("\\\\[.125cm]",  file=cfile_other)



fn_journals = open('num_journals.text', 'w')
print(jnumber, file=fn_journals)

fn_confs = open('num_confs.text', 'w')
print(cnumber, file=fn_confs)

fn_confs_s = open('num_confs_select.text', 'w')
print(cnumber_select, file=fn_confs_s)


fn_confs_s2 = open('num_confs_select2.text', 'w')
print(cnumber_select2, file=fn_confs_s2)



fn_confs_o = open('num_confs_other.text', 'w')
print(cnumber_other, file=fn_confs_o)



























# vim: ft=python ts=4 sw=4 :
# EoF

