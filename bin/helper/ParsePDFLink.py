import csv

# link_file='_PDFLink.txt'
def readlinkfile( link_file ):

    key=[]
    val=[]
    dict1={}

    try:
        with open( link_file, 'r') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:

                if (len(row) > 0):
                    key.append( row[0].strip() )
                    val.append( row[1].strip() )

            dict1 = dict(zip(key, val))

    except IOError:
        return False


    return dict1, key, val
