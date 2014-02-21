import numpy as np
import pandas as pd
import itertools as it
import csv

def get_top_topics(sourceList,docTopicWeights,nTopics,unique=True):
    topTopics = []
    for source in sourceList:
        weights = docTopicWeights[source]
        # get the largest weighted topics
        weights.sort(key=lambda tup: tup[0], reverse=True) #sort in place in descending order by the weights (first element in tuples)
        for i in xrange(nTopics):
            if(unique):
                if weights[i][1] not in topTopics:
                    topTopics.append(weights[i][1])
            else:
                topTopics.append(weights[i][1])
    return sorted(list(topTopics)) # return it as a sorted list so it's a bit easier to work with

datafilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControls.xlsx"
pathfilename = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Paths/_CSVversions/paths_all.csv"
weightsfilename = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/sorted_CF0_DF0_400_ASP_optim_composition-6.csv"

# read in the doc-topic weights
print "Reading in weights..."
doc_topic_weights = {}
with open(weightsfilename, 'rU') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        if 'doc' not in row[0]: #skip the header
            docname = row[0].replace("tokenized_","").replace(".txt","")
            weightsList = []
            for i in xrange(1,len(row)):
                weightsList.append((float(row[i]),i-1)) #append tuple: weight, topic (-1 for topic so that it aligns with index in real topics)
            doc_topic_weights[docname] = weightsList
            #doc_topic_weights[docname] = [float(i) for i in row[1:]]
csvfile.close

# read in the paths, create data for seed type so we can select later (for the set); may want to add source type later if we want to grab diversity only for inspirations
print "Reading in paths..."
pathlevel_df = pd.read_csv(pathfilename)
pathlevel_df = pathlevel_df[pathlevel_df['level'] == 1] # trim to only immediate paths for now to reduce computation time and memory usage - this will change later when we want to compute last N sources, for example
pathlevel_df['seedtype'] = [n.split('_')[1] for n in pathlevel_df.seed_ID] #create seed type
pathlevel_df['seedtype'] = [n[0] for n in pathlevel_df.seedtype]
pathlevel_df['challenge'] = [n.split('_')[0] for n in pathlevel_df.seed_ID]

sourceList = ['bone-marrow_C-001','bone-marrow_C-002','bone-marrow_C-003']
sourceTopTopics = get_top_topics(sourceList,doc_topic_weights,5)
print sourceTopTopics
print len(sourceTopTopics)

for challengeName, challengeDF in pathlevel_df.groupby('challenge'):
    concepts = set()
    concepts.update(challengeDF[challengeDF['seedtype'] == 'C']['seed_ID'])
    challengeTopTopics = get_top_topics(challengeDF['source_ID'],doc_topic_weights,5) #get its top topics
    for concept in concepts:
        conceptSources = challengeDF[challengeDF['seed_ID'] == concept]['source_ID'] #get it sources
        conceptTopTopics = get_top_topics(conceptSources,doc_topic_weights,5,unique=False) #get its top topics