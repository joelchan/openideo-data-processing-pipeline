import pandas as pd
from nltk.tokenize import TreebankWordTokenizer
from sys import stdout

def remove_urls(words):
	newwords = []
	for word in words:
		if word.count("-") < 3 and word.count('.') < 2 and word.count('/') < 2 and not '.com' in word and not '.pdf' in word:
			newwords.append(word)
	return newwords

def remove_punctuation_only(words):
	newwords = []
	for word in words:
		if any(c.isalpha() for c in word):
			newwords.append(word)
	return newwords

def remove_trailing_punctuation(words):
    newwords = []
    for word in words:
        punct = True
        while punct:
            if word[-1].isalpha():
                punct = False
                newwords.append(word)
            else:
                word = word[:-1]
    return newwords

def remove_leading_punctuation(words):
	newwords = []
	for word in words:
		punct = True
		while punct:
			if word[0].isalpha():
				punct = False
				newwords.append(word)
			else:
				word = word[1:]
	return newwords

def remove_weird_words(words,weirdwords):
    newwords = []
    for word in words:
        if word not in weirdwords:
            newwords.append(word)
    return newwords

def split_slashes_and_periods(words):
	newwords = []
	for word in words:
		if '/' in word:
			temp = word.split('/')
			for t in temp:
				newwords.append(t)
		elif '.' in word:
			temp = word.split('.')
			for t in temp:
				newwords.append(t)
		else:
			newwords.append(word)
	return newwords

def clean_raw_text(rawtext):
    cleantext = ""
    rawtext = rawtext.encode("utf-8", "ignore") #then convert from unicode to to utf-8
    tokens = TreebankWordTokenizer().tokenize(rawtext)
    tokens = remove_urls(tokens)
    tokens = remove_punctuation_only(tokens)
    tokens = remove_leading_punctuation(tokens)
    tokens = split_slashes_and_periods(tokens)
    tokens = remove_weird_words(tokens,weirdwords)
    for token in tokens:
        cleantext = cleantext + token + " "
    cleantext += "\n\n"
    return cleantext

def make_author_id(author,author_id_mappings,id_counter):
    if author not in author_id_mappings:
        if id_counter < 10:
            author_id = "000%i" %id_counter
        elif id_counter < 100:
            author_id = "00%i" %id_counter
        elif id_counter < 1000:
            author_id = "0%i" %id_counter
        else:
            author_id = str(id_counter)
        author_id_mappings[author] = author_id
        id_counter += 1
        
        return id_counter

def get_post_text(author,post_metadata,postdir):
    posttext = ""
    for post in post_metadata[post_metadata['authorID'] == author]['nodeID']:
        postfilename = postdir + post + ".txt"
        rawtext = open(postfilename).read().decode("utf-8", "ignore") #first convert from utf-8 to unicode
        posttext += clean_raw_text(rawtext)
    return posttext  

def get_comment_text(comments):
    comments_by_author = {}
    for i in xrange(len(comments)):
        thisauthor = comments.ix[i]['author_url']
        thiscomment = str(comments.ix[i]['commenttext'])
        thiscomment = clean_raw_text(thiscomment)
        if thisauthor in comments_by_author:
            updatedcomment = comments_by_author[thisauthor] + thiscomment
            comments_by_author[thisauthor] = updatedcomment
        else:
            comments_by_author[thisauthor] = thiscomment
        stdout.write("\t%d of %d comments processed...\r" %(i+1, len(comments)))
        stdout.flush()
    return comments_by_author

# Parameters
comments_file = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/AllCommentsData_2013-12-25.csv"
author_metadata_file = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/AuthorData_EmilyThesisSample_2013-12-30.csv"
post_metadata_file = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/AllMetaData_CSV_2013-12-30.csv"
outdir = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/PostsByAuthor/"
postdir = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/RawTextDescriptions/"
weirdwords = ['http','nbsp']

# Read in the data files
comments = pd.read_csv(comments_file)
author_metadata = pd.read_csv(author_metadata_file)
post_metadata = pd.read_csv(post_metadata_file)

# MAIN LOOP

# GET THE COMMENTS
print "Getting comments..."
comments_by_author = get_comment_text(comments)

# GET THE POSTS
print "Getting posts..."
author_id_mappings = {}
author_texts = {}
id_counter = 1
author_counter = 0
for author in author_metadata['author ID']:
    id_counter = make_author_id(author,author_id_mappings,id_counter) # make the author ID
    posttext = get_post_text(author,post_metadata,postdir)
    commenttext = ""
    if author in comments_by_author:
        commenttext = comments_by_author[author]
    author_texts[author] = posttext #+ commenttext
    author_counter += 1
    stdout.write("\t%d of %d authors processed...\r" %(author_counter, len(author_metadata)))
    stdout.flush()
    
# PRINT THE RESULTS
print "Printing results and mapping file..."
for author, text in author_texts.iteritems():
    filename = outdir + author_id_mappings[author] + ".txt"
    outfile = open(filename,'w')
    outfile.write(text)
    outfile.close()

mappingfile = open("authormappings.csv",'w')    
for author, author_id in author_id_mappings.iteritems():
    mappingfile.write("%s,%s\n" %(author,author_id))
    
print "Done!"
