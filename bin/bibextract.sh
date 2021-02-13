#!/usr/bin/env bash
### ====================================================================
###  @UNIX-shell-file{
###     author          = "Nelson H. F. Beebe",
###     version         = "1.09",
###     date            = "25 August 2001",
###     time            = "17:46:02 MDT",
###     filename        = "bibextract.sh",
###     address         = "Center for Scientific Computing
###                        University of Utah
###                        Department of Mathematics, 322 INSCC
###                        155 S 1400 E RM 233
###                        Salt Lake City, UT 84112-0090
###                        USA",
###     telephone       = "+1 801 581 5254",
###     FAX             = "+1 801 585 1640, +1 801 581 4148",
###     URL             = "http://www.math.utah.edu/~beebe",
###     checksum        = "20889 126 556 5060",
###     email           = "beebe@math.utah.edu, beebe@acm.org,
###                        beebe@ieee.org (Internet)",
###     codetable       = "ISO/ASCII",
###     keywords        = "BibTeX, bibliography, citation label,
###                        citation tag",
###     supported       = "yes",
###     docstring       = "Extract a subset of one or more bibtex
###                        files according to a regular expression
###                        pattern given on the command line, writing
###                        them on stdout.
###
###                        The pattern should avoid upper-case
###                        letters; the matching will be against a
###                        lower-cased copy of the BibTeX entry, to
###                        make letter case insignificant.
###
###                        Usage:
###                             bibextract 'keyword-pat' 'regexp-pat' \
###                                bibtex-file(s) >new-bibtex-file
###
###                        If the keyword-pat pattern is empty,
###                        matching occurs against the entire
###                        bibliographic entry.
###
###                        Here are some examples:
###
###                        Extract all entries mentioning chaos in any field:
###
###                             bibextract "" "chaos" file(s) >new-bibtex-file
###
###                        Extract entries with names Brown or Smith
###                        occurring in either of the author or editor
###                        fields:
###
###                             bibextract "author|editor" "brown|smith" \
###                                 file(s) >new-bibtex-file
###
###                        Extract entries for titles containing the
###                        letter z anywhere after a vowel; note that
###                        single quotes are necessary to provide the
###                        necessary protection from shell expansion:
###
###                             bibextract "title" '[aeiou].*z' file(s) \
###                                 >new-bibtex-file
###
###                        The checksum field above contains a CRC-16
###                        checksum as the first value, followed by the
###                        equivalent of the standard UNIX wc (word
###                        count) utility output of lines, words, and
###                        characters.  This is produced by Robert
###                        Solovay's checksum utility.",
###  }
### ====================================================================

### Edit history (reverse chronological order):
### [25-Aug-2001]	1.09	Update file header data.
###
### [19-Feb-1999]	1.08	Update file header data.
###
### [16-May-1998]	1.07	Update file header data.
###
### [24-Aug-1994]	1.06	Update bibextract.awk to handle matches
###				with alternate patterns and @string
###				abbreviations, and update the manual
###				page file, bibextract.man, with new
###				examples.
###
### [23-Aug-1994]	1.05	Correct name of temporary file.
###
### [22-Jul-1994]	1.04	Eliminate printbraceditem() in favor of
###				using collectbraceditem(), which now
###				checks for balanced braces to avoid
###				possibility of an infinite loop.
###
###
### [17-Jul-1994]	1.03	Revise to output only those @String{...}
###				entries that are actually used by the
###				matched entries.
###
### [30-Oct-1992]	1.02	Fix typographical error.
###
### [21-Oct-1992]       1.01    Update for public distribution.
###
### [08-May-1989]       1.00    Original version.



TMPFILE=/tmp/bibextract.$$
# LIBDIR=@LIBDIR@
# LIBDIR=.




trap '/bin/rm -f ${TMPFILE}'  2  1

# Force the keyword and pattern to lowercase.
keyword=`echo $1 | tr ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz`
pattern=`echo $2 | tr ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz`

Gsed=sed

[[ "$OSTYPE" == "darwin"* ]] && Gsed=gsed

# Make a new awk program with the patterns built in.
$Gsed         -e "sKEYWORD$keyword"\
            -e "sPATTERN$pattern"\
            < ./bibextract.awk >${TMPFILE}

# Discard first 2 arguments (keyword-pat and regexp-pat)
shift
shift

# Extract the bibliography subset
# nawk -f ${TMPFILE} $*

Gawk=awk
[[ "$OSTYPE" == "darwin"* ]] && Gawk=gawk

$Gawk -f ${TMPFILE} $*


# discard our temporary file
/bin/rm -f ${TMPFILE}
