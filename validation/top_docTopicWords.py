import csv, sys

numTopTopics = int(sys.argv[1])
numTopWords = int(sys.argv[2])

TOPICINDEXSTART = 2

docCompFile = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/CF0_DF0_400_ASP_optim_composition-6_formatted.txt"
keysFile = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/CF0_DF0_400_ASP_optim_keys-6.txt"
namesFile = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/KT_Structuring/labels.csv"

# read in labels
docNames = []
with open(namesFile,'rU') as csvFile:
    fileReader = csv.reader(csvFile, delimiter='\t', quotechar='|')
    docNames = [row[0] for row in fileReader]

# get the doc-topic compositions
docComps = {}
with open(docCompFile,'rU') as csvFile:
    fileReader = csv.reader(csvFile, delimiter='\t', quotechar='|')
    for row in fileReader:
        docName = row[1]
        docTopNTopics = row[TOPICINDEXSTART:(numTopTopics*TOPICINDEXSTART)+TOPICINDEXSTART]
        docComps[docName] = docTopNTopics
csvFile.close()

# grab topic-keys -> hash: key = topic, value = list of words
topicKeys = {}
with open(keysFile,'rU') as csvFile:
    fileReader = csv.reader(csvFile, delimiter='\t', quotechar='|')
    for row in fileReader:
        topicKeys[row[0]] = row[2].split(' ')
        
# main stuff here
indices = [i*2 for i in xrange(numTopTopics)]
outFileName = "newNames_%i-%i.csv" %(numTopTopics,numTopWords)
outFile = open(outFileName,'w')
for docName in docNames:
    newName = ""
    for index in indices:
        topicName = docComps[docName][index] # grab the topic name
        topicWords = topicKeys[topicName][:numTopWords] # grab the topic words
        # append the top N words from the topic onto newName
        for word in topicWords:
            #newName += word.title() # make the first letter uppercase so we have readable camelCase
            newName = newName + word + " " 
    outFile.write("%s,%s\n" %(docName,newName))
outFile.close()

# create set of unique topics
# sum the weights for each of the topics
# sort in reverse order of summed weight
# print out the top N