

from pybtex.database.input import bibtex
from operator import itemgetter, attrgetter
import pprint
import re
from pathlib import  Path


venuefull = {'icml': 'Proc. International Conference on Machine Learning (ICML)',
             'neurips' : 'Proc. Advances in Neural Information Processing Systems (NeurIPS)',
             'eccv': 'Proc. European Conference on Computer Vision (ECCV)',
             'iccv': 'Proc. IEEE International Conference on Computer Vision (ICCV)',
             'cvpr': 'Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)',
             'ijcv':  'International Journal of Computer Vision (IJCV)',
             'tpami': 'IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)',
             'jmlr' : 'Journal of Machine Learning Research (JMLR)',
	     'tog'  : 'ACM Transactions on Graphics (TOG)',
}



parser = bibtex.Parser()

# Global variables
bib_data = [];
bib_entries = [];
selected_venues = [];


def init( bibtex_file, selected_list_input ):
    global bib_entries
    global selected_venues
    global bib_data

#    bib_data = parser.parse_file('../../data/cs.bib')
    bib_data = parser.parse_file( bibtex_file )
    bib_entries = bib_data.entries.items()
    selected_venues = selected_list_input





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


def count_venue( s_venue ):

    idx = 0
    is_journal = 0
    is_conf = 0

    for key, value in bib_entries:

        citef   = gen_citefields( key )
        v_ = instance_fields('venue', citef)

        if ( v_.lower() == s_venue  ):
            idx = idx + 1

            if 'journal' in value.fields:
                is_journal = 1

            if 'booktitle' in value.fields:
                is_conf = 1

    return idx, is_journal, is_conf


def count_selected_venues( venue_list ):

    counts     = [];
    is_journal = [];
    is_conf    = [];

    for iv in venue_list:
        pp, j_, c_ = count_venue( iv )
        counts.append( pp  )
        is_journal.append( j_ )
        is_conf.append( c_ )

    return counts, is_journal, is_conf


def print_conf( ):
    num, is_journal, is_conf = count_selected_venues ( selected_venues )

    _tot_num_c =  0
    for i in range( len(num) ):
        if  is_conf [ i ] == 1:
            _tot_num_c = _tot_num_c + num[i]

    print ('== Conference: ' + str( _tot_num_c ) )


    for i in range( len(num) ):
        if  is_conf[ i ] == 1:
            s =   venuefull [ selected_venues[ i ] ] + ': '  + str( num[ i ] )
            print ( '===  ' + s )


def print_journal( ):
    num, is_journal, is_conf = count_selected_venues ( selected_venues )

    _tot_num_j = 0
    for i in range( len(num) ):
        if  is_journal[ i ] == 1:
            _tot_num_j = _tot_num_j + num[i]


    print ( '== Journal: ' + str( _tot_num_j ) )

    for i in range( len(num) ):
        if  is_journal[ i ] == 1:
            s =   venuefull [ selected_venues[ i ] ] + ': '  + str( num[ i ] )
            print ( '===  ' + s )



if __name__ == "__main__":
    bf = '../../data/cs.bib'
    bl = ["cvpr", "iccv", "eccv", "icml", "neurips", "tpami", "ijcv", "jmlr"]

    init( bf, bl )
    print_conf()
    print_journal()

