#! /usr/bin/python
#
# This code computes source distance measures
#
# usage: python get_distance_measures.py <levelRange>
#
# where levelRange defines the range of levels (inclusive) in the genealogy you want to consider for the source distance measures
# e.g., 1-1 says only sources at level-1, 2-5 says only sources from levels 2 to 5

import numpy as np
import pandas as pd
import csv, sys

#############################################################################################################################################################
# PRELIMINARIES AND FILE PATHS
#############################################################################################################################################################

# function for computing cosine
def cosine(doc1, doc2):
    weights1 = doc_topic_weights[doc1]
    weights2 = doc_topic_weights[doc2]
    dotProduct = np.dot(weights1,weights2)
    mag1 = np.sqrt(sum([np.square(weight) for weight in weights1]))
    mag2 = np.sqrt(sum([np.square(weight) for weight in weights2]))
    return dotProduct/(mag1*mag2)

# normalize by type
def normalize_by_type(dataframe,desired_type,distances_raw):
    desired_type_raw_distances = [distances_raw[id] for id in dataframe[dataframe['type'] == desired_type].nodeID]
    desired_type_raw_distances = [d for d in desired_type_raw_distances if not np.isnan(d)]
    local_mean = np.mean(desired_type_raw_distances)
    local_sd = np.std(desired_type_raw_distances)
    output = {}
    for index, row in dataframe.iterrows():
        if row['type'] == desired_type and row['nodeID'] in doc_names:
            normalized = (distances_raw[row['nodeID']]-local_mean)/local_sd
            output[row['nodeID']] = normalized
        else:
            output[row['nodeID']] = np.nan
    return output

levelRange = sys.argv[1] #this command-line parameter determines range of levels to consider in the genealogy (1 = immediate)
fromLevel = int(levelRange.split('-')[0])
toLevel = int(levelRange.split('-')[1])
levels = [i for i in xrange(fromLevel,toLevel+1)] #create list of levels, inclusive of the upper limit (toLevel)

weightsfilename = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/sorted_CF0_DF0_400_ASP_optim_composition-6.csv"
docmetadatafilename = "/Users/jchan/Desktop/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/DocLevel.csv"
pathlevelfilename = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Paths/_CSVversions/paths_all.csv"

#############################################################################################################################################################
# COMPUTE DISTANCE AT THE DOC-LEVEL
#############################################################################################################################################################
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

# create doc-level data frame
docmetadata_df = pd.read_csv(docmetadatafilename)
doclevel_df = pd.DataFrame(doc_names,columns=['nodeID']) #use the doc name list from the LDA output file so that we have challenge briefs to start with
doclevel_df = pd.merge(doclevel_df,docmetadata_df,how='outer') #merge by outer so that we get the missing voting_C-119 and voting_I-369 into the doclevel
doclevel_df['challenge'] = [s.split('_')[0] for s in doclevel_df.nodeID] #make sure that the challenge field for challengebrief docs is not missing

print "Computing distances at doc-level..."
# Now we'd like to iterate over each challenge, computing the cosine for each concept/inspiration vs its challenge brief.
# First, we groupby challenge. Next, we grab the cosine for each concept/inspiration vs its challenge brief,
# and also create a standardized (z-score) version of it.
# NOTE that here we are "reversing" the cosine by subtracting it from zero,
# so that smaller numbers (i.e., larger negative numbers) indicate *less* DISTANCE,
# and the closer we get to ZERO, the FARTHER we are from the reference point.
# **NOTE:** For some reason the cosine of a doc vs itself is not 1 (i.e., in this case, challenge brief vs itself)! Not sure what the deal is here...
# We're flagging them as 'NaN' for now. SHOULD go back and check if my reshaping of the doc-topic-matrix makes sense.
# I don't think there's any bug there though, just a bug in my understanding of how cosine works
# I tried various versions of identity dot-products (i.e., a dot-product between a vector and itself) for a sample unit-vector,
# and none of them went to 1. HOLE IN MENTAL MODEL!

# compute distances (raw and normalized versions)
distances_raw = {}
distances_z_all = {}
distances_z_insp = {}
distances_z_concept = {}
for name, group in doclevel_df.groupby(['challenge']):
    
    group_doc_names = [n for n in group.nodeID]
    
    # raw distances
    group_distances_raw = {}
    for group_doc_name in group_doc_names:
        if 'challengebrief' not in group_doc_name and group_doc_name in doc_names:
            distance = 0-cosine(group_doc_names[0],group_doc_name)
            group_distances_raw[group_doc_name] = distance
        else:
            group_distances_raw[group_doc_name] = np.nan
    distances_raw.update(group_distances_raw)
    
    # normalized for all relative to both inspirations and concepts
    group_distances_z_all = {}
    group_raw_distances = [value for value in group_distances_raw.values() if not np.isnan(value)] # drop the missing values so we can compute means and sds
    mean = np.mean(group_raw_distances)
    sd = np.std(group_raw_distances)
    for group_doc_name, doc_distance_raw in group_distances_raw.items():    
        if not np.isnan(doc_distance_raw):
            distance = (doc_distance_raw-mean)/sd
            group_distances_z_all[group_doc_name] = distance
        else:
            group_distances_z_all[group_doc_name] = np.nan
    distances_z_all.update(group_distances_z_all)
        
    # normalized for inspirations relative to inspirations
    group_distances_z_insp = normalize_by_type(group,'inspiration',group_distances_raw)
    distances_z_insp.update(group_distances_z_insp)
        
    # normalized for concepts relative to concepts    
    group_distances_z_concept = normalize_by_type(group,'concept',group_distances_raw)
    distances_z_concept.update(group_distances_z_concept)
    
# put all computed values back into the master data frame
doclevel_df['distance_raw'] = [distances_raw[doc] for doc in doclevel_df['nodeID']]
doclevel_df['distance_z_all'] = [distances_z_all[doc] for doc in doclevel_df['nodeID']]
doclevel_df['distance_z_insp'] = [distances_z_insp[doc] for doc in doclevel_df['nodeID']]
doclevel_df['distance_z_concept'] = [distances_z_concept[doc] for doc in doclevel_df['nodeID']]

# delete the challengebrief rows
doclevel_df = doclevel_df[pd.notnull(doclevel_df.views)]

# print out for later use
#doclevel_df.to_excel("DocLevel_AfterDistance_Level.xlsx")

#############################################################################################################################################################
# COMPUTE DISTANCE AT THE CONCEPT-LEVEL
#############################################################################################################################################################
print "Reading in paths from file..."
# read in the paths, create data for challenge and source type
pathlevel_df = pd.read_csv(pathlevelfilename)
pathlevel_df['challenge'] = [n.split('_')[0] for n in pathlevel_df.seed_ID]
pathlevel_df['sourcetype'] = [n.split('_')[1] for n in pathlevel_df.source_ID]
pathlevel_df['sourcetype'] = [n[0] for n in pathlevel_df.sourcetype]

# trim to only levels we care about (defined in levelRange). isin method from http://stackoverflow.com/questions/12065885/how-to-filter-the-dataframe-rows-of-pandas-by-within-in
pathlevel_df = pathlevel_df[pathlevel_df['level'].isin(levels)]

print "Importing distance data into path-level dataframe..."
# grab the source_ID distances
pathlevel_df['source_dist_raw'] = [float(doclevel_df[doclevel_df.nodeID == s].distance_raw) for s in pathlevel_df.source_ID]
pathlevel_df['source_dist_z_all'] = [float(doclevel_df[doclevel_df.nodeID == s].distance_z_all) for s in pathlevel_df.source_ID]
pathlevel_df['source_dist_z_insp'] = [float(doclevel_df[doclevel_df.nodeID == s].distance_z_insp) for s in pathlevel_df.source_ID]
pathlevel_df['source_dist_z_concept'] = [float(doclevel_df[doclevel_df.nodeID == s].distance_z_concept) for s in pathlevel_df.source_ID]

# print out for later use
#pathlevel_df.to_excel("PathLevel_AfterDistance_Level%s.xlsx" %levelRange)

print "Computing distance measures at concept-level..."
# Now get all the concept-level measures.
# NOTE: we are not dealing with voting_C-119 and I-369 because they are not cited, so they shouldn't throw anything off
conceptdata = []
for name, group in pathlevel_df.groupby(['seed_ID']):
    # both kinds of sources
    rowdict = {'nodeID':name}
    rowdict['both_dist_raw_mean'] = group.source_dist_raw.mean()
    rowdict['both_dist_raw_max'] = np.nanmax(group.source_dist_raw)
    rowdict['both_dist_raw_std'] = group.source_dist_raw.std()
    rowdict['both_dist_z_all_mean'] = group.source_dist_z_all.mean()
    rowdict['both_dist_z_all_max'] = np.nanmax(group.source_dist_z_all)
    rowdict['both_dist_z_all_std'] = group.source_dist_z_all.std()
    rowdict['both_dist_count'] = group.source_dist_z_all.count()
    # concept sources
    if len(group[group.sourcetype == 'C'].source_dist_raw) > 0:
        rowdict['concept_dist_raw_mean'] = group[group.sourcetype == 'C'].source_dist_raw.mean()
        rowdict['concept_dist_raw_max'] = np.nanmax(group[group.sourcetype == 'C'].source_dist_raw)
        rowdict['concept_dist_raw_std'] = group[group.sourcetype == 'C'].source_dist_raw.std()
        rowdict['concept_dist_z_all_mean'] = group[group.sourcetype == 'C'].source_dist_z_all.mean()
        rowdict['concept_dist_z_all_max'] = np.nanmax(group[group.sourcetype == 'C'].source_dist_z_all)
        rowdict['concept_dist_z_all_std'] = group[group.sourcetype == 'C'].source_dist_z_all.std()
        rowdict['concept_dist_z_concept_mean'] = group[group.sourcetype == 'C'].source_dist_z_concept.mean()
        rowdict['concept_dist_z_concept_max'] = np.nanmax(group[group.sourcetype == 'C'].source_dist_z_concept)
        rowdict['concept_dist_z_concept_std'] = group[group.sourcetype == 'C'].source_dist_z_concept.std()
        rowdict['concept_dist_count'] = group[group.sourcetype == 'C'].source_dist_z_all.count()
    else:
        rowdict['concept_dist_raw_mean'] = np.nan
        rowdict['concept_dist_raw_max'] = np.nan
        rowdict['concept_dist_raw_std'] = np.nan
        rowdict['concept_dist_z_all_mean'] = np.nan
        rowdict['concept_dist_z_all_max'] = np.nan
        rowdict['concept_dist_z_all_std'] = np.nan
        rowdict['concept_dist_z_concept_mean'] = np.nan
        rowdict['concept_dist_z_concept_max'] = np.nan
        rowdict['concept_dist_z_concept_std'] = np.nan
        rowdict['concept_dist_count'] = 0
    # inspiration sources
    if len(group[group.sourcetype == 'I'].source_dist_raw) > 0:
        rowdict['insp_dist_raw_mean'] = group[group.sourcetype == 'I'].source_dist_raw.mean()
        rowdict['insp_dist_raw_max'] = np.nanmax(group[(group.sourcetype == 'I') ].source_dist_raw)
        rowdict['insp_dist_raw_std'] = group[group.sourcetype == 'I'].source_dist_raw.std()
        rowdict['insp_dist_z_all_mean'] = group[group.sourcetype == 'I'].source_dist_z_all.mean()
        rowdict['insp_dist_z_all_max'] = np.nanmax(group[group.sourcetype == 'I'].source_dist_z_all)
        rowdict['insp_dist_z_all_std'] = group[group.sourcetype == 'I'].source_dist_z_all.std()
        rowdict['insp_dist_z_insp_mean'] = group[group.sourcetype == 'I'].source_dist_z_insp.mean()
        rowdict['insp_dist_z_insp_max'] = np.nanmax(group[group.sourcetype == 'I'].source_dist_z_insp)
        rowdict['insp_dist_z_insp_std'] = group[group.sourcetype == 'I'].source_dist_z_insp.std()
        rowdict['insp_dist_count'] = group[group.sourcetype == 'I'].source_dist_z_all.count()
    else:
        rowdict['insp_dist_raw_mean'] = np.nan
        rowdict['insp_dist_raw_max'] = np.nan
        rowdict['insp_dist_raw_std'] = np.nan
        rowdict['insp_dist_z_all_mean'] = np.nan
        rowdict['insp_dist_z_all_max'] = np.nan
        rowdict['insp_dist_z_all_std'] = np.nan
        rowdict['insp_dist_z_insp_mean'] = np.nan
        rowdict['insp_dist_z_insp_max'] = np.nan
        rowdict['insp_dist_z_insp_std'] = np.nan
        rowdict['insp_dist_count'] = 0
    conceptdata.append(rowdict)
conceptdata_df = pd.DataFrame(conceptdata)

# and finally, create a conceptlevel file from the doclevel dataframe, and merge this distance data in
conceptlevel_df = doclevel_df[doclevel_df['type'] == 'concept']
conceptlevel_df_merged = pd.DataFrame.merge(conceptlevel_df,conceptdata_df,how='left')

# print out for later use
conceptlevel_df_merged.to_excel("ConceptLevel_AfterDistance_Level%s_CORRECTED.xlsx" %levelRange)

print "Finished!"
