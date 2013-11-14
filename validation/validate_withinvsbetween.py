#! /usr/bin/python
#
# this code will iterate over the model output files
# for each file, it will:
# 1) slice the first 50 concepts from each challenge
# next, for each slice:
# 1) compute and summarize (mean, sd) the inner pairwise cosines,
# 2) compute pairwise cosines for each of the other slices
# 3) summarize (mean, sd) the collective pairwise cosines vs other slices
# 4) get the d and t-value for the difference between mean(within) vs mean(between)
# spit out two files:
# first file summarizes the mean within (with sd), mean between (with sd)
# second file will spit out mean within (with sd), 

import csv, itertools, numpy, os
from scipy import stats
from sys import argv

def within_vs_between(infilename):
    # read in the data
    #infilename = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/LDA_CF1_DF50_ASP_opt10/ForValidation/sorted_CF1_DF50_12_ASP_optim_composition-6.csv"
    rawdata = []
    filereader = csv.reader(open(infilename, 'rb'))
    for row in filereader:
        rawdata.append(','.join(row))
    rawdata = rawdata[1:] #discard header
        
    doc_topic_weights = {}
    doc_names = []
    cb_indices = []
    for d in rawdata:
        data = d.split(",")
        docname = data[0] #redundant, but helpful for readability
        weights = data[1:] #slice out the topic weights
        weights = [float(i) for i in weights] #convert all to float
        doc_topic_weights[docname] = weights #put in the dict
        doc_names.append(docname) 
        if "challengebrief" in docname: #store the index for any challenge brief we encounter
            cb_indices.append(rawdata.index(d))
    
    # slice first 50 concepts from each challenge
    samples = []
    for index in cb_indices:
        currentsample = []
        startindex = index+1
        stopindex = index+51
        for i in xrange(startindex, stopindex):
            currentsample.append(doc_names[i])
        samples.append(currentsample)
    
    innercosines_master = []
    betweencosines_master = []
    cohen_d_list = []
    t_value_list = []
    # for each challenge
    for sample in samples:
        # compute pairwise lists
        # inner pairs
        innerpairs = []
        for i in xrange(len(sample)):
            for j in xrange(i+1,len(sample)):
                pair = (sample[i],sample[j]) # store in a tuple
                innerpairs.append(pair)
        # between pairs
        betweenpairs = []
        for i in xrange(len(samples)):
            if samples[i] != sample:
                pairs = itertools.product(sample, samples[i])
                for p in pairs:
                    betweenpairs.append(p)
                    
        # compute cosines
        # inner pairs
        innercosines = []
        for pair in innerpairs:
            cosine = numpy.dot(doc_topic_weights[pair[0]],doc_topic_weights[pair[1]])
            innercosines.append(cosine)
            innercosines_master.append(cosine)
        innercosine_mean = numpy.mean(innercosines)
        innercosine_sd = numpy.std(innercosines)
        innercosine_N = len(innercosines)
        print "\tmean cosine for inner pairs = %.3f (SD = %.3f, N = %i)" %(innercosine_mean, innercosine_sd, innercosine_N)
        
        # between pairs
        betweencosines = []
        for pair in betweenpairs:
            cosine = numpy.dot(doc_topic_weights[pair[0]],doc_topic_weights[pair[1]])
            betweencosines.append(cosine)
            betweencosines_master.append(cosine)
        betweencosine_mean = numpy.mean(betweencosines)
        betweencosine_sd = numpy.std(betweencosines)
        betweencosine_N = len(betweencosines)
        print "\tmean cosine for between pairs = %.3f (SD = %.3f, N = %i)" %(betweencosine_mean, betweencosine_sd, betweencosine_N)
        
        # d and t
        # cohen's d
        cohen_d = (innercosine_mean-betweencosine_mean)/((innercosine_sd+betweencosine_sd)/2)
        cohen_d_list.append(cohen_d)
        t_value, p_value = stats.ttest_ind(innercosines, betweencosines, equal_var=False)
        t_value_list.append(t_value)
        print "\t\tthe difference in means is d = %.3f, t = %.3f, p = %.3f" %(cohen_d, t_value, p_value)
    
    #summaries
    innercosine_mean_overall = numpy.mean(innercosines_master)
    betweencosine_mean_overall = numpy.mean(betweencosines_master)
    cohen_d_mean = numpy.mean(cohen_d_list)
    t_value_mean = numpy.mean(t_value_list)
    
    results = (innercosine_mean_overall, betweencosine_mean_overall, cohen_d_mean, t_value_mean)
    return results

data_dir = argv[1]

# benchmark and print to file
resultsfilename = data_dir + "benchmarkRESULTS_within_vs_between.txt" 
resultsfile = open(resultsfilename,'w')
resultsfile.write("numtopics\titernumber\tfilename\tmeaninnercosine\tmeanbetweencosine\tmeancohend\tmeantvalue\n")
for fnamefull in os.listdir(data_dir):
    if fnamefull.endswith(".csv"): #pesky .DS_store!!
        print "Benchmarking for %s..." %fnamefull
        data_filename = data_dir + fnamefull
        meaninnercosine, meanbetweencosine, meancohend, meantvalue = within_vs_between(data_filename)
        # make the metadata info
        # Assumes this format: sorted_CF1_DF50_12_ASP_optim_composition-1.csv
        f_noext = fnamefull.split(".")[0]
        f_info = f_noext.split("_")
        numtopics = f_info[3]
        iternumber = f_info[-1].split("-")[1]
        towrite = "%s\t%s\t%s\t%.3f\t%.3f\t%.3f\t%.3f\t\n" %(numtopics, iternumber, f_noext, meaninnercosine, meanbetweencosine, meancohend, meantvalue)
        resultsfile.write(towrite)
resultsfile.close()