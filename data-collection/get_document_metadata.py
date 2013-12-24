"""
Simple parser that reads in the raw HTML files for OpenIDEO concepts and inspirations
and grabs their author urls
"""

from bs4 import BeautifulSoup
from sys import argv
import os

HTML_dir = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/RawHTMLFiles/"

def get_authordata(filename):
    soup = BeautifulSoup(open(filename)) #create soup
    authorsoup = soup.find(id="content-submitted-by").find(class_="text").find("a") #grab the authordata subsoup
    return authorsoup.get('href')

resultsfile = open("/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/PythonCode/authormetadata_2013-12-20.csv",'w')
for d in os.listdir(HTML_dir): #iterate over subfolders (challenges) in top folder hierarchy
    dir_name = HTML_dir + d 
    if os.path.isdir(dir_name): #iterate over files in subfolders (documents within challenges)
        print "Processing %s..." %d
        for f in os.listdir(dir_name):
            if f.endswith(".html"):
                print "\tProcessing %s..." %f
                filename = dir_name + "/" + f
                authorurl = get_authordata(filename)
                result = "%s,%s\n" %(f, authorurl)
                resultsfile.write(result)
resultsfile.close()