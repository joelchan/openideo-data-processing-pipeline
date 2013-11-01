from bs4 import BeautifulSoup

results = open("parsetestresults.txt",'w')

# create the big soup of comments stuff, put in a list
document = "/Users/joelc/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Data/RawHTMLFiles/e-waste/all/C-digital-data-transfer-and-elimination-service-.html"
soup = BeautifulSoup(open(document))
comments = soup.find_all(class_="comment")

# iterate over the comments in the comments list
for comment in comments:
    print "Next subsoup..."
    subsoup = BeautifulSoup(str(comment))
    
    # get author URL - very hacky - would like to just get the right URL
    links = []
    for link in subsoup.find_all('a'):
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
	    towrite = "%s\t%s\t%s\n" %(author_url, date, text)
	    results.write(towrite)	
results.close()
	
	
	