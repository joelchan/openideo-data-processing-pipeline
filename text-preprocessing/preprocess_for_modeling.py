
#! /usr/bin/python

# usage: python preprocess_for_modeling.py <location> <source-directory> <output-format> <CFt> <Dft>
# output-format is either ctm or mallet
# CFt is corpus frequency threshold (we want to keep only tokens that appear more than CFt times in the corpus)
# DFt is document frequency threshold (we want to keep only tokens that appear at least once in more than DFt documents)
# example: python preprocess_for_modeling.py joelc TokenizedText/ ctm 1 50

from sys import argv
import os
import nltk

script, location, source_dir, outputformat, CFt, DFt = argv  

"""
Get the data
"""
dir = "/Users/%s/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/%s" %(location, source_dir)
masterdocnames = []
documents = []
for filename in os.listdir(dir):
    if ".txt" in filename: #don't process the "ghost files"
        docfilename = dir + filename
        docfile = open(docfilename)
        decodedtext = docfile.read().decode("utf-8","ignore")
        encodedtext = decodedtext.encode("ascii","ignore")
        documents.append(encodedtext)
        masterdocnames.append(str(filename))

"""
Get corpus-level word counts (i.e., how many times was word w used in the whole corpus?)
and corpus-level word-in-document frequencies (i.e., in how many docs did word w occur at least once?)
"""

print "Getting word counts..."
wordcounts = {}
worddoccounts = {}
for document in documents:
    docwords = [] #doc word history
    for word in document.split():
        decoded_word = word.decode("utf-8","ignore")
        encoded_word = decoded_word.encode("ascii","ignore")
        if encoded_word in wordcounts: #process word counts
            wordcounts[encoded_word] += 1
        else:
            wordcounts[encoded_word] = 1
        if encoded_word not in docwords: #process word-doc frequencies; if we've seen this word in the doc already, skip it
            if encoded_word in worddoccounts: 
                worddoccounts[encoded_word] += 1
            else:
                worddoccounts[encoded_word] = 1
        docwords.append(encoded_word) #store this word in the doc word history
#print wordcounts

"""
Build feature space, screening out low frequency words and extra stopwords
Outputs of this step are:
1) A new list of documents, with each element being a string that holds all the screened tokens for a given doc
2) A master list of tokens encountered in the 
"""

print "Building feature space, screening out low frequency words and extra stopwords..."
extrastopwords = [word.strip() for word in open("englishstopwords-mallet.txt").readlines()]
masterWordList = []
screenedDocuments = []
corpfreq_threshold = int(CFt)
docfreq_threshold = int(DFt)
numwords = 0
for i in xrange(len(documents)):
    
    # screen out low frequency words and extra stopwords
    docwords = []
    for word in documents[i].split():
        decoded_word = word.decode("utf-8","ignore")
        encoded_word = decoded_word.encode("ascii","ignore")
        if wordcounts[encoded_word] > corpfreq_threshold and worddoccounts[encoded_word] > docfreq_threshold and encoded_word not in extrastopwords:
            docwords.append(encoded_word)
            numwords += 1
            if encoded_word not in masterWordList:
                masterWordList.append(encoded_word)
    
    # write the "screened" doc text
    doctext = ""
    for word in docwords:
        doctext = doctext + word + " "
    screenedDocuments.append(doctext)
    #print doctext

"""
write master vocabulary list to file
"""
print "Writing master vocabulary list to file..."
vocabfilename = "/Users/%s/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/SemanticModelData/%s/inputs/vocab_CF-%i_DF-%i.dat" %(location, outputformat, corpfreq_threshold, docfreq_threshold)
vocabfile = open(vocabfilename, 'w')
for i in xrange(0,len(masterWordList)):
	if i+1 == len(masterWordList): # if we are at the last word
		vocabfile.write(masterWordList[i])
	else:
		vocabfile.write(masterWordList[i] + "\n")
vocabfile.close()
print "%i total words, %i unique tokens" %(numwords, len(masterWordList))
    
"""
create file that lists each doc as sparse vector of token counts on new line;
do not list vocabulary terms that don't show up in the doc, 
so each line has a different number of parameters. THIS IS THE CORRECT FORMAT.
"""

print "Making master doc file..."
resultsfilename = "/Users/%s/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/SemanticModelData/%s/inputs/alldocs_CF-%i_DF-%i_%sformat.txt" %(location, outputformat, corpfreq_threshold, docfreq_threshold, outputformat)

if outputformat == "ctm":	
	
	results = open(resultsfilename,'w')
	
	for document in screenedDocuments:
		
		# get the doc's data
		tokens = document.split() 
		
		# get the token list and token counts for this doc
		doctoken_hash = {} #stores token counts
		docTokens = [] #list of tokens
		for token in tokens: 
			if token not in docTokens: # we haven't seen it
				docTokens.append(token) # add the token to our list of unique tokens in the doc
				doctoken_hash[token] = 1 # create an entry in the token count hash
			else:
				doctoken_hash[token] = doctoken_hash[token]+1 # don't add the token to our list of unique tokens, but increment its count
	
		# print the results to the results file
		results.write(str(len(docTokens)) + " ") # number of unique tokens in docs ***OK***
		for token in docTokens:
			if not(token == docTokens[len(docTokens)-1]): # if we aren't at the last token in the doc
				results.write(str(masterWordList.index(token)) + ":" + str(doctoken_hash[token]) + " ")
			else:
				results.write(str(masterWordList.index(token)) + ":" + str(doctoken_hash[token]))
		if document != screenedDocuments[-1]: # if we aren't processing the last doc
			results.write("\n")
	results.close()
	print "Finished!"
	
elif outputformat == "mallet":
	
	results = open(resultsfilename,'w')
	
	for document in screenedDocuments:
		
		# get the doc's data
		tokens = document.split()
		
		documentname = masterdocnames[screenedDocuments.index(document)]
		towrite = "%s %s " %(documentname, documentname)
		for token in tokens:
			towrite = towrite + token + " "
		towrite = towrite.strip()
		results.write(towrite)
		if document != screenedDocuments[-1]: # if we aren't processing the last doc
			results.write("\n")
			
else:
	
	print "Don't recognize that format!"
	