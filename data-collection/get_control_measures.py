import numpy as np
import pandas as pd
from pandas import Series, DataFrame

#############################################################################################################################################################
# PRELIMINARIES AND PATHS
#############################################################################################################################################################

def format_date_string(unformatted):
    """
    Take an unformatted date-time string and put it in the proper format
    that pandas will be able to easily recognize and convert to its datetime format
    e.g., [in] April 02, 2011, 05:29pm --> [out] 2011-04-02 17:29
    """
    months = {'January': '01',
              'February': '02',
              'March': '03',
              'April': '04',
              'May': '05',
              'June': '06',
              'July': '07',
              'August': '08',
              'September': '09',
              'October': '10',
              'November': '11',
              'December': '12'}

    twentyfour_am = {'12':'00',
                     '01':'01',
                     '02':'02',
                     '03':'03',
                     '04':'04',
                     '05':'05',
                     '06':'06',
                     '07':'07',
                     '08':'08',
                     '09':'09',
                     '10':'10',
                     '11':'11',
                     '12':'12'}
    
    twentyfour_pm = {'12':'12',
                     '01':'13',
                     '02':'14',
                     '03':'15',
                     '04':'16',
                     '05':'17',
                     '06':'18',
                     '07':'19',
                     '08':'20',
                     '09':'21',
                     '10':'22',
                     '11':'23'}
   
    unformattedarr = unformatted.split(',')
    
    # year
    year = unformattedarr[1]
    year = year.strip()
    
    # month
    month = months[unformattedarr[0].split(' ')[0]]
    month = month.strip()
    
    # day
    day = str(unformattedarr[0].split(' ')[1])
    day = day.strip()
    
    # time
    timearr = unformattedarr[2].split(':')
    minute = timearr[1][:2]
    if timearr[1].endswith("pm"):
        hour = twentyfour_pm[timearr[0].strip()]
    else:
        hour = twentyfour_am[timearr[0].strip()]
    
    formatted = "%s-%s-%s %s:%s" %(year, month, day, hour, minute)
    return formatted

doclevelfilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/DocLevel_AfterDistance.xlsx"
pathlevelfilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/PathLevel_AfterDistance.xlsx"
conceptlevelfilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistance.xlsx"
rawcommentsfilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/AllCommentsData_2013-12-25.csv"
challengemetadatafilename = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ChallengeMetadata.csv"

#############################################################################################################################################################
# COMPUTE SOURCE QUALITY
#############################################################################################################################################################
print "Computing source quality..."
# read in data
print "\tReading in data..."
doclevel_df = pd.read_excel(doclevelfilename,'sheet1')
pathlevel_df = pd.read_excel(pathlevelfilename, 'sheet1')
conceptlevel_df = pd.read_excel(conceptlevelfilename, 'sheet1')

# import the shortlist data from doclevel into the path df
# create subset dataframe from doclevel, rename the nodeID as source_ID to match pathlevel
print "\tPutting shortlist data into pathlevel..."
shortlist_df = DataFrame(doclevel_df['nodeID'],columns=['source_ID'])
shortlist_df['source_shortlist'] = doclevel_df['shortlist']
# merge the subset dataframe into pathlevel
pathlevel_df = pd.merge(pathlevel_df,shortlist_df)

# now compute in conceptlevel df
print "\tCompute source shortlist data by concept..."
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
conceptlevel_df.num_shortlisted_sources[pd.isnull(conceptlevel_df['num_shortlisted_sources'])] = 0

#############################################################################################################################################################
# COMPUTE FEEDBACK
#############################################################################################################################################################
print "Computing feedback..."
# read in the comments and challenge data
comments = pd.read_csv(rawcommentsfilename)
challenge_data = pd.read_csv(challengemetadatafilename)

# convert shortlist date in challenge metadata into usable pandas format
print "\tProcessing dates at comments level..."
challenge_data['datetime_shortlistdate'] = [format_date_string(unformatted) for unformatted in challenge_data['shortlist_start']]
pd.to_datetime(challenge_data['datetime_shortlistdate'])

# do the same conversions in the comments df
comments['date_clean'] = [format_date_string(unformatted) for unformatted in comments.date]
pd.to_datetime(comments.date_clean)

# create flag variable for "before vs after shortlist"
# this could be optimized because i'm using slow iterrows method for now
before_shortlist = []
for rowindex, row in comments.iterrows():
    challenge_shortlistdate = challenge_data[challenge_data.challenge == row['challenge']].datetime_shortlistdate
    rowdate = row['date_clean']
    if rowdate < challenge_shortlistdate:
        before_shortlist.append(1)
    else:
        before_shortlist.append(0)
comments['before_shortlist'] = before_shortlist

# aggregate by document, put in new data frame to merge into master concept level
print "\tAggregating by concept and merging into master concept level data frame..."
concept_comments = pd.pivot_table(comments, rows='document',aggfunc={'before_shortlist':'sum'})
concept_comments.columns = ['comments_preshortlist'] #rename the column
concept_comments.index.names = ['nodeID'] #rename the index so we can merge

# merge into the master data frame
conceptlevel_df = pd.merge(conceptlevel_df,concept_comments,how='left',left_on='nodeID',right_index=True)

# change missing to "0" for concepts that have no comments
conceptlevel_df.comments_preshortlist[pd.isnull(conceptlevel_df['comments_preshortlist'])] = 0

# finished! output for analysis
print "Finished!"
conceptlevel_df.to_excel("ConceptLevel_AfterDistanceAndControls.xlsx")

