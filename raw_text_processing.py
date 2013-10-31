from nltk.tokenize import TreebankWordTokenizer
import sys
import os

def remove_stop_words(words, stopwords):
	newwords = []
	for word in words:
		if not(word in stopwords):
			newwords.append(word)
	return newwords
	
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
	#newwords = []
	#for word in words:
	#	if word[-1] == '.' or word[-1] == '?' or word[-1] == '!':
	#		newwords.append(word[:-1])
	#	else:
	#		newwords.append(word)
	#return newwords

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

def tokenize_raw_text(infilename,outfilename):

    #infile = open("/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Data/TextDescriptions/social-business/screened/social-business_screened_C-bring-the-festival-de-teatro-de-manizales-to-rural-caldas.txt")
    infile = open(infilename)
    outfile = open(outfilename,'w')
    
    # get the stopwords (this is the list that nltk uses)
    stopwords = read_data("englishstopwords-jc")

    # read in the doc as one long string
    temp = infile.read().decode("utf-8", "ignore") #first convert from utf-8 to unicode
    rawtext = temp.encode("utf-8", "ignore") #then convert from unicode to to utf-8
    
    # remove the weird formatting text
    #formattingtext = open('formattingtext.txt').read().split('\n')
    #for text in formattingtext:
    #    rawtext = rawtext.replace(text,' ')
    #rawtext = rawtext.encode('utf8')

    ## define a regex pattern to tokenize
    #pattern = r'''(?x) 			# set flag to allow verbose regexps
    #        ([A-Z]\.)+ 			# abbreviations, e.g., U.S.A.
    #        | \w+(-\w+)* 		# words with optional internal hyphens
    #        | \$?\d+(\.\d+)?%?	# currency and percentages, e.g., $12.40, 82%
    #        | \.\.\.			# ellipsis
    #        | [][.,;"'?():-_`]	# these are separate tokens
    #        '''

    # tokenize the long string, remove stopwords, then do some stemming of tokens (haven't decided how to stem yet)
    #tokens = nltk.regexp_tokenize(rawtext, pattern)
    tokens = TreebankWordTokenizer().tokenize(rawtext)
    #wnl = nltk.WordNetLemmatizer()
    #tokens = [wnl.lemmatize(t) for t in tokens]
    #porter = nltk.PorterStemmer()
    #tokens = [porter.stem(t) for t in tokens]
    tokens = remove_urls(tokens)
    tokens = remove_punctuation_only(tokens)
    tokens = remove_trailing_punctuation(tokens)
    tokens = remove_leading_punctuation(tokens)
    tokens = split_slashes_and_periods(tokens)
    tokens = remove_stop_words(tokens, stopwords)
    # print tokens to outfile

    text = ""
    for t in tokens:
        t = t.lower()
        text = text + t + " "
        outfile.write(t + " ")
    outfile.close()

    return text
    
"""
tokenize all docs and send to new folder
"""
raw_dir = "renamedrawtextdescriptionfiles/"
tokenized_dir = "renamedtokenizeddocs/"
#masterdocfile = open("alldocs.txt",'w')
#masterdoclist = open("masterdoclist.txt",'w')
for filename in os.listdir(raw_dir):
	raw_docfilename = raw_dir + filename
	tokenized_docfilename = tokenized_dir + "tokenized_" + filename
	text = tokenize_raw_text(raw_docfilename,tokenized_docfilename)
	#masterdocfile.write(text + "\n")
	#print text
	#masterdoclist.write(str(filename) + "\n")
#masterdocfile.close()
#masterdoclist.close()
