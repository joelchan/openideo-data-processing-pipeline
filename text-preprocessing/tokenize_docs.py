#! /usr/bin/python

# usage: python tokenize_docs.py <source-directory> <destination-directory>
# example: python tokenize_docs.py RawTextDescriptions/ TokenizedText/ 

from nltk.tokenize import TreebankWordTokenizer
import sys
import os
	
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

    infile = open(infilename)
    outfile = open(outfilename,'w')

    # read in the doc as one long string
    temp = infile.read().decode("utf-8", "ignore") #first convert from utf-8 to unicode
    rawtext = temp.encode("utf-8", "ignore") #then convert from unicode to to utf-8

    # tokenize the long string, remove stopwords,
    # then do some other work to remove urls, punctuation only, other weird stuff
    tokens = TreebankWordTokenizer().tokenize(rawtext)
    tokens = remove_urls(tokens)
    tokens = remove_punctuation_only(tokens)
    tokens = remove_trailing_punctuation(tokens)
    tokens = remove_leading_punctuation(tokens)
    tokens = split_slashes_and_periods(tokens)
    
    # print tokens to outfile
    text = ""
    for t in tokens:
        t = t.lower()
        text = text + t + " "
        outfile.write(t + " ")
    outfile.close()

    return len(tokens)
    
if (__name__ == '__main__'):
    
    # get the source and destination directory arguments
    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    
    # iterate over the docs in the raw directory and
    # send the tokenized versions to the destination directory
    numDocs = 0
    totalTokens = 0
    for filename in os.listdir(source_dir):
        
        # create the source and dest file name
        raw_docfilename = source_dir + filename # create the source and dest file name
        tokenized_docfilename = dest_dir + "tokenized_" + filename
        
        # TOKENIZE THE DOCUMENT
        docTokens = tokenize_raw_text(raw_docfilename,tokenized_docfilename)
        
        # compute info for potential debugging - we want to know how many tokens we have at this step!
        totalTokens += docTokens
        numDocs += 1
    
    print "Finished! Corpus has %i documents with %i tokens" %(numDocs, totalTokens)
