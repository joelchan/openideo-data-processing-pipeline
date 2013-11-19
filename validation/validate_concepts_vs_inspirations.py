#! /usr/bin/python
#

from sys import argv
#from scipy.stats.stats import ttest_ind
import math
import numpy
import os
import pandas as pd

def read_data(filename):
	"""
	Read in data from a file and return a list with each element being one line from the file.
	Parameters:
	1) filename: name of file to be read from
	Note: the code now opens as a binary and replaces carriage return characters with newlines because python's read and readline functions don't play well with carriage returns.
	However, this will no longer be an issue with python 3.
	"""	
	with open(filename, "rb") as f:
		s = f.read().replace('\r\n', '\n').replace('\r', '\n')
		data = s.split('\n')
	
	return data

def concepts_vs_insps(infilename,filenamestem):
    # get the data, store in dict: keys are docnames, values are topic-weight vectors (in float format)
    rawdata = read_data(infilename)
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
    
    # compute cosines and store in list of lists
    all_cosine_data = []
    for i in xrange(len(cb_indices)):
        current_cb_index = cb_indices[i]
        if i+1 == len(cb_indices):
            next_cb_index = len(doc_names)
        else:
            next_cb_index = cb_indices[i+1]
        cb_weights = doc_topic_weights[doc_names[current_cb_index]]
        for i in xrange(current_cb_index+1,next_cb_index):
            current_cosine_data = []
            doc_name = doc_names[i]
            current_cosine_data.append(doc_name.split("_")[1]) #challengename
            current_cosine_data.append(doc_name.split("_")[2][0]) #doctype (C or I)
            current_cosine_data.append(doc_name)
            current_cosine_data.append(numpy.dot(cb_weights,doc_topic_weights[doc_names[i]]))
            all_cosine_data.append(current_cosine_data)
    
    ## print out the list of lists for intermediate processing        
    #outfile = open("testoutfile.csv",'w')
    #outfile.write("challengename,doctype,docname,cosine\n")
    #for line in all_cosine_data:
    #    for i in xrange(len(line)):
    #        outfile.write(str(line[i]))
    #        if i != len(line)+1:
    #            outfile.write(",")
    #    outfile.write("\n")
        
    # convert to dataframe
    all_cosine_dictlist = []
    for line in all_cosine_data:
        cosine_dict = {"challenge":line[0],"type":line[1],"name":line[2],"cosine":line[3]}
        all_cosine_dictlist.append(cosine_dict)
    cosine_df = pd.DataFrame(all_cosine_dictlist)
    
    # descriptives (mean, SD, N) for concepts and inspirations
    summary_cosine_df = cosine_df.groupby('type').agg([numpy.mean, numpy.std, numpy.size])
    c_mean = float(summary_cosine_df.ix['C']['cosine']['mean'])
    c_std = float(summary_cosine_df.ix['C']['cosine']['std'])
    c_size = int(summary_cosine_df.ix['C']['cosine']['size'])
    i_mean = float(summary_cosine_df.ix['I']['cosine']['mean'])
    i_std = float(summary_cosine_df.ix['I']['cosine']['std'])
    i_size = int(summary_cosine_df.ix['I']['cosine']['size'])
    
    # standardized difference and t-value for difference
    cohen_d = (c_mean-i_mean)/((c_std+i_std)/2)
    pooled_sd = math.sqrt(((c_size-1)*math.pow(c_std,2)+(i_size-1)*math.pow(i_std,2))/(c_size+i_size-2))
    diff = c_mean-i_mean
    estimator = math.sqrt((1.0/c_size)+(1.0/i_size))
    t_value = diff/(pooled_sd*estimator)
    
    # make the metadata info
    # Assumes this format: sorted_CF1_DF50_12_ASP_optim_composition-1.csv
    d_noext = filenamestem.split(".")[0]
    d_info = d_noext.split("_")
    numtopics = d_info[3]
    iternumber = d_info[-1].split("-")[1]

    # this is temp stuff to print out the concept and inspiration cosines when i'm just running this on one file
    conceptcosines = []
    inspcosines = []
    for dictlist in all_cosine_dictlist:
        data = "%s\t%f" %(dictlist["name"], dictlist["cosine"])
        if dictlist["type"] == 'C':  
            conceptcosines.append(data)
        else:
            inspcosines.append(data)

    conceptcosine_out = open("conceptcosines.txt",'w')
    for cosine in conceptcosines:
        conceptcosine_out.write(cosine + "\n")
    conceptcosine_out.close()
    
    inspcosine_out = open("inspcosines.txt",'w')
    for cosine in inspcosines:
        inspcosine_out.write(cosine + "\n")
    inspcosine_out.close()

    # write the results to file, print to screen
    towrite = "%s\t%s\t%s\t%.3f\t%.3f\t%i\t%.3f\t%.3f\t%i\t%.3f\t%.3f\n" %(numtopics, iternumber, d_noext, c_mean, c_std, c_size, i_mean, i_std, i_size, cohen_d, t_value)
    resultsfile.write(towrite)
    print "\tConcepts (N = %i) have mean cosine of %.3f, with SD of %.3f" %(c_size, c_mean, c_std)
    print "\tInspirations (N = %i) have mean cosine of %.3f, with SD of %.3f" %(i_size, i_mean, i_std)
    print "\tThe difference between the mean cosines for concepts vs inspirations is %.3f" %cohen_d
    print "\tThe t-value for this difference is %.3f" %t_value
    
data_dir = argv[1]

# benchmark and print to file
resultsfilename = data_dir + "benchmarkRESULTS_concepts_vs_inspirations.txt" 
resultsfile = open(resultsfilename,'w')
resultsfile.write("numtopics\titernumber\tfilename\tconcept_mean\tconcept_sd\tconcept_N\tinsp_mean\tinsp_sd\tinsp_N\tcohen_d\tt-value\n")
for d in os.listdir(data_dir):
    if d.endswith(".csv"): #pesky .DS_store!!
        print "Benchmarking for %s..." %d
        data_filename = data_dir + d
        concepts_vs_insps(data_filename,d)
resultsfile.close()