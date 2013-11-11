#! /usr/bin/python
#

from sys import argv
from scipy.stats.stats import pearsonr
import numpy
import os

def my_sumproduct(a,b):
    sum = 0
    for i in xrange(len(a)):
        sum += a[i]*b[i]
    return sum

def continuous_benchmarks(infilename,benchmarkdata):
    
    """
    Read in challenge brief and inspirations
    """
    doc_topic_weightsfile = open(infilename)
    doc_topic_weights = []
    for line in doc_topic_weightsfile.readlines():
        doc_topic_weights.append(line)
        
    #challenge brief
    rawquery = doc_topic_weights[index_ewastechallengebrief].strip().split(",")
    #print rawquery
    query = []
    for i in xrange(1,len(rawquery)):
       query.append(float(rawquery[i])) 
    
    #inspirations
    rawindex = doc_topic_weights[index_ewasteinspstart:index_ewasteinspstop+1]
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
        #print len(index), len(query)
        cosines.append(my_sumproduct(index,query))
        #cosines.append(numpy.dot(index,query))
    
    """
    Correlate cosines with human judgments, print to screen, save to results file
    """
    
    d_noext = d.split(".")[0]
    outfilename = "%se-waste_insp_cosines_%s.txt" %(data_dir, d_noext)
    resultsfile = open(outfilename,'w')
    for cosine in cosines:
        resultsfile.write(str(cosine) + "\n")
    resultsfile.close()
    #print "%i human ratings" %len(benchmarkdata)
    #print "%i cosines" %len(cosines)
    #print benchmarkdata
    #print cosines
    result = pearsonr(benchmarkdata,cosines)
    print "For %s, r = %.3f, p = %.3f" %(d, result[0], result[1])
    return cosines

human_ratings = [4.00,4.80,2.60,3.40,3.40,4.80,5.00,4.80,4.20,3.40,5.00,1.60,4.60,2.80,3.80,2.20,3.80,5.00,5.20,5.80,4.80,3.20,4.80,4.00,3.20,3.80,4.20,3.60,2.60,2.60,4.60,3.60,3.40,4.40,5.00,4.20,4.00,4.20,4.40,4.20,3.80,3.80,3.40,4.40,5.20,4.80,4.20,2.20,2.60,5.00,4.80,5.00,5.00,3.20,4.00,4.20,4.60,3.60,4.40,4.00,5.00,2.80,4.40,2.80,2.40,2.60,5.60,5.60,3.40,4.20,5.00,4.40,4.60,3.80,1.40,2.00,4.60,4.00,2.20,4.00,1.80,4.00,3.60,3.00,4.00,4.00,4.20,3.00,3.80,3.80,3.00,4.00,2.00,2.80,5.20,4.00,4.00,4.00,4.60,3.60,3.40,3.80,3.60,4.00,3.80,4.80,3.60,2.80,3.60,1.40,3.60,2.60,3.60,3.60,3.60,3.60,4.40,3.80,3.00,3.40,3.80,3.60,1.20,1.80,4.20,3.60,3.60,4.40,4.00,4.00,3.40,3.80,4.00,4.40,4.40,3.20,5.00,4.40,4.80,4.60,4.60,4.00,4.80,3.80,3.60,2.60,5.20,3.80,3.60,2.80,4.20,2.80,4.00,4.40,5.00,2.40,4.60,3.20,3.80,2.00,2.60,3.80,3.80,4.20,3.80,2.20,3.80,3.80,2.60,4.60,4.00,3.60,4.20,4.60,5.00,3.40,3.00,4.40,5.00,3.40,3.80,3.20,4.60,2.40,3.60,4.00,3.60,4.60,3.20,3.80,5.20,4.40,3.40,4.60,4.40,2.20,4.40,4.60,4.40]

data_dir = argv[1]
#outfilename = argv[2]
index_ewastechallengebrief = 1003
index_ewasteinspstart = 1110
index_ewasteinspstop = 1308
#index_bonemarrowchallengebrief = 0
#index_bonemarrowinspstart = 283
#index_bonemarrowinspstop = 627
  

# # # # # # # # # # # # # # 
# Continuous benchmarking #
# # # # # # # # # # # # # #


mastercosines = []
for d in os.listdir(data_dir):
    if d.endswith(".csv"): #pesky .DS_store!!
        #print "Benchmarking %s..." %d
        data_filename = data_dir + d
        #print data_filename
        mastercosines.append(continuous_benchmarks(data_filename,human_ratings))

masterdatafilename = data_dir + "e-waste_insp_cosines_MASTER.txt"
masteroutfile = open(masterdatafilename,'w')
for mastercosine in mastercosines:
    for cosine in mastercosine:
        #towrite = str(cosine) 
        masteroutfile.write(str(cosine) + "\t")
    masteroutfile.write("\n")
masteroutfile.close()


    
