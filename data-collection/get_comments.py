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
from sys import argv, stdout
import os, csv

def extract_comments(filename, docname, challengename):

	docname = docname.replace(".html","")
	# create the big soup of comments stuff, put in a list
	soup = BeautifulSoup(open(filename),"html5lib") # CRITICAL THAT WE USE THE HTML5LIB parser, otherwise we'll lose data
	comments = soup.find_all('div',class_="comment")
	
	# iterate over the comments in the comments list
	for comment in comments:
		
		authorsoup = comment.find(class_="comment-author").find(class_="author-name")
		
		if authorsoup != None: #only proceed if it's a real author_url (i.e., actually a real comment, not just a placeholder for user-submitted comment) ALSO threw in the text soup earlier to catch that one file (food-production-consumption_C-149.html) that had a blank comment with author info but no text
			
			# get author_url
			author_url = authorsoup.find("a").get("href")
			
			bodysoup = comment.find('div',class_="comment-body clearfix")
			try:
				# get comment full-text - very hacky, have to re-encode the full-text as ascii
				# and strip away whitespace (newlines and tabs) to make for easier reading
				textsoup = bodysoup.find(class_="comment-message")
				temptext = textsoup.get_text().strip() #remove blank lines, whitespace, etc.
				temptext = temptext.encode('ascii', 'ignore') #encode to ascii
				textarr = temptext.splitlines() #split and join back together to enhance readability
				text = ""
				for t in textarr:
					text = text + t.strip() + " "
				
				# get rough word counts
				words = [w for w in text.split(" ") if any(c.isalpha() for c in w)]
				
				# get date		
				datesoup = bodysoup.find(class_="comment-date")
				date = datesoup.get_text()
				
			except:
				print "Crikey! We've got a bug!"
				continue
				
			# print out results
			resultswriter.writerow([challengename,docname,author_url,date,text,len(words)])

# get args from command-line
HTML_dir = argv[1]
resultsfilename = argv[2]

# open the results file and prepare header
resultsfile = open(resultsfilename,'w') 
resultswriter = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
resultswriter.writerow(['challenge','document','author_url','date','commenttext','numwords'])

# iterate over the sub-directories in the HTML folder (eah sub-dir is a challenge)
for d in os.listdir(HTML_dir):
	dir_name = HTML_dir + d
	if os.path.isdir(dir_name): #pesky .dsstore!!!!!!
		print "Processing %s..." %d
		files = os.listdir(dir_name)
		files = [f for f in files if f.endswith(".html")] #screen out the pesky "other" files (e.g., hidden .dsstore)
		numfiles = len(files)
		processedfiles = 0
		for f in files:
			filename = dir_name + "/" + f #make the filename
			#print "Processing %s..." %f
			extract_comments(filename,f,d) #extract its comments data and dump in the results file
			processedfiles +=1
			stdout.write("\t%d of %d files processed...\r" %(processedfiles, numfiles))
			stdout.flush()
		print "\t%d of %d files processed...\r" %(processedfiles, numfiles)
resultsfile.close()