
import os
import nltk

"""
Get the data
"""
dir = "/Users/joelc/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/TokenizedText/"
masterdoclist = open("masterdoclist.txt",'w')
masterdocnames = []
documents = []
for filename in os.listdir(dir):
    if ".txt" in filename: #don't process the "ghost files"
        docfilename = dir + filename
        docfile = open(docfilename)
        decodedtext = docfile.read().decode("utf-8","ignore")
        encodedtext = decodedtext.encode("ascii","ignore")
        documents.append(encodedtext)
        masterdoclist.write(str(filename) + "\n")
        masterdocnames.append(str(filename))
masterdoclist.close()
#print documents

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
corpfreq_threshold = 1 # change these to suit your fancy
docfreq_threshold = 50
masterWordList = []
screenedDocuments = []
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
vocabfile = open("ctm-dist/vocab.dat", 'w')
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
results = open("alldocs_CFgt1_DFgt50_CTMformat.txt",'w')
for document in screenedDocuments:
    
    # get the doc's data
    #print document
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
    index = 0 #this helps us keep our place in the MASTER token list
    for token in docTokens:
        if not(token == docTokens[len(docTokens)-1]): # if we aren't at the last token in the doc
            results.write(str(masterWordList.index(token)) + ":" + str(doctoken_hash[token]) + " ")
        else:
            results.write(str(masterWordList.index(token)) + ":" + str(doctoken_hash[token]))
    if document != screenedDocuments[-1]: # if we aren't processing the last doc
        results.write("\n")
results.close()
print "Finished!"