#! /usr/bin/python
#
#
# this code searches through the combination space of k, run number, and weightthreshold to explore robustness of our quadratic variety effect
# it produces C datafiles, where C is the number of combinations of k, run number, and weightthreshold
#
# usage: python search_variety_space.py <weightsDir> <outputDir>
#
# where weightsDir defines a directory that contains the weightsfiles to be processed
# and outputDir is the directory into which we want to output the datafiles

import numpy as np
import pandas as pd
import csv, sys, os

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

def compute_variety(pathDF,docTopicWeights,threshold):
    #print "Computing variety..."
    conceptSet = set()
    conceptSet.update(pathDF[pathDF['seedtype'] == 'C']['seed_ID'])
    concepts = sorted(list(conceptSet))
    
    conceptdata = []
    
    print len(concepts)
    print concepts[:15]
    for i in xrange(len(concepts)):
        
        print "Hello!"
        conceptDict = {"nodeID":concepts[i], 'challenge':concepts[i].split('_')[0]}
        conceptSources_both = pathDF[pathDF['seed_ID'] == concepts[i]]['source_ID'] #get all its sources
        conceptSources_conc = [s for s in conceptSources_both if "_C-" in s] # grab concept sources
        conceptSources_insp = [s for s in conceptSources_both if "_I-" in s] # grab inspiration sources
        
        # both
        both_TopTopics, both_WeightSum = get_top_topics(conceptSources_both,docTopicWeights,threshold) #get its top topics
        conceptDict['both_sourceVariety'] = entropy(both_TopTopics)
        conceptDict['both_topTopics'] = '_'.join([str(t) for t in both_TopTopics]) #list of top topics
        conceptDict['both_numTopTopics'] = len(both_TopTopics)
        conceptDict['both_numUniqueTopTopics'] = count_unique_items(both_TopTopics)
        conceptDict['both_weightSum'] = both_WeightSum
        conceptDict['both_numSources'] = len(conceptSources_both)
        
        # concepts
        conceptDict['conc_numSources'] = len(conceptSources_conc)
        if len(conceptSources_conc) > 0:
            conc_TopTopics, conc_WeightSum = get_top_topics(conceptSources_conc,docTopicWeights,threshold) #get its top topics
            conceptDict['conc_sourceVariety'] = entropy(conc_TopTopics)
            conceptDict['conc_topTopics'] = '_'.join([str(t) for t in conc_TopTopics]) #list of top topics
            conceptDict['conc_numTopTopics'] = len(conc_TopTopics)
            conceptDict['conc_numUniqueTopTopics'] = count_unique_items(conc_TopTopics)
            conceptDict['conc_weightSum'] = conc_WeightSum
        else:
            conceptDict['conc_sourceVariety'] = np.nan
            conceptDict['conc_topTopics'] = np.nan
            conceptDict['conc_numTopTopics'] = np.nan
            conceptDict['conc_numUniqueTopTopics'] = np.nan
            conceptDict['conc_weightSum'] = np.nan
        
        # inspirations
        conceptDict['insp_numSources'] = len(conceptSources_insp)
        if len(conceptSources_insp) > 0:
            insp_TopTopics, insp_WeightSum = get_top_topics(conceptSources_insp,docTopicWeights,threshold) #get its top topics
            conceptDict['insp_sourceVariety'] = entropy(insp_TopTopics)
            conceptDict['insp_topTopics'] = '_'.join([str(t) for t in insp_TopTopics]) #list of top topics
            conceptDict['insp_numTopTopics'] = len(insp_TopTopics)
            conceptDict['insp_numUniqueTopTopics'] = count_unique_items(insp_TopTopics)
            conceptDict['insp_weightSum'] = insp_WeightSum
        else:
            conceptDict['insp_sourceVariety'] = np.nan
            conceptDict['insp_topTopics'] = np.nan
            conceptDict['insp_numTopTopics'] = np.nan
            conceptDict['insp_numUniqueTopTopics'] = np.nan
            conceptDict['insp_weightSum'] = np.nan
        
        conceptdata.append(conceptDict)
        df = pd.DataFrame(conceptdata)
        print len(df)
        return df

def output_df(varietyDF,masterDataFilePath,outFileName):
    #print varietyDF.head()
    data = pd.read_csv(masterDataFilePath) #open the data file
    masterDF = pd.merge(data,varietyDF,how='left',on='nodeID') #merge into the master datafile
    print masterDF.head()
    masterDF.to_csv(outFileName)

### HELPER FUNCTIONS ###

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

def discrete_entropy(topTopics):
    uniqueTopTopics = set()
    uniqueTopTopics.update(topTopics)
    sumVar = 0
    for topic in uniqueTopTopics:
        pTopic = topTopics.count(topic)/float(len(topTopics))
        sumVar += pTopic*np.log(pTopic)
    return -1*sumVar

def corrected_discrete_entropy(topTopics):
    """
    Correction based on Biemann & Kearney (2010) to make different-sized groups more comparable
    Uncorrected entropy underestimates variety of smaller groups even if distributions are equally spread out
    """
    uniqueTopTopics = set()
    uniqueTopTopics.update(topTopics)
    sumVar = 0
    for topic in uniqueTopTopics:
        pTopic = topTopics.count(topic)/float(len(topTopics))
        sumVar += pTopic*np.log(pTopic)
    if len(topTopics) > 1: # handles edge case of having just 1 source and 1 top topic
        correction = len(topTopics)/(len(topTopics)-1) # N/(N-1)
    else:
        correction = 1
    return -1*sumVar*correction

def get_unique_top_topic_weights(sourceList,docTopicWeights,threshold):
    """Grabs unique top topics from a list of sources (defined by a threshold paramter)
    and returns those topics in a hash with the total weight of each topic over the
    sources as values. It also returns the total topic weight from the top topics,
    which is necessary for computing the weighted entropy measure
    
    Parameters
    ----------
    sourceList : list
        list of sources to be processed
    
    docTopicWeights : dict
        hash with documents as keys, and a list of (weight, topic) tuples as values
    
    threshold : float
        defines "how much" of a given source's topic probability mass (weight)
        we want to account for when grabbing topics
    """
    topTopics = {}
    totalWeightSum = 0.0
    for source in sourceList:
        weights = docTopicWeights[source] # get the weights for this source
        weights.sort(key=lambda tup: tup[0], reverse=True) # sort the weights so the "biggest" topics are first
        thisWeightSum = 0.0 # initialize the cumulative sum for this source
        i = 0
        while thisWeightSum <= threshold: # iterate over the topics until we pass our threshold
            currentTopic = weights[i][1]
            currentTopicWeight = weights[i][0]
            if currentTopic in topTopics: # if we've seen this topic before
                topTopics[currentTopic] += currentTopicWeight # add this weight to the weight for that topic
            else:
                topTopics[currentTopic] = currentTopicWeight # add a new entry
            thisWeightSum += currentTopicWeight # add to the cumulative sum
            i += 1
        totalWeightSum += thisWeightSum # add to the total weight sum
    return topTopics, totalWeightSum

def weighted_entropy(topTopics,totalWeight):
    """Modified Teachman's index: pk is the proportion of available topic weight
    that is contained in the kth topic
    
    Parameters
    ----------
    topTopics : dict
        hash with topics as keys and weights as values (output from get_unique_top_topic_weights)
    
    totalWeight : float
        total "available weight" from the sources
    """
    sumVar = 0.0
    for topic, weight in topTopics.items():
        pk = weight/totalWeight
        sumVar += pk*np.log(pk)
    return -1*sumVar

def count_unique_items(a):
    unique_a = set()
    unique_a.update(a)
    return len(unique_a)

if __name__ == '__main__':
    """
    
    """
    DATA_FILENAME = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControlsAndDiversity.csv"
    PATH_FILENAME = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Paths/_CSVversions/paths_all.csv"
    levelRange = "1-1"
    fromLevel = int(levelRange.split('-')[0])
    toLevel = int(levelRange.split('-')[1])
    levels = [i for i in xrange(fromLevel,toLevel+1)] #create list of levels, inclusive of the upper limit (toLevel)
    weightThresholds = [0.20,
                        0.30,
                        0.40,
                        0.50,
                        0.60,
                        0.70,
                        0.80,
                        0.90]
    weightsDir = sys.argv[1]
    outputDir = sys.argv[2]
    
    for weightsFile in os.listdir(weightsDir):
        if ".csv" in weightsFile:
            weightsPath = weightsDir + weightsFile
            for weightThreshold in weightThresholds:
                k = weightsFile.split("_")[3] #get K from weightsfilename
                run = weightsFile.split("-")[1].replace(".csv","") #get run number
                #print "Processing %s..." %weightsFile
                print "Processing k = %s, run #%s, threshold = %.2f..." %(k, run, weightThreshold)
                weights = get_doctopic_weights(weightsPath)
                path_df = get_paths(PATH_FILENAME,levels)
                #variety_df = compute_variety(path_df,weights,weightThreshold)
                conceptSet = set()
                conceptSet.update(path_df[path_df['seedtype'] == 'C']['seed_ID'])
                concepts = sorted(list(conceptSet))
                
                conceptdata = []
    
                for i in xrange(len(concepts)):
                    
                    conceptDict = {"nodeID":concepts[i], 'challenge':concepts[i].split('_')[0]}
                    conceptSources_both = path_df[path_df['seed_ID'] == concepts[i]]['source_ID'] #get all its sources
                    conceptSources_conc = [s for s in conceptSources_both if "_C-" in s] # grab concept sources
                    conceptSources_insp = [s for s in conceptSources_both if "_I-" in s] # grab inspiration sources
                    
                    # both
                    #both_TopTopics, both_WeightSum = get_unique_top_topic_weights(conceptSources_both,weights,weightThreshold) #get its top topics
                    #conceptDict['both_sourceVariety'] = weighted_entropy(both_TopTopics,both_WeightSum)
                    both_TopTopics, both_WeightSum = get_top_topics(conceptSources_both,weights,weightThreshold) #get its top topics
                    conceptDict['both_sourceVariety'] = corrected_discrete_entropy(both_TopTopics)
                    #conceptDict['both_topTopics'] = '_'.join(["%i$%.3f" %(key, value) for key, value in both_TopTopics.items()]) #list of top topics
                    conceptDict['both_numTopTopics'] = len(both_TopTopics)
                    conceptDict['both_numUniqueTopTopics'] = count_unique_items(both_TopTopics)
                    conceptDict['both_weightSum'] = both_WeightSum
                    conceptDict['both_numSources'] = len(conceptSources_both)
                    
                    ## concepts
                    #conceptDict['conc_numSources'] = len(conceptSources_conc)
                    #if len(conceptSources_conc) > 0:
                    #    conc_TopTopics, conc_WeightSum = get_unique_top_topic_weights(conceptSources_conc,weights,weightThreshold) #get its top topics
                    #    conceptDict['conc_sourceVariety'] = weighted_entropy(conc_TopTopics, conc_WeightSum)
                    #    conceptDict['conc_topTopics'] = '_'.join(["%i$%.3f" %(key, value) for key, value in conc_TopTopics.items()]) #list of top topics
                    #    #conceptDict['conc_numTopTopics'] = len(conc_TopTopics)
                    #    conceptDict['conc_numUniqueTopTopics'] = len(conc_TopTopics)
                    #    conceptDict['conc_weightSum'] = conc_WeightSum
                    #else:
                    #    conceptDict['conc_sourceVariety'] = np.nan
                    #    conceptDict['conc_topTopics'] = np.nan
                    #    #conceptDict['conc_numTopTopics'] = np.nan
                    #    conceptDict['conc_numUniqueTopTopics'] = np.nan
                    #    conceptDict['conc_weightSum'] = np.nan
                    #
                    ## inspirations
                    #conceptDict['insp_numSources'] = len(conceptSources_insp)
                    #if len(conceptSources_insp) > 0:
                    #    insp_TopTopics, insp_WeightSum = get_unique_top_topic_weights(conceptSources_insp,weights,weightThreshold) #get its top topics
                    #    conceptDict['insp_sourceVariety'] = weighted_entropy(insp_TopTopics,insp_WeightSum)
                    #    conceptDict['insp_topTopics'] = '_'.join(["%i$%.3f" %(key, value) for key, value in insp_TopTopics.items()]) #list of top topics
                    #    #conceptDict['insp_numTopTopics'] = len(insp_TopTopics)
                    #    conceptDict['insp_numUniqueTopTopics'] = len(insp_TopTopics)
                    #    conceptDict['insp_weightSum'] = insp_WeightSum
                    #else:
                    #    conceptDict['insp_sourceVariety'] = np.nan
                    #    conceptDict['insp_topTopics'] = np.nan
                    #    #conceptDict['insp_numTopTopics'] = np.nan
                    #    conceptDict['insp_numUniqueTopTopics'] = np.nan
                    #    conceptDict['insp_weightSum'] = np.nan
                    conceptdata.append(conceptDict)
                variety_df = pd.DataFrame(conceptdata)
                outFileName = "%s/ConceptLevel_AfterDistanceAndControlsAndDiversityAndCorrectedDiscreteVariety_K%s-%s_T%d.csv" %(outputDir,k,run,int(weightThreshold*100))
                data = pd.read_csv(DATA_FILENAME) #open the data file
                masterDF = pd.merge(data,variety_df,how='left',on='nodeID') #merge into the master datafile
                #print masterDF.head()
                masterDF.to_csv(outFileName)
                #output_df(variety_df,DATA_FILENAME,outFileName)