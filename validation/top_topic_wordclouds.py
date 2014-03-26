import wordcloud, sys, csv

conceptFile = sys.argv[1]
#keysFile = sys.argv[2]
keysFile = "/Users/joelc/Desktop/Desktop_from_Joels_old_iMac/LDA_CF0_DF0_ASP_opt0/RawOutputs/CF0_DF0_200_ASP_optim_keys-20.txt"
#numTopWords = int(sys.argv[2])

# read in the concept list
concepts = {}
with open(conceptFile, 'rU') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        concepts[row[0]] = row[1]

# grab topic-keys -> hash: key = topic, value = list of words
topicKeys = {}
with open(keysFile,'rU') as csvFile:
    fileReader = csv.reader(csvFile, delimiter='\t', quotechar='|')
    for row in fileReader:
        topicKeys[row[0]] = row[2].split(' ')
        
for concept in sorted(concepts.keys()):
    print "Processing %s..." %concept
    topics = concepts[concept].split("_")
    text = ""
    for topic in topics:
        t = " ".join(topicKeys[topic]) + " "
        text += t
    
    words = wordcloud.process_text(text)
    elements = wordcloud.fit_words(words)
    outpath = "/Users/joelc/Desktop/wordclouds/bothk200t50/%s.png" %concept
    wordcloud.draw(elements, outpath)