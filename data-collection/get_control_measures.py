import numpy as np
import pandas as pd
from pandas import Series, DataFrame

#############################################################################################################################################################
# COMPUTE SOURCE QUALITY
#############################################################################################################################################################

# read in data
doclevelfilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/openideo-data-processing-pipeline/data-collection/DocLevel_AfterDistance.xlsx"
pathlevelfilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/openideo-data-processing-pipeline/data-collection/PathLevel_AfterDistance.xlsx"
conceptlevelfilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/openideo-data-processing-pipeline/data-collection/ConceptLevel_AfterDistance.xlsx"

doclevel_df = pd.read_excel(doclevelfilename,'sheet1')
pathlevel_df = pd.read_excel(pathlevelfilename, 'sheet1')
conceptlevel_df = pd.read_excel(conceptlevelfilename, 'sheet1')

# import the shortlist data from doclevel into the path df
# create subset dataframe from doclevel, rename the nodeID as source_ID to match pathlevel
shortlist_df = DataFrame(doclevel_df['nodeID'],columns=['source_ID'])
shortlist_df['source_shortlist'] = doclevel_df['shortlist']
# merge the subset dataframe into pathlevel
pathlevel_df = pd.merge(pathlevel_df,shortlist_df)

# now compute in conceptlevel df
conceptdata = []
for name, group in pathlevel_df.groupby(['seed_ID']):
    # both kinds of sources
    rowdict = {'nodeID':name}
    rowdict['num_shortlisted_sources'] = np.sum(group.source_shortlist)
    conceptdata.append(rowdict)
conceptdata_df = pd.DataFrame(conceptdata)
conceptlevel_df = pd.merge(conceptlevel_df,conceptdata_df) # merge into concept level 

# create binary indicator
conceptlevel_df['any_shortlisted_sources'] = 0
conceptlevel_df.any_shortlisted_sources[conceptlevel_df['num_shortlisted_sources'] > 0] = 1

# change missing to "0" for concepts that cite no concept sources
conceptlevel_df.num_shortlisted_sources[conceptlevel_df['num_shortlisted_sources'] == 'NaN'] = 0

# temp output
conceptlevel_df.to_excel("ConceptLevel_AfterDistanceAndControls.xlsx")

#############################################################################################################################################################
# COMPUTE FEEDBACK
#############################################################################################################################################################

# get this code from getting_clean_comments_data.ipynb