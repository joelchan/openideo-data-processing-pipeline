#! /usr/bin/python
#
# This code iterates over sub-directories in a directory
# to extract comments data from each file in each sub-directory
# IT IS VERY SPECIFIC TO MY DATASET
#
# usage: python get_comments.py <directory> <resultsfilename>
#
# At the moment, files that don't have comments don't get printed to the
# results file.

from bs4 import BeautifulSoup
from sys import argv
import os

def extract_comments(filename, docname, challengename):

    # create the big soup of comments stuff, put in a list
    soup = BeautifulSoup(open(filename))
    comments = soup.find_all(class_="comment")

    # iterate over the comments in the comments list
    for comment in comments:
        #print "Next subsoup..."
        subsoup = BeautifulSoup(str(comment))

        # get author URL - very hacky - would like to just get the right URL
        links = []
        for link in subsoup.find_all('a'):
            #print link
            if link.get('href') == "": #blank comment placeholder
                links.append("blank/url")
            else:
                links.append(link.get('href'))
        author_url = links[1]

        # get comment date - very hacky at the moment, have to make lots of subsoups!
        body = subsoup.find('div',class_="comment-body clearfix")
        subsoup_body = BeautifulSoup(str(body))
        datesoup = BeautifulSoup(str(subsoup_body.find(class_="comment-date")))
        date = datesoup.get_text()
    
        # get comment full-text - very hacky, have to re-encode the full-text as ascii
        # and strip away whitespace (newlines and tabs) to make for easier reading
        textsoup = BeautifulSoup(str(subsoup_body.find(class_="comment-message")))
        temptext = textsoup.get_text().strip()
        temptext = temptext.encode('ascii', 'ignore')
        textarr = temptext.splitlines()
        text = ""
        for t in textarr:
            text = text + t.strip() + " "
    
        # print to resultsfile
        if "profiles" in author_url:
            temp = author_url.split("/")
            author_url = temp[len(temp)-2]
            towrite = "%s\t%s\t%s\t%s\t%s\n" %(challengename, docname, author_url, date, text)
            results.write(towrite)	

# get args from command-line
HTML_dir = argv[1]
resultsfilename = argv[2]

# open the results file and prepare header
results = open(resultsfilename,'w') 
results.write("challenge\tdocument\tauthor_url\tdate\ttext\n")

# iterate over the sub-directories in the HTML folder (eah sub-dir is a challenge)
for d in os.listdir(HTML_dir):
	dir_name = HTML_dir + d
	if os.path.isdir(dir_name): #pesky .dsstore!!!!!!
		for f in os.listdir(dir_name):
			if f.endswith(".html"):
			    print "Getting comments from %s..." %f
			    filename = dir_name + "/" + f #make the filename
			    extract_comments(filename,f,d) #extract its comments data and dump in the results file

#for root, dirs, files in os.walk(HTML_dir):
#	for d in dirs:
#		print os.path.abspath(d)
    #for name in files: # for each HTML file
    #    if name.endswith(".html"):
    #        print "Getting comments from %s..." %os.path.abspath(name)
    #        #filename = HTML_dir + name #make the filename
    #        extract_comments(os.path.abspath(name)) 

results.close()
	
	
	