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
    
    # partition data
    paths_immediate = []
    paths_indirect_recent = []
    paths_indirect_medium = []
    paths_indirect_old = []
    for path in pathdata:
        pathlevel = path[2]
        if pathlevel == "immediate":
            paths_immediate.append(path)
        elif pathlevel == "indirect-recent":
            paths_indirect_recent.append(path)
        elif pathlevel == "indirect-medium":
            paths_indirect_medium.append(path)
        else:
            paths_indirect_old.append(path)
                
    #print paths_immediate
    #print paths_indirect_recent
    #print paths_indirect_medium
    #print paths_indirect_old
    with open("immediate.txt",'w') as f:
        for path in paths_immediate:
            for p in path:
                f.write(p + "\t")
            f.write("\n")
    f.close()
    with open("indirect-recent.txt",'w') as f:   
        for path in paths_indirect_recent:
            for p in path:
                f.write(p + "\t")
            f.write("\n")
    f.close()
    with open("indirect-medium.txt",'w') as f:
        for path in paths_indirect_medium:
            for p in path:
                f.write(p + "\t")
            f.write("\n")
    f.close()
    with open("indirect-far.txt",'w') as f:
        for path in paths_indirect_old:
            for p in path:
                f.write(p + "\t")
            f.write("\n")
    f.close()
    
    ##debugfile = open("debugfile.txt",'w')
    #for seed in seeds:
    #    seedweights = doc_topic_weights[seed]
    #    seeddata = {"0_conceptname":seed}
    #    # inspirations
    #    for level in levels:
    #        insp_levelcosines_cb = []
    #        insp_levelcosines_con = []
    #        fieldname_concept_cb = "concept_cb_" + str(levels.index(level)+1) + "_meandist_" + level
    #        fieldname_concept_con = "concept_con_" + str(levels.index(level)+1) + "_meandist_" + level
    #        while currentindex < len(pathdata) and pathdata[currentindex][0] == seed and pathdata[currentindex][2] == level:
    #            if "_I-" in pathdata[currentindex][1]:
    #                query = pathdata[currentindex][1]
    #                queryweights = doc_topic_weights[query]
    #                insp_levelcosines_cb.append(numpy.dot(cbweights,queryweights))
    #                insp_levelcosines_con.append(numpy.dot(seedweights,queryweights))
    #                currentindex += 1
    #        if len(insp_levelcosines_cb) > 0: # what if we don't have any at this level?
    #            insp_levelcosinemean_cb = numpy.mean(insp_levelcosines_cb)
    #            insp_levelcosinemean_con = numpy.mean(insp_levelcosines_con)
    #            seeddata[fieldname_insp_cb] = insp_levelcosinemean_cb
    #            seeddata[fieldname_insp_con] = insp_levelcosinemean_con
    #            #for levelcosine in levelcosines_cb:
    #            #    towrite = "%s\t%s\t%s\t%.3f\n" %(seed,query,level,levelcosine)
    #            #    debugfile.write(towrite)
    #        else:
    #            seeddata[fieldname_insp_cb] = "NaN"
    #            seeddata[insp_fieldname_insp_con] = "NaN"
    #    # concepts
    #    for level in levels:
    #        concept_levelcosines_cb = []
    #        concept_levelcosines_con = []
    #        fieldname_concept_cb = "concept_cb_" + str(levels.index(level)+1) + "_meandist_" + level
    #        fieldname_concept_con = "concept_con_" + str(levels.index(level)+1) + "_meandist_" + level
    #        while currentindex < len(pathdata) and pathdata[currentindex][0] == seed and pathdata[currentindex][2] == level:
    #            if "_C-" in pathdata[currentindex][1]:
    #                query = pathdata[currentindex][1]
    #                queryweights = doc_topic_weights[query]
    #                concept_levelcosines_cb.append(numpy.dot(cbweights,queryweights))
    #                concept_levelcosines_con.append(numpy.dot(seedweights,queryweights))
    #                currentindex += 1
    #        if len(concept_levelcosines_cb) > 0: # what if we don't have any at this level?
    #            concept_levelcosinemean_cb = numpy.mean(concept_levelcosines_cb)
    #            concept_levelcosinemean_con = numpy.mean(concept_levelcosines_con)
    #            seeddata[fieldname_concept_cb] = concept_levelcosinemean_cb
    #            seeddata[fieldname_concept_con] = concept_levelcosinemean_con
    #            #for levelcosine in levelcosines_cb:
    #            #    towrite = "%s\t%s\t%s\t%.3f\n" %(seed,query,level,levelcosine)
    #            #    debugfile.write(towrite)
    #        else:
    #            seeddata[fieldname_concept_cb] = "NaN"
    #            seeddata[fieldname_concept_con] = "NaN"
    #        
    #    sortedseeddata = collections.OrderedDict(sorted(seeddata.items(), key=lambda t:t[0]))
    #    outdata.append(sortedseeddata)
    #debugfile.close()

data_dir = argv[1]
doctopicweightsfilename = argv[2]
#outfilename = argv[3]

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
#df = pandas.DataFrame(outdata)
#df.to_csv(outfilename)