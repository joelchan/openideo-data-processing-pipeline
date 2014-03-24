#! /usr/bin/python
#
#
# usage: python get_variety_measures.py <levelRange> <weightsThreshold>
#
# where levelRange defines the range of levels (inclusive) in the genealogy you want to consider 
# e.g., 1-1 says only sources at level-1, 2-5 says only sources from levels 2 to 5
# and weightsThreshold is the threshold of topic weight mass we want the top topics to collectively cover
# e.g., 0.50 will grab all top topics until their cumulative probability mass exceeds 0.50

import numpy as np
import pandas as pd
import csv, sys

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

def compute_variety(topTopics):
    uniqueTopTopics = set()
    uniqueTopTopics.update(topTopics)
    sumVar = 0
    for topic in uniqueTopTopics:
        pTopic = topTopics.count(topic)/float(len(topTopics))
        sumVar += pTopic*np.log(pTopic)
    return -1*sumVar

def count_unique_items(a):
    unique_a = set()
    unique_a.update(a)
    return len(unique_a)

datafilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControlsAndDiversity.csv"
pathfilename = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Paths/_CSVversions/paths_all.csv"
weightsfilename = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/sorted_CF0_DF0_400_ASP_optim_composition-6.csv"
levelRange = sys.argv[1] #this command-line parameter determines range of levels to consider in the genealogy (1 = immediate)
fromLevel = int(levelRange.split('-')[0])
toLevel = int(levelRange.split('-')[1])
levels = [i for i in xrange(fromLevel,toLevel+1)] #create list of levels, inclusive of the upper limit (toLevel)

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
    
    conceptDict = {"nodeID":concept, 'challenge':concept.split('_')[0]}
    conceptSources_both = pathlevel_df[pathlevel_df['seed_ID'] == concept]['source_ID'] #get all its sources
    conceptSources_conc = [s for s in conceptSources_both if "_C-" in s] # grab concept sources
    conceptSources_insp = [s for s in conceptSources_both if "_I-" in s] # grab inspiration sources
    
    # both
    both_conceptTopTopics, both_conceptWeightSum = get_top_topics(conceptSources_both,doc_topic_weights,weightsThreshold) #get its top topics
    conceptDict['both_sourceVariety'] = compute_variety(both_conceptTopTopics)
    conceptDict['both_topTopics'] = '-'.join([str(t) for t in both_conceptTopTopics]) #list of top topics
    conceptDict['both_numTopTopics'] = len(both_conceptTopTopics)
    conceptDict['both_weightSum'] = both_conceptWeightSum
    conceptDict['both_numSources'] = count_unique_items(conceptSources_both)
    
    # concepts
    conceptDict['conc_numSources'] = len(conceptSources_conc)
    if len(conceptSources_conc) > 0:
        conc_conceptTopTopics, conc_conceptWeightSum = get_top_topics(conceptSources_conc,doc_topic_weights,weightsThreshold) #get its top topics
        conceptDict['conc_sourceVariety'] = compute_variety(conc_conceptTopTopics)
        conceptDict['conc_topTopics'] = '-'.join([str(t) for t in conc_conceptTopTopics]) #list of top topics
        conceptDict['conc_numTopTopics'] = count_unique_items(conc_conceptTopTopics)
        conceptDict['conc_weightSum'] = conc_conceptWeightSum
    else:
        conceptDict['conc_sourceVariety'] = np.nan
        conceptDict['conc_topTopics'] = np.nan
        conceptDict['conc_numTopTopics'] = np.nan
        conceptDict['conc_weightSum'] = np.nan
    
    # inspirations
    conceptDict['insp_numSources'] = len(conceptSources_insp)
    if len(conceptSources_insp) > 0:
        insp_conceptTopTopics, insp_conceptWeightSum = get_top_topics(conceptSources_insp,doc_topic_weights,weightsThreshold) #get its top topics
        conceptDict['insp_sourceVariety'] = compute_variety(insp_conceptTopTopics)
        conceptDict['insp_topTopics'] = '-'.join([str(t) for t in insp_conceptTopTopics]) #list of top topics
        conceptDict['insp_numTopTopics'] = count_unique_items(insp_conceptTopTopics)
        conceptDict['insp_weightSum'] = insp_conceptWeightSum
    else:
        conceptDict['insp_sourceVariety'] = np.nan
        conceptDict['insp_topTopics'] = np.nan
        conceptDict['insp_numTopTopics'] = np.nan
        conceptDict['insp_weightSum'] = np.nan
    
    conceptdata.append(conceptDict)

print "Cleaning up..."
conceptVarDF = pd.DataFrame(conceptdata)
data = pd.read_csv(datafilename) #open the data file
masterDF = pd.merge(data,conceptVarDF,how='left') #merge into the master datafile
masterDF.to_csv("ConceptLevel_AfterDistanceAndControlsAndDiversityAndVariety_1-1_Var%s.csv" %sys.argv[2].split('.')[1])