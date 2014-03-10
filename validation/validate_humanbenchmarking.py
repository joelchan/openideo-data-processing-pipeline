#! /usr/bin/python
#

from sys import argv
from scipy.stats.stats import pearsonr
import numpy as np
import os

def cos(weights1, weights2):
    dotProduct = np.dot(weights1,weights2)
    mag1 = np.sqrt(sum([np.square(weight) for weight in weights1]))
    mag2 = np.sqrt(sum([np.square(weight) for weight in weights2]))
    return dotProduct/(mag1*mag2)

def benchmark(infilename,anchorindex,slicestartindex, slicestopindex, benchmarkdata,resultsfile):
    
    """
    Read in challenge brief and inspirations
    """
    doc_topic_weightsfile = open(infilename)
    doc_topic_weights = [line for line in doc_topic_weightsfile.read().replace('\r\n', '\n').replace('\r', '\n').split('\n')]
    #for line in doc_topic_weightsfile.readlines():
    #    doc_topic_weights.append(line)
        
    #challenge brief
    rawquery = doc_topic_weights[anchorindex].strip().split(",")
    #print rawquery
    query = []
    for i in xrange(1,len(rawquery)):
       query.append(float(rawquery[i])) 
    
    #inspirations
    rawindex = doc_topic_weights[slicestartindex:slicestopindex+1]
    cleanindex = []
    for index in rawindex:
        indexrowraw = index.strip().split(",")
        indexrow = []
        for i in xrange(1,len(indexrowraw)):
            indexrow.append(float(indexrowraw[i]))
        cleanindex.append(indexrow)
    
    """
    Compute cosines
    """
    cosines = []
    for index in cleanindex:
        cosines.append(cos(index,query))
    
    """
    Correlate cosines with human judgments, print to screen, save to results file
    """
    
    # THIS IS ALL VERY BRITTLE AT THE MOMENT - DEPENDS ON A PARTICULAR NAMING SYSTEM FOR THE DOC-TOPIC FILENAME
    # sorted_<CFsetting>_<DFsetting>_<numtopics>_ASP_optim_composition-<iternumber>.csv
    d_noext = d.split(".")[0]
    d_info = d_noext.split("_")
    numtopics = d_info[3]
    iternumber = d_info[-1].split("-")[1]
    correls = pearsonr(benchmarkdata,cosines)
    print "\tFor %s, r = %.3f, p = %.3f" %(d, correls[0], correls[1])
    towrite = "%s\t%s\t%s\t%.3f\t%.3f\n" %(numtopics, iternumber, d_noext, correls[0], correls[1])
    resultsfile.write(towrite)
    return cosines

human_ratings_continuous = [4.00,4.80,2.60,3.40,3.40,4.80,5.00,4.80,4.20,3.40,5.00,1.60,4.60,2.80,3.80,2.20,3.80,5.00,5.20,5.80,4.80,3.20,4.80,4.00,3.20,3.80,4.20,3.60,2.60,2.60,4.60,3.60,3.40,4.40,5.00,4.20,4.00,4.20,4.40,4.20,3.80,3.80,3.40,4.40,5.20,4.80,4.20,2.20,2.60,5.00,4.80,5.00,5.00,3.20,4.00,4.20,4.60,3.60,4.40,4.00,5.00,2.80,4.40,2.80,2.40,2.60,5.60,5.60,3.40,4.20,5.00,4.40,4.60,3.80,1.40,2.00,4.60,4.00,2.20,4.00,1.80,4.00,3.60,3.00,4.00,4.00,4.20,3.00,3.80,3.80,3.00,4.00,2.00,2.80,5.20,4.00,4.00,4.00,4.60,3.60,3.40,3.80,3.60,4.00,3.80,4.80,3.60,2.80,3.60,1.40,3.60,2.60,3.60,3.60,3.60,3.60,4.40,3.80,3.00,3.40,3.80,3.60,1.20,1.80,4.20,3.60,3.60,4.40,4.00,4.00,3.40,3.80,4.00,4.40,4.40,3.20,5.00,4.40,4.80,4.60,4.60,4.00,4.80,3.80,3.60,2.60,5.20,3.80,3.60,2.80,4.20,2.80,4.00,4.40,5.00,2.40,4.60,3.20,3.80,2.00,2.60,3.80,3.80,4.20,3.80,2.20,3.80,3.80,2.60,4.60,4.00,3.60,4.20,4.60,5.00,3.40,3.00,4.40,5.00,3.40,3.80,3.20,4.60,2.40,3.60,4.00,3.60,4.60,3.20,3.80,5.20,4.40,3.40,4.60,4.40,2.20,4.40,4.60,4.40]
human_ratings_binary = [0,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1,1,1,0,0,1,0,0,1,0,1,0,1,1,1,1,1,0,1,1,0,0,1,1,0,1,1,1,1,1,0,0,1,1,0,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,1,1,0,1,1,1,0,1,0,0,0,1,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1,0,0,1,1,0,1,0,0,1,1,1,0,1,0,0,1,0,0,0,0,1,1,1,0,0,1,0,1,1,1,0,0,1,0,1,0,0,1,1,0,0,1,0,1,1,1,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,0,0,0,1,1,1,0,0,1,1,1,1,0,1,1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,1,1,1,0,0,0,1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1,0,1,0,1,1,0,1,1,1,1,1,0,0,1,0,1,1,0,0,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,1,1,0,1,0,1,0,0,1,1,0,0,1,1,1,1,0,0,1,0,1,0,1,1,1,1,1,0,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,1,0,1,0,1,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,0,1]

data_dir = argv[1]


# THESE ARE ALL VERY BRITTLE!!! MAKE SURE THEY MATCH UP BEFORE RUNNING.
# shouldn't change anymore since i think we are locked in wrt N docs
index_ewastechallengebrief = 1003
index_ewasteinspstart = 1110
index_ewasteinspstop = 1308

index_bonemarrowchallengebrief = 1
index_bonemarrowinspstart = 284
index_bonemarrowinspstop = 628 

fileorder = []

# # # # # # # # # # # # # # 
# Continuous benchmarking #
# # # # # # # # # # # # # #

print "Continuous benchmarking..."

# benchmark and print to file
continuousresultsfilename = data_dir + "benchmarkRESULTS_continuous_e-waste.txt"
continuousresultsfile = open(continuousresultsfilename,'w')
# header
continuousresultsfile.write("numtopics\titernumber\tfilename\tcorrelation\tp-value\n")
# data
continuouscosines = []
for d in os.listdir(data_dir):
    if d.endswith(".csv"): #pesky .DS_store!!
        dname = d.split('.')[0]
        fileorder.append(d)
        data_filename = data_dir + d
        continuouscosines.append(benchmark(data_filename,index_ewastechallengebrief,index_ewasteinspstart,index_ewasteinspstop,human_ratings_continuous,continuousresultsfile))

# store the cosines in a file
continuouscosinedatafilename = data_dir + "cosines_continuous_e-waste.txt"
continouscosine_outfile = open(continuouscosinedatafilename,'w')
# header 
for order in fileorder:
    continouscosine_outfile.write(order + "\t")
continouscosine_outfile.write("\n")
#data
for i in xrange(len(continuouscosines[0])):
    row = ""
    for continuouscosine in continuouscosines:
        row = row + str(continuouscosine[i]) + "\t"
    towrite = row.strip() + "\n" 
    continouscosine_outfile.write(towrite)
continouscosine_outfile.close()

# # # # # # # # # # # # # # 
# Binary benchmarking     #
# # # # # # # # # # # # # #

print "Binary benchmarking..."

# benchmark and print to file
binaryresultsfilename = data_dir + "benchmarkRESULTS_binary_bone-marrow.txt" 
binaryresultsfile = open(binaryresultsfilename,'w')
# header file
binaryresultsfile.write("numtopics\titernumber\tfilename\tcorrelation\tp-value\n")
# data
binarycosines = []
for d in os.listdir(data_dir):
    if d.endswith(".csv"): #pesky .DS_store!!
        data_filename = data_dir + d
        binarycosines.append(benchmark(data_filename,index_bonemarrowchallengebrief,index_bonemarrowinspstart,index_bonemarrowinspstop,human_ratings_binary,binaryresultsfile))

# store the cosines in a file
binarycosinedatafilename = data_dir + "cosines_binary_bone-marrow.txt"
binarycosine_outfile = open(binarycosinedatafilename,'w')
# header
for order in fileorder:
    binarycosine_outfile.write(order + "\t")
binarycosine_outfile.write("\n")
for i in xrange(len(binarycosines[0])):
    row = ""
    for binarycosine in binarycosines:
        row = row + str(binarycosine[i]) + "\t"
    towrite = row.strip() + "\n" 
    binarycosine_outfile.write(towrite)
binarycosine_outfile.close()
