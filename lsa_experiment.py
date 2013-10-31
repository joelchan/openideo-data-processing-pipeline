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

"""
Convert documents to tf-idf vectors
"""

# prepare dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents to a corpus of vectors
corpus = [dictionary.doc2bow(text) for text in texts]

# convert raw vectors to tfidf vectors
tfidf = models.TfidfModel(corpus) #initialize model
corpus_tfidf = tfidf[corpus] #apply tfidf model to whole corpus
    
"""
****************************************************************************************************
*    LSA experiment.                                                                               
*    Has 2 parts:                                                                                  
*    1) Initialize space                                                                           
*    2) Similarity queries                                                                      
*    Output is list of cosines for a set of inspirations vs the challenge brief
****************************************************************************************************
"""
#dims = [100,200,300,400,500,600,700,800]
#dims = [50,100,150]
dims = [1,2,3,4,6,8,10,12,14,16,18,20,22,24,26,28]
#dims = [300]
master_cosines = []
numrefdocs = 199
for dim in dims:
    """
    Transform tfidf corpus to LSA space
    """
    lsi = models.LsiModel(corpus_tfidf, id2word = dictionary, num_topics=dim) #create the space
    
    """
    Prepare the reference documents (i.e., the inspirations)
    """
    # get slice from corpus and convert to vectorized corpus
    startindex = 1112
    stopindex = 1310
    refcorpus_texts = texts[startindex:stopindex+1] 
    refcorpus = [dictionary.doc2bow(text) for text in refcorpus_texts]
        
    #fold into LSA space and index it for querying
    index = similarities.MatrixSimilarity(lsi[refcorpus])

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
    
    # fold into LSA space
    query_lsa = lsi[query_bow]
    
    """
    Make query and add to internal correl list
    """
    results = index[query_lsa]
    internal_cosines = []
    for cosine in results:
        internal_cosines.append(cosine)
    master_cosines.append(internal_cosines)

"""
Print out LSA experiment results to file
"""
lsaresults = open("results_lsa.txt","w")
for i in xrange(0,numrefdocs):
    for cosine in master_cosines:
        lsaresults.write(str(cosine[i]) + "\t")
    lsaresults.write("\n")

elapsed = (time.clock() - starttime)
print "Finished! Elapsed time: %.2f." %elapsed