#! /usr/bin/python

# usage: python get_simmatrix.py <labelsfile> <weightsfile>

import numpy as np
import sys, csv

def cos(a,b):
    dotProduct = np.dot(a,b)
    magA = np.sqrt(sum([np.square(i) for i in a]))
    magB = np.sqrt(sum([np.square(i) for i in b]))
    return dotProduct/(magA*magB)

def get_simmatrix(labelsFile,weightsFile):
    
    # read in the labels and weights
    # labels
    print "Reading in labels..."
    labels = []
    with open(labelsFile, 'rU') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        labels = [row[0] for row in filereader]
    csvfile.close()
    
    # doc-topic weights
    print "Reading in weights..."
    weights = {}
    with open(weightsFile, 'rU') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in filereader:
            if 'doc' not in row[0]: #skip the header
                docname = row[0].replace("tokenized_","").replace(".txt","")
                weights[docname] = [float(i) for i in row[1:]]
    csvfile.close()
    
    # simmatrix
    cosines = []
    history = []
    for i in xrange(len(labels)):
        print "Processing %s..." %labels[i]
        row = []
        for j in xrange(len(labels)):
            currentPair = ' '.join(sorted([labels[i],labels[j]]))
            if currentPair not in history:
                history.append(currentPair)
                cosines.append(cos(weights[labels[i]],weights[labels[j]]))
            #   row.append(1.0)
            #else:
                #row.append(cos(weights[labels[i]],weights[labels[j]]))
        #cosines.append(row)

    # print out
    print "Printing out..."
    #outfilename = "%s_simmatrix.csv" %labelsFile.replace(".csv","")
    outfilename = "%s_simlist.csv" %labelsFile.replace(".csv","")
    outfile = open(outfilename,'w')    
    for cosine in cosines:
        #outfile.write(','.join([str(c) for c in cosine]))
        #outfile.write("\n")
        outfile.write(str(cosine) + "\n")
    outfile.close()
    print "Finished!"

if __name__ == '__main__':
    labelsFile = sys.argv[1]
    weightsFile = sys.argv[2]
    get_simmatrix(labelsFile, weightsFile)