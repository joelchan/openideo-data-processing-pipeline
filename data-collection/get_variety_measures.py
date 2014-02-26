#! /usr/bin/python
#
#
# usage: python get_variety_measures.py <levelRange> <numTopTopics>
#
# where levelRange defines the range of levels (inclusive) in the genealogy you want to consider for the source distance measures
# e.g., 1-1 says only sources at level-1, 2-5 says only sources from levels 2 to 5
# and numTopTopics is the number of top topics you want to grab for each source

import numpy as np
import pandas as pd
import itertools as it
import csv, sys

#def get_top_topics(sourceList,docTopicWeights,nTopics,unique=True):
#    topTopics = []
#    for source in sourceList:
#        weights = docTopicWeights[source]
#        # get the largest weighted topics
#        weights.sort(key=lambda tup: tup[0], reverse=True) #sort in place in descending order by the weights (first element in tuples)
#        for i in xrange(nTopics):
#            if(unique):
#                if weights[i][1] not in topTopics:
#                    topTopics.append(weights[i][1])
#            else:
#                topTopics.append(weights[i][1])
#    return topTopics # return it as a sorted list so it's a bit easier to work with

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

datafilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControls.xlsx"
pathfilename = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Paths/_CSVversions/paths_all.csv"
weightsfilename = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/sorted_CF0_DF0_400_ASP_optim_composition-6.csv"
levelRange = sys.argv[1] #this command-line parameter determines range of levels to consider in the genealogy (1 = immediate)
fromLevel = int(levelRange.split('-')[0])
toLevel = int(levelRange.split('-')[1])
levels = [i for i in xrange(fromLevel,toLevel+1)] #create list of levels, inclusive of the upper limit (toLevel)

#numTopTopics = int(sys.argv[2])
weightsThreshold = float(sys.argv[2])

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
pathlevel_df = pathlevel_df[pathlevel_df['level'].isin(levels)] # trim to only desired levels in genealogy
pathlevel_df['seedtype'] = [n.split('_')[1] for n in pathlevel_df.seed_ID] #create seed type
pathlevel_df['seedtype'] = [n[0] for n in pathlevel_df.seedtype]
pathlevel_df['challenge'] = [n.split('_')[0] for n in pathlevel_df.seed_ID]

#########################
# compute variety
#########################
print "Computing variety..."
concepts = set()
concepts.update(pathlevel_df[pathlevel_df['seedtype'] == 'C']['seed_ID'])
conceptdata = []
for concept in concepts:
    conceptDict = {"nodeID":concept}
    conceptSources = pathlevel_df[pathlevel_df['seed_ID'] == concept]['source_ID'] #get its sources
    conceptTopTopics, conceptWeightSum = get_top_topics(conceptSources,doc_topic_weights,weightsThreshold) #get its top topics
    uniqueConceptTopTopics = set()
    uniqueConceptTopTopics.update(conceptTopTopics)
    sumVar = 0
    for topic in uniqueConceptTopTopics:
        pTopic = conceptTopTopics.count(topic)/float(len(conceptTopTopics))
        sumVar += pTopic*np.log(pTopic)
    conceptDict['sourceVariety'] = -1*sumVar
    conceptDict['topTopics'] = '-'.join([str(t) for t in conceptTopTopics]) #list of top topics
    conceptDict['numTopTopics'] = len(conceptTopTopics)
    conceptDict['weightSum'] = conceptWeightSum
    conceptDict['numSources'] = len(conceptSources)
    conceptDict['challenge'] = concept.split('_')[0]
    conceptdata.append(conceptDict)
conceptDF = pd.DataFrame(conceptdata)
conceptDF.to_csv("test_%s.csv" %sys.argv[2].split('.')[1])

#for challengeName, challengeDF in pathlevel_df.groupby('challenge'):
#    concepts = set()
#    concepts.update(challengeDF[challengeDF['seedtype'] == 'C']['seed_ID'])
#    challengeTopTopics = get_top_topics(challengeDF['source_ID'],doc_topic_weights,numTopTopics) #get its top topics
#    #print challengeName
#    #print "\tnumConcepts: %i\tnumTopTopics: %i\tnumPossibleTopics: %i\tpropPossibleTopics: %.2f" %(len(concepts), len(challengeTopTopics), len(concepts)*5, len(challengeTopTopics)/float(len(concepts)*5))
#    for concept in concepts:
#        conceptDict = {"nodeID":concept}
#        conceptSources = challengeDF[challengeDF['seed_ID'] == concept]['source_ID'] #get its sources
#        conceptTopTopics = get_top_topics(conceptSources,doc_topic_weights,5,unique=False) #get its top topics
#        sumVar = 0
#        for topic in challengeTopTopics:
#            pTopic = conceptTopTopics.count(topic)/float(len(conceptTopTopics))
#            if pTopic > 0:
#                sumVar += pTopic*np.log(pTopic)
#        conceptDict['sourceVariety'] = -1*sumVar
#        conceptDict['topTopics'] = '-'.join([str(t) for t in conceptTopTopics]) #list of top topics
#        conceptDict['numTopTopics'] = len(conceptTopTopics)
#        conceptDict['numSources'] = len(conceptSources)
#        conceptDict['challenge'] = challengeName
#        conceptdata.append(conceptDict)