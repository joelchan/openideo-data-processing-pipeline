#! /usr/bin/python
#
# This code computes "self-anchored" source distance measures (i.e., distance of sources from parent concept, not problem domain)
#
# usage: python get_distance_from_self.py <levelRange>
#
# where levelRange defines the range of levels (inclusive) in the genealogy you want to consider for the source distance measures
# e.g., 1-1 says only sources at level-1, 2-5 says only sources from levels 2 to 5

import numpy as np
import pandas as pd
import csv, sys

def cosine(doc1,doc2):
    """
    function for computing cosine
    """
    weights1 = doc_topic_weights[doc1]
    weights2 = doc_topic_weights[doc2]
    dotProduct = np.dot(weights1,weights2)
    mag1 = np.sqrt(sum([np.square(weight) for weight in weights1]))
    mag2 = np.sqrt(sum([np.square(weight) for weight in weights2]))
    return dotProduct/(mag1*mag2)

def cosines_from_self(myself,mysources):
    """
    function for computing distance from self:
    returns list of cosines
    """
    cosines = []
    for source in mysources:
        cosines.append(cosine(myself,source))
    return cosines

levelRange = sys.argv[1] #this command-line parameter determines range of levels to consider in the genealogy (1 = immediate)
fromLevel = int(levelRange.split('-')[0])
toLevel = int(levelRange.split('-')[1])
levels = [i for i in xrange(fromLevel,toLevel+1)] #create list of levels, inclusive of the upper limit (toLevel)

weightsfilename = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/sorted_CF0_DF0_400_ASP_optim_composition-6.csv"
datafilename = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControls_Level1-1.csv"
pathlevelfilename = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Paths/_CSVversions/paths_all.csv"

### GET WEIGHTS ###
print "Getting LDA weights from file..."
# read in the doc-topic weights
doc_names = []
doc_topic_weights = {}
with open(weightsfilename, 'rU') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        if 'doc' not in row[0]: #skip the header
            docname = row[0].replace("tokenized_","").replace(".txt","")
            doc_topic_weights[docname] = [float(i) for i in row[1:]]
            doc_names.append(docname)
csvfile.close()

### GET PATHS ###
print "Reading in paths from file..."
# read in the paths, create data for challenge and source type
pathlevel_df = pd.read_csv(pathlevelfilename)
pathlevel_df['challenge'] = [n.split('_')[0] for n in pathlevel_df.seed_ID]
pathlevel_df['seedtype'] = [n.split('_')[1] for n in pathlevel_df.seed_ID]
pathlevel_df['seedtype'] = [n[0] for n in pathlevel_df.seedtype]
pathlevel_df['sourcetype'] = [n.split('_')[1] for n in pathlevel_df.source_ID]
pathlevel_df['sourcetype'] = [n[0] for n in pathlevel_df.sourcetype]
pathlevel_df = pathlevel_df[pathlevel_df['level'].isin(levels)] # trim to only levels we care about (defined in levelRange). isin method from http://stackoverflow.com/questions/12065885/how-to-filter-the-dataframe-rows-of-pandas-by-within-in

### COMPUTE DISTANCE FROM SELF ###
print "Computing distance from self..."
concepts = set()
concepts.update(pathlevel_df[pathlevel_df['seedtype'] == "C"].seed_ID)
conceptdata = []
for concept in concepts:
    
    rowdict = {'nodeID':concept}
    # get sources
    sources_both = pathlevel_df[pathlevel_df['seed_ID'] == concept].source_ID
    sources_concepts = [s for s in sources_both if "_C-" in s]
    sources_inspirations = [s for s in sources_both if "_I-" in s]
    
    # both
    cosines_both = cosines_from_self(concept,sources_both)
    rowdict['both_distSelf_mean'] = np.mean(cosines_both)
    rowdict['both_distSelf_min'] = np.nanmin(cosines_both)
    rowdict['both_distSelf_max'] = np.nanmax(cosines_both)
    
    # concepts
    if len(sources_concepts) > 0:
        cosines_concepts = cosines_from_self(concept,sources_concepts)
        rowdict['conc_distSelf_mean'] = np.mean(cosines_concepts)
        rowdict['conc_distSelf_min'] = np.nanmin(cosines_concepts)
        rowdict['conc_distSelf_max'] = np.nanmax(cosines_concepts)
    else:
        rowdict['conc_distSelf_mean'] = np.nan
        rowdict['conc_distSelf_min'] = np.nan
        rowdict['conc_distSelf_max'] = np.nan
        
    # inspirations
    if len(sources_inspirations) > 0:
        cosines_insp = cosines_from_self(concept,sources_inspirations)
        rowdict['insp_distSelf_mean'] = np.mean(cosines_insp)
        rowdict['insp_distSelf_min'] = np.nanmin(cosines_insp)
        rowdict['insp_distSelf_max'] = np.nanmax(cosines_insp)
    else:
        rowdict['insp_distSelf_mean'] = np.nan
        rowdict['insp_distSelf_min'] = np.nan
        rowdict['insp_distSelf_max'] = np.nan
    
    conceptdata.append(rowdict)
conceptdata_df = pd.DataFrame(conceptdata)

### CLEAN UP ###
print "Cleaning up..."
conceptlevel_df = pd.read_csv(datafilename)
conceptlevel_df_merged = pd.DataFrame.merge(conceptlevel_df,conceptdata_df,how='left')
conceptlevel_df_merged.to_csv("ConceptLevel_AfterDistanceAndControlsAndSelfDistance_Level%s.csv" %levelRange)

print "Finished!"
