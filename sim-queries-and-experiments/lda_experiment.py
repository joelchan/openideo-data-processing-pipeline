import time
from gensim import corpora, models, similarities

starttime = time.clock()

"""
Get the documents
"""
documents = []
infile = open("alldocs.txt")
for line in infile:
    temp = line.decode("utf-8") #convert from utf-8 to unicode
    text = temp.encode("ascii", "ignore") #convert from unicode to plain ascii (strip out chars/formats we can't represent)
    documents.append(text.strip()) #make sure we don't have leading/trailing whitespaces

"""
Convert documents to arrays of words, removing infrequent words
"""    
wordcounts = {} #to keep track of the counts of each word
texts = []
for document in documents:
    docarr = []
    for word in document.split():
        docarr.append(word)
        if word in wordcounts:
            wordcounts[word] += 1
        else:
            wordcounts[word] = 1
    texts.append(docarr)
    
# remove infrequent words
frequencyThreshold = 1 #change this to what you want
texts = [[word for word in text if wordcounts[word] > 1] for text in texts]

# remove additional stopwords
stopwords = open("englishstopwords-mallet.txt").read().split()
texts = [[word for word in text if word not in stopwords] for text in texts]

"""
Convert documents to tf-idf vectors
"""

# prepare dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents to a corpus of vectors
corpus = [dictionary.doc2bow(text) for text in texts]

"""
****************************************************************************************************
*    LDA experiment.                                                                               
*    Has 2 parts:                                                                                  
*    1) Initialize space                                                                           
*    2) Similarity queries                                                                      
*    Output is list of cosines for a set of inspirations vs the challenge brief
****************************************************************************************************
"""

topicsettings = [200,300,400,500,600,700]
#topicsettings = [100]
numrefdocs = 199
master_LDA_cosines = []
for topicsetting in topicsettings:
    """
    Transform bag of words corpus to LSA space
    """
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topicsetting) #create the space
    
    """
    ******************************************************************
    TODO: Save the model for future reference so we can just load it
    ******************************************************************
    """
    
    print "This run of LDA has k = %i." %topicsetting
    print "And these are the top 12 topics:"
    lda.print_topics(12)
    print "\n\n"
    
    """
    Prepare the reference documents (i.e., the inspirations)
    """
    # get slice from corpus and convert to vectorized corpus
    startindex = 1112
    stopindex = 1310
    refcorpus_texts = texts[startindex:stopindex+1] 
    refcorpus = [dictionary.doc2bow(text) for text in refcorpus_texts]
        
    #fold into LSA space and index it for querying
    index = similarities.MatrixSimilarity(lda[refcorpus])

    """
    Prepare the query (i.e., the challenge brief)
    """
    # get slice from corpus 
    queryindex = 1006
    query_texts = texts[queryindex] 
    query_text = ""
    for t in query_texts:
        query_text = query_text + t + " "
    query_bow = dictionary.doc2bow(query_text.split())
    
    # fold into LDA space
    query_lda = lda[query_bow]
    
    """
    Make query and add to internal correl list
    """
    results = index[query_lda]
    internal_cosines = []
    for cosine in results:
        internal_cosines.append(cosine)
    master_LDA_cosines.append(internal_cosines)

"""
Print out LDA experiment results to file
"""
ldaresults = open("results_lda.txt","w")
for i in xrange(0,numrefdocs):
    for cosine in master_LDA_cosines:
        ldaresults.write(str(cosine[i]) + "\t")
    ldaresults.write("\n")

elapsed = (time.clock() - starttime)
print "Finished! Elapsed time: %.2f." %elapsed