import wordcloud, sys, csv
import pandas as pd

def get_doctopic_weights(weightsfilename):
    """
    read in the doc-topic weights
    this is different from the "usual" in that it returns a dict of docnames
    associated with lists of topic-weight tuples (vs just a list of weights)
    """
    #print "Reading in weights..."
    weights = {}
    with open(weightsfilename, 'rU') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in filereader:
            if 'doc' not in row[0]: #skip the header
                docname = row[0].replace("tokenized_","").replace(".txt","")
                weightsList = []
                for i in xrange(1,len(row)):
                    weightsList.append((float(row[i]),i-1)) #append tuple: weight, topic (-1 for topic so that it aligns with index in real topics)
                weights[docname] = weightsList
    csvfile.close
    return weights

def get_paths(pathfilename,levels):
    """
    read in the paths, create data for seed type so we can select later (for the set);
    may want to add source type later if we want to grab diversity only for inspirations
    """
    #print "Reading in paths..."
    df = pd.read_csv(pathfilename)
    df = df[df['level'].isin(levels)] # trim to only desired levels in genealogy
    df['seedtype'] = [n.split('_')[1] for n in df.seed_ID] #create seed type
    df['seedtype'] = [n[0] for n in df.seedtype]
    df['challenge'] = [n.split('_')[0] for n in df.seed_ID]
    return df

def get_top_topics(sourceList,docTopicWeights,threshold):
    topTopics = [] 
    for source in sourceList:
        # get the weights, sort in place in descending order by the weights (first element in tuples)
        weights = docTopicWeights[source]
        weights.sort(key=lambda tup: tup[0], reverse=True) #
        # get the top N weights whose sum > threshold
        weightSum = 0.0
        i = 0
        while weightSum <= threshold:
            topTopics.append(weights[i][1])
            weightSum += weights[i][0]
            i += 1     
    return topTopics, weightSum

#conceptFile = sys.argv[1]
#keysFile = sys.argv[2]
keysFile = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/CF0_DF0_400_ASP_optim_keys-6.txt"
weightsFile = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/sorted_CF0_DF0_400_ASP_optim_composition-6.csv"
pathFile = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Paths/_CSVversions/paths_all.csv"
fontPath = "/Library/Fonts/Microsoft/Andale Mono"
levelRange = "1-1"
fromLevel = int(levelRange.split('-')[0])
toLevel = int(levelRange.split('-')[1])
levels = [i for i in xrange(fromLevel,toLevel+1)] #create list of levels, inclusive of the upper limit (toLevel)
weightThreshold = 0.50
#numTopWords = int(sys.argv[2])

# get weights
docWeights = get_doctopic_weights(weightsFile)

# get sources
source_df = get_paths(pathFile,levels)
sources = set()
sources.update(source_df.source_ID)

# grab topic-keys -> hash: key = topic, value = list of words
topicKeys = {}
with open(keysFile,'rU') as csvFile:
    fileReader = csv.reader(csvFile, delimiter='\t', quotechar='|')
    for row in fileReader:
        topicKeys[int(row[0])] = row[2].split(' ')

# main work        
for source in sources:
    print "Processing %s..." %source
    topics, weightSum = get_top_topics([source],docWeights,weightThreshold)
    text = ""
    for topic in topics:
        t = " ".join(topicKeys[topic]) + " "
        text += t
    
    words = wordcloud.process_text(text)
    elements = wordcloud.fit_words(words,font_path=fontPath)
    outpath = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/wordclouds/k400t50/%s.png" %source
    wordcloud.draw(elements, outpath, font_path=fontPath)

## read in the concept list
#concepts = {}
#with open(conceptFile, 'rU') as csvfile:
#    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
#    for row in filereader:
#        concepts[row[0]] = row[1]
#
## grab topic-keys -> hash: key = topic, value = list of words
#topicKeys = {}
#with open(keysFile,'rU') as csvFile:
#    fileReader = csv.reader(csvFile, delimiter='\t', quotechar='|')
#    for row in fileReader:
#        topicKeys[row[0]] = row[2].split(' ')
#        
#for concept in sorted(concepts.keys()):
#    print "Processing %s..." %concept
#    topics = concepts[concept].split("_")
#    text = ""
#    for topic in topics:
#        t = " ".join(topicKeys[topic]) + " "
#        text += t
#    
#    words = wordcloud.process_text(text)
#    elements = wordcloud.fit_words(words)
#    outpath = "/Users/joelc/Desktop/wordclouds/bothk200t50/%s.png" %concept
#    wordcloud.draw(elements, outpath)