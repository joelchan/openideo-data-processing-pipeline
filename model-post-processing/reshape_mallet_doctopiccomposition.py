from sys import argv

infilename = argv[1]
outfilename = argv[2]
numTopics = int(argv[3])

# read in the data, discard the first row (the header row)
rawData = open(infilename).readlines()
rawData.pop(0)

# open outfile, prepare header
outfile = open(outfilename, 'w')
outfile.write("doc,")
for k in xrange(0,numTopics):
    outfile.write(str(k) + ",")
outfile.write("\n")

# reshape data and print to file
counter = 1
for row in rawData:
    weights = {}
    data = row.strip().split("\t") # added strip because of the ghost new line
    
    # write the doc name
    outfile.write(data[1] + ",")
    
    # get the topic-weight mappings
    for i in xrange(2,len(data),2):
        weights[data[i]] = data[i+1]
     
    # now print them to the file
    for i in xrange(0, numTopics):
        outfile.write(weights[str(i)])
        if i+1 != numTopics: # if we aren't at the last topic
            outfile.write(",") # add a delimiter
    
    if row != rawData[-1]: # if we aren't at the last row
        outfile.write("\n")
    counter += 1
    
print "%i docs processed." %counter
outfile.close()
        