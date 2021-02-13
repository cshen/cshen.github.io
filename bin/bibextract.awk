### ====================================================================
###  @Awk-file{
###     author          = "Nelson H. F. Beebe",
###     version         = "1.09",
###     date            = "25 August 2001",
###     time            = "17:44:41 MDT",
###     filename        = "bibextract.awk",
###     address         = "Center for Scientific Computing
###                        University of Utah
###                        Department of Mathematics, 322 INSCC
###                        155 S 1400 E RM 233
###                        Salt Lake City, UT 84112-0090
###                        USA",
###     telephone       = "+1 801 581 5254",
###     FAX             = "+1 801 585 1640, +1 801 581 4148",
###     URL             = "http://www.math.utah.edu/~beebe",
###     checksum        = "23217 261 1158 9297",
###     email           = "beebe@math.utah.edu, beebe@acm.org,
###                        beebe@computer.org, beebe@ieee.org (Internet)",
###     codetable       = "ISO/ASCII",
###     keywords        = "BibTeX, bibliography",
###     supported       = "yes",
###     abstract        = "This file is a template for bibextract.sh
###                        to produce a temporary awk program for
###                        extracting bibliography entries selected
###                        by particular keywords.",
###     docstring       = "*********************************************
###                        This code is hereby placed in the PUBLIC
###                        DOMAIN and may be redistributed without any
###                        restrictions.
###                        *********************************************
###
###                        NB: This file is not used directly by awk,
###                        but rather is a template for bibextract.sh
###                        to produce a temporary file with an awk
###                        program to do the work.  This subterfuge is
###                        necessary because there is no convenient
###                        way to provide a pattern for an awk program
###                        at run time.  The strings replaced by
###                        bibextract.sh are upper-case versions of
###                        'keyword' and 'pattern'.
###
###                        Matching entries are found in each of the
###                        file arguments as BibTeX bib files and
###                        output to stdout.  @preamble{} and
###                        @string{} entries are automatically output
###                        as well.
###
###                        Usage:
###                             nawk -f bibextract.awk bibfile(s) >newbibfile
###
###                        To be recognized, bib entries must look like
###
###                        @keyword{tag,
###                        ...
###                        }
###
###                        where the start @ appears in column 1, and
###                        the complete entry has balanced braces.
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
### [25-Aug-2001]	1.09	Update file header data, and output
###				GNU Emacs editing mode comment.
### [19-Feb-1999]	1.08	Update file header data.
### [16-May-1998]	1.07	Update file header data.
### [24-Aug-1994]	1.06	Parenthesize substituted keyword and
###				pattern so that they can include
###				alternates, e.g.  "author|editor".
###				Add match_keyword() to handle case of
###				`key = abbrev' as well as the old `key
###				= "value"'.  Add output of `bibsource =
###				"URL"' lines when input is not from
###				stdin.
### [23-Aug-1994]	1.05	Correct name of script in comment.
### [22-Jul-1994]	1.04	Eliminate printbraceditem() in favor of
###				using collectbraceditem(), which now
###				checks for balanced braces to avoid
###				possibility of an infinite loop.
### [17-Jul-1994]	1.03	Revise to output only those @String{...}
###				entries that are actually used by the
###				matched entries.
### [30-Oct-1992]	1.02	Fix typographical error in bibextract.sh
### [21-Oct-1992]       1.01    Update for public distribution
### [08-May-1989]       1.00    original version

BEGIN	{ "hostname" | getline hostname
	"pwd" | getline cwd
	URL_prefix = (hostname != "") ? ("file://" hostname) : ""
	print "%%% -*-BibTeX-*-"
 }

# @string and @preamble -- collect up to paired closing brace

/^@[Pp][Rr][Ee][Aa][Mm][Bb][Ll][Ee]{/        { # brace balance -> }
    print collectbraceditem()
    print ""
}

/^@[sS][tT][rR][iI][nN][gG]{/        { savestring() }

# "@keyword{tag," -- collect up to line starting with right brace
/^@[a-zA-Z0-9]*{/       {
    item = collectbraceditem()
    if ("KEYWORD" == "")        # line is changed by bibextract.sh
    {
        if (lowercase(item) ~ /(PATTERN)/) # line is changed by bibextract.sh
	    save_entry(item)
    }
    else                        # match against text of selected field(s)
    {
        lcitem = lowercase(item)
	match_keyword(lcitem)
        while (RLENGTH > 0)
        {                       # loop over all keyword-pattern matches
            field = substr(lcitem,RSTART,RLENGTH)
#           if (RLENGTH > 0)
#               printf ("%%DEBUG%% %s\n",field)
            if (field ~ /(PATTERN)/) # line is changed by bibextract.sh
            {
		save_entry(item)
                break          # exit loop after printing
            }
            lcitem = substr(lcitem,RSTART+RLENGTH)
	    match_keyword(lcitem)
        }
    }
  }

END {

    for (m = 0; m < num_string; ++m)
    {				# print just those @String{...} entries used
#	print "DEBUG: [" abbrev[m] "]"
	for (k = 0; k < num_entry; ++k)
	{
	    if (index(entry[k],abbrev[m]) > 0)
	   {
#	       print "DEBUG: <" entry[k] ">[" k "]"
	       print string[m],"\n"
	       break
	   }
	}
    }
    for (k = 0; k < num_entry; ++k) # print the matched entries
	print entry[k],"\n"
}



function bracecount(s, k,n)
{
    n = 0
    for (k = 1; k <= length(s); ++k)
    {
        if (substr(s,k,1) == "{")
            n++
        else if (substr(s,k,1) == "}")
            n--
    }
    return (n)
}

# Starting with the current contents of $0, collect lines until we
# reach a zero brace count, and return the complete entry as a string
# value.  In order to prevent infinite loops in the event of unbalance
# braces, we abort with an error message if a line is found beginning
# with an @ character

function collectbraceditem( count,item)
{
    count = bracecount($0)
    item = $0
    while (count != 0)
    {
        if (getline <= 0)
            break
	if ($0 ~ /^[ \t]*@/)
	{
	    print "ERROR: Unbalanced brace detected at line", FNR, \
		" in entry before [" $0 "]" > "/dev/tty"
	    exit(1)
	}
        item = item "\n" $0
        count += bracecount($0)
    }
    return (item)
}


# Return a lower-cased copy of the argument string.

function lowercase(s, t,k,letter)
{
    t = s
    for (k = 1; k <= length(s); ++k)
    {
        letter = substr(t,k,1)
        if (("A" <= letter) && (letter <= "Z"))
        {
            letter = substr("abcdefghijklmnopqrstuvwxyz",
                index("ABCDEFGHIJKLMNOPQRSTUVWXYZ",letter),1)
            t = substr(t,1,k-1) letter substr(t,k+1)
        }
    }
#   printf ("%%DEBUG%% %s\n",t)
    return (t)
}

function match_keyword(lcitem)
{
    if (match(lcitem,/(KEYWORD)[ \t]*=/)) # quick check for `key ='
    {				# expect key = "value" or key = abbrev
	match(lcitem,/(KEYWORD)[ \t]*=[ \t]*"[^"]*"/) || \
	    match(lcitem,/(KEYWORD)[ \t]*=[ \t]*[^,]*,/)
    }
}

function save_entry(item)
{
    sub(/[ \t]*$/,"",item) # strip trailing space
 #   if ((FILENAME != "-") && (substr(item,length(item),1) == "}"))
 # CS: I don't want to have `bibsource'    
    if (0)
    {				# add a record of where we extracted this from
	bibsource = "  bibsource =    \"" \
	    URL_prefix \
	    ((substr(FILENAME,1,1) == "/") ? "" : cwd "/") \
	    FILENAME "\","
	if (substr(item,length(item)-2,2) == ",\n")
	    item = substr(item,1,length(item)-1) bibsource "\n}"
	else if (substr(item,length(item)-1,1) == "\n")
	    item = substr(item,1,length(item)-2) ",\n" bibsource "\n}"
    }
    entry[num_entry++] = item	# save item, preserving input order
}

# Starting with the current contents of $0, collect lines until we
# reach a zero brace count, and then save the string value along
# with a reference count for the abbreviation.

function savestring( s,t)
{
    s = collectbraceditem()
    t = s			# collect the abbreviation name in t
    gsub(/^[^{]*{/,"",t)	# brace balance -> } }
    gsub(/ *=.*$/,"",t)
    abbrev[num_string] = t	# and save the entire @String{...}
    string[num_string] = s	# and its abbreviation name preserving
				# the input order
#   print "DEBUG: abbrev[" num_string "] = <" t "> length = " length(t)
    num_string++
}

### ====================================================================
