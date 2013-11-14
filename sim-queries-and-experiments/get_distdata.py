"""
merge with metadata?? too complicated - just do it by hand
"""

import os, csv, numpy, pandas, collections
from sys import argv

def process_challenge(infilename, doc_topic_weights, doc_names, cb_indices, outdata):
    # read in the path data
    """
    to deal with this error: _csv.Error: new-line character seen in unquoted field - do you need to open the file in universal-newline mode?
    assumes input format:
    0 - seed
    1 - source
    2 - target
    3 - level
    """
    pathdata = []
    seeds = []
    levels = ["immediate","indirect-recent","indirect-medium","indirect-old"]
    with open(infilename, 'rU') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in filereader:
            if row[3] != "level": #not the header row
                if int(row[3]) == 1:
                    rowtuple = (row[0],row[1],"immediate") #seed, source, level
                elif int(row[3]) > 1 and int(row[3]) <= 4:
                    rowtuple = (row[0],row[1],"indirect-recent")
                elif int(row[3]) > 4 and int(row[3]) <= 7:
                    rowtuple = (row[0],row[1],"indirect-medium")
                else:
                    rowtuple = (row[0],row[1],"indirect-old")
                pathdata.append(rowtuple)
                if row[0] not in seeds:
                    seeds.append(row[0])
    
    # compute the data for each level
    cbweights = doc_topic_weights[doc_names[cb_indices[0]]]
    currentindex = 0
    
    debugfile = open("debugfile.txt",'w')
    for seed in seeds:
        seedweights = doc_topic_weights[seed]
        seeddata = {"0_conceptname":seed}
        for level in levels:
            levelcosines_cb = []
            levelcosines_con = []
            fieldname_cb = "cb_" + str(levels.index(level)+1) + "_meandist_" + level
            fieldname_con = "con_" + str(levels.index(level)+1) + "_meandist_" + level
            while currentindex < len(pathdata) and pathdata[currentindex][0] == seed and pathdata[currentindex][2] == level:
                query = pathdata[currentindex][1]
                queryweights = doc_topic_weights[query]
                levelcosines_cb.append(numpy.dot(cbweights,queryweights))
                levelcosines_con.append(numpy.dot(seedweights,queryweights))
                currentindex += 1
            if len(levelcosines_cb) > 0: # what if we don't have any at this level?
                levelcosinemean_cb = numpy.mean(levelcosines_cb)
                levelcosinemean_con = numpy.mean(levelcosines_con)
                seeddata[fieldname_cb] = levelcosinemean_cb
                seeddata[fieldname_con] = levelcosinemean_con
                for levelcosine in levelcosines_cb:
                    towrite = "%s\t%s\t%s\t%.3f\n" %(seed,query,level,levelcosine)
                    debugfile.write(towrite)
            else:
                seeddata[fieldname_cb] = "NaN"
                seeddata[fieldname_con] = "NaN"
            
        sortedseeddata = collections.OrderedDict(sorted(seeddata.items(), key=lambda t:t[0]))
        outdata.append(sortedseeddata)
    debugfile.close()

data_dir = argv[1]
doctopicweightsfilename = argv[2]
outfilename = argv[3]

# read in the doc-topic weights
rawdoctopic = []
with open(doctopicweightsfilename, 'rU') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        rawdoctopic.append(','.join(row))
rawdoctopic = rawdoctopic[1:] #discard header

doc_topic_weights = {}
doc_names = []
cb_indices = []
for d in rawdoctopic:
    data = d.split(",")
    docname = data[0].replace("tokenized_","").replace(".txt","") #redundant, but helpful for readability
    weights = data[1:] #slice out the topic weights
    weights = [float(i) for i in weights] #convert all to float
    doc_topic_weights[docname] = weights #put in the dict
    doc_names.append(docname) 
    if "challengebrief" in docname: #store the index for any challenge brief we encounter
        cb_indices.append(rawdoctopic.index(d))
        
outdata = []
for d in os.listdir(data_dir):
    if d.endswith(".csv"): #pesky .DS_store!!
        print "Processing %s..." %d
        data_filename = data_dir + d
        process_challenge(data_filename,doc_topic_weights, doc_names, cb_indices, outdata)

#convert to dataframe and print out
df = pandas.DataFrame(outdata)
df.to_csv(outfilename)