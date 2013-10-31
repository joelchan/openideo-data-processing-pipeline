
import os
import nltk

"""
Get the data
"""
dir = "tokenizeddocs/"
masterdoclist = open("masterdoclist.txt",'w')
masterdocnames = []
documents = []
for filename in os.listdir(dir):
    docfilename = dir + filename
    docfile = open(docfilename)
    decodedtext = docfile.read().decode("utf-8","ignore")
    encodedtext = decodedtext.encode("ascii","ignore")
    documents.append(encodedtext)
    masterdoclist.write(str(filename) + "\n")
    masterdocnames.append(str(filename))
masterdoclist.close()

"""
Get corpus-level word counts (i.e., how many times was word w used in the whole corpus?)
and corpus-level word-in-document frequencies (i.e., in how many docs did word w occur at least once?)
"""
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

"""
Make the results file, screening out low frequency words
"""
masterdocfile = open("alldocs_CFgt1_DFgt50_stemmed_malletformat.txt",'w')
extrastopwords = [word.strip() for word in open("englishstopwords-mallet.txt").readlines()]
print extrastopwords
corpfreq_threshold = 1 # change these to suit your fancy
docfreq_threshold = 50
for i in xrange(len(documents)):
    doctext = ""
    docwords = []
    for word in documents[i].split():
        decoded_word = word.decode("utf-8","ignore")
        encoded_word = decoded_word.encode("ascii","ignore")
        if wordcounts[encoded_word] > corpfreq_threshold and worddoccounts[encoded_word] > docfreq_threshold and encoded_word not in extrastopwords:
            docwords.append(encoded_word)
            
    porter = nltk.PorterStemmer()
    docwords = [porter.stem(word) for word in docwords]
    for word in docwords:
        doctext = doctext + word + " "
        
    label = masterdocnames[i]
    #truncatedname = label[:17] + "..." + str(i)
    towrite = "%s %s %s\n" %(label, label, doctext)
    masterdocfile.write(towrite)
masterdocfile.close()