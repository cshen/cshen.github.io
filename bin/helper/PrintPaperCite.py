

from subprocess import Popen, PIPE, STDOUT
from os.path import relpath, dirname, join
import sys

url=[];

def init( inurl ):
    global url
    url = inurl

def mynum(s):
    try:
        return int(s)
    except ValueError:
        return -1


def get_citations():

    ppath = relpath(join(dirname(__file__).encode(sys.getfilesystemencoding()), './get_paper_cite.sh   '))

    p=Popen(  './' + ppath + str(url) , shell=True, stdout=PIPE, stderr=STDOUT, close_fds=True)

    out = p.stdout.read()
    out2 = out.replace('\n', ' ').replace('\r', '')
    out3 = mynum(out2)

    return out3


if __name__ == "__main__":

    myurl1="Adaptive+object+tracking+based+on+an+effective+appearance+filter+Wang,+Hanzi+and+Suter,+David+and+Schindler,+Konrad+and+Shen,+Chunhua"

    myurl2="Plague:+Fine-Grained+Learning+for+Visual+Question+Answering+Zhou,+Yiyi+and+Ji,+Rongrong+and+Su,+Jinsong+and+Sun,+Xiaoshuai+and+Meng,+Deyu+and+Gao,+Yue+and+Shen,+Chunhua"



    init(myurl1)
    out1 = get_citations()
    print ( out1 )


    init(myurl2)
    out2 = get_citations()
    print ( out2 )
