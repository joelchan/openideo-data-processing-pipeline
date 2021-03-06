#! /usr/bin/python
#
# This code computes source diversity measures
#
# usage: python get_diversity_measures.py <levelRange>
#
# where levelRange defines the range of levels (inclusive) in the genealogy you want to consider for the source diversity measures
# e.g., 1-1 says only sources at level-1, 2-5 says only sources from levels 2 to 5

import numpy as np
import pandas as pd
import itertools as it
import csv, sys

# function for computing cosine
def cosine(doc1, doc2):
    weights1 = doc_topic_weights[doc1]
    weights2 = doc_topic_weights[doc2]
    dotProduct = np.dot(weights1,weights2)
    mag1 = np.sqrt(sum([np.square(weight) for weight in weights1]))
    mag2 = np.sqrt(sum([np.square(weight) for weight in weights2]))
    return dotProduct/(mag1*mag2)

datafilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControls_Level1-1.xlsx"
pathfilename = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Paths/_CSVversions/paths_all.csv"
weightsfilename = "/Users/joelc/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/sorted_CF0_DF0_400_ASP_optim_composition-6.csv"

levelRange = sys.argv[1] #this command-line parameter determines range of levels to consider in the genealogy (1 = immediate)
fromLevel = int(levelRange.split('-')[0])
toLevel = int(levelRange.split('-')[1])
levels = [i for i in xrange(fromLevel,toLevel+1)] #create list of levels, inclusive of the upper limit (toLevel)

# read in the doc-topic weights
print "Reading in weights..."
doc_topic_weights = {}
with open(weightsfilename, 'rU') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        if 'doc' not in row[0]: #skip the header
            docname = row[0].replace("tokenized_","").replace(".txt","")
            doc_topic_weights[docname] = [float(i) for i in row[1:]]
csvfile.close

# read in the paths, create data for seed type so we can select later (for the set); may want to add source type later if we want to grab diversity only for inspirations
print "Reading in paths..."
pathlevel_df = pd.read_csv(pathfilename)
pathlevel_df = pathlevel_df[pathlevel_df['level'].isin(levels)] # trim to the levels we want
pathlevel_df['seedtype'] = [n.split('_')[1] for n in pathlevel_df.seed_ID] #create seed type
pathlevel_df['seedtype'] = [n[0] for n in pathlevel_df.seedtype]

# get the set of concepts to be processed
concepts = set()
concepts.update(pathlevel_df[pathlevel_df.seedtype == 'C'].seed_ID)
concepts = sorted(concepts)

### MAIN FUNCTION HERE ###
# for each concept, we'll get its sources, then (if it's got more than 1 source),
# generate all possible combinations, then grab all pairwise cosines and spit out summary statistics (mean, min, max, sd)
# finally, we'll make it into a dataframe
print "Computing diversity..."
concept_diversity = []
counter = 0
for concept in concepts:
    #get all its immediate sources
    sources = pathlevel_df[pathlevel_df.seed_ID == concept].source_ID
    sources_concepts = [source for source in sources if '_C-' in source]
    sources_inspirations = [source for source in sources if '_I-' in source]
    #row_dict['both_dist_count'] = len(sources)
    #row_dict['concept_dist_count'] = len(sources)
    #row_dict['insp_dist_count'] = len(sources)
    row_dict = {}
    if len(sources) > 1: #both concepts and inspirations
        row_dict['nodeID'] = concept
        #generate all possible pairs
        source_combos = [x for x in it.combinations(sources,2)] #n choose 2
        #get all the cosines
        distances = [0-cosine(combo[0],combo[1]) for combo in source_combos]
        #summary statistics: mean, max, min, sd
        row_dict['both_div_mean'] = np.mean(distances)
        row_dict['both_div_min'] = np.min(distances)
        row_dict['both_div_max'] = np.max(distances)
        row_dict['both_div_sd'] = np.std(distances)
    if len(sources_concepts) > 1: #concepts
        #generate all possible pairs
        source_combos = [x for x in it.combinations(sources_concepts,2)] #n choose 2
        #get all the cosines
        distances = [0-cosine(combo[0],combo[1]) for combo in source_combos]
        #summary statistics: mean, max, min, sd
        row_dict['concept_div_mean'] = np.mean(distances)
        row_dict['concept_div_min'] = np.min(distances)
        row_dict['concept_div_max'] = np.max(distances)
        row_dict['concept_div_sd'] = np.std(distances)
    if len(sources_inspirations) > 1: #concepts
        #generate all possible pairs
        source_combos = [x for x in it.combinations(sources_inspirations,2)] #n choose 2
        #get all the cosines
        distances = [0-cosine(combo[0],combo[1]) for combo in source_combos]
        #summary statistics: mean, max, min, sd
        row_dict['insp_div_mean'] = np.mean(distances)
        row_dict['insp_div_min'] = np.min(distances)
        row_dict['insp_div_max'] = np.max(distances)
        row_dict['insp_div_sd'] = np.std(distances)
    if len(row_dict) > 0: 
        concept_diversity.append(row_dict)
    counter += 1
    sys.stdout.write("\tProcessed %i of %i concepts...\r" %(counter, len(concepts)))
    sys.stdout.flush()
concept_diversity_df = pd.DataFrame(concept_diversity) #make into dataframe

# merge into the master data file and export
print "\nCleaning up..."
data = pd.read_excel(datafilename,sheetname='data') #open the data file
data = pd.merge(data,concept_diversity_df,how='left') #merge in the data
data.to_csv("ConceptLevel_AfterDistanceAndControlsAndDiversity_Level%s.csv" %levelRange)
print "Done!!"