import urllib
import sys
from bs4 import BeautifulSoup

def read_data(filename):
    """
    Read in data from a file and return a list with each element being one line from the file.
    Parameters:
    1) filename: name of file to be read from
    Note: the code now opens as a binary and replaces carriage return characters with newlines because python's read and readline functions don't play well with carriage returns.
    However, this will no longer be an issue with python 3.
    """	
    with open(filename, "rb") as f:
        s = f.read().replace('\r\n', '\n').replace('\r', '\n')
        data = s.split('\n')
    return data

links_file = "/Users/jchan/Desktop/Dropbox/Research/OpenIDEO/Data/LinksAndNames/community-initiative_concepting_links_to_download.txt"
names_file = "/Users/jchan/Desktop/Dropbox/Research/OpenIDEO/Data/LinksAndNames/community-initiative_concepting_names.txt"

links = read_data(links_file)
names = read_data(names_file)

if not(len(links) == len(names)):
    print "need the same # of links and file names!"
    exit(0)

for i in range(len(links)):
    f_name = "%s%s.html" % ("HTMLFiles/", names[i])
    print "Processing %s..." % names[i]
    f = urllib.urlretrieve(links[i],f_name)

	

	