"""
Read through the raw doc-composition files, spit out one text file for each document
that lists the top 5 topics for that document
"""

import csv

data_dir = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/TopicCompositions/"
doccompfile = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/CF0_DF0_400_ASP_optim_composition-6_formatted.txt"
keysfile = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/FINAL_malletLDA/CF0_DF0_400_ASP_optim_keys-6.txt"
namesfile = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/PythonCode/master_IDmappings.csv"

# get the doc-topic compositions
doccomps = {}
docnames = []
with open(doccompfile,'rU') as csvfile:
    filereader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in filereader:
        docname = row[1]
        doctop5topics = row[2:12]
        doccomps[docname] = doctop5topics
        docnames.append(docname)
csvfile.close()

# get the topic keys
topics = {}
with open(keysfile,'rU') as csvfile:
    filereader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in filereader:
        topics[row[0]] = row[2]
        
# get the fullname mappings
name_hash = {}
with open(namesfile,'rU') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        name_hash[row[1]] = row[0]

# do the real work
indices = [0,2,4,6,8]
for docname in docnames:
    docfilename = data_dir + "topwords_" + docname + ".txt"
    f = open(docfilename,'w')
    if "challenge" in docname:
        f.write(docname + "\n")
    else:
        f.write(name_hash[docname] + "\n")
    for index in indices:
        topicnum = doccomps[docname][index]
        topicweight = doccomps[docname][index+1]
        topicwords = topics[topicnum]
        towrite = "%s\t%.3f\n" %(topicnum, float(topicweight))
        f.write(towrite)
        f.write(topicwords + "\n")
    f.close()