"""
Get cosines for all nodes vs their challenge briefs
"""

import numpy
from sys import argv

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
	
def getsimdata(start_stop,all_data,master_output_filename):
    
    master_output_file = open(master_output_filename, 'w')
    
    # outer loop (running through the start_stop)
    print "started outer start_stop loop..."
    counter = 0; # for the current file name
    for items in start_stop:
    
        start = items[0] # define the starting point to slice from all_data
        stop = items[1] # define the stopping point for the slice
    
        # create the current file
        current_outfile_name = "challenge-brief-anchored_cosines_for_challenge-%d.csv" % (counter+1)
        current_outfile = open(current_outfile_name, 'w')
    
        # grab appropriate slice of all_data
        nodes = all_data[start:(stop+1)]
    
        # inner loops (create sim list for each start_stop)
        print "creating sim list for item #%d in start_stop slice, starting at %d and ending at %d..." % (counter + 1, start, stop)
        challengebrief = nodes[0]
        #print challengebrief
        for i in range(1,len(nodes)):
            doc = nodes[i]
            cosine = numpy.dot(doc[1:],challengebrief[1:])
            towrite = "%s,%.8f" %(doc[0], cosine)
            current_outfile.write(towrite)
            master_output_file.write(towrite)
            if i+1 != len(nodes): # if we aren't at the last doc in the challenge
                current_outfile.write("\n") # add a new line
                master_output_file.write("\n")

        counter += 1 # increment the counter for the next file name
        current_outfile.close()
    master_output_file.close()
    print "Finished!"

# this is terrible, terrible, terrible - hard coded start/stop indices - MAKE SURE you have 6,913 documents!!!
start_stop = [[1,631],
			  [632,1005],
			  [1006,1311], 
			  [1312,2348], 
			  [2349,2925],
			  [2926,3476],
			  [3477,3864],
			  [3865,4074],
			  [4075,5298],
			  [5299,5888],
			  [5889,6410],
			  [6411,6913]]

input_file = argv[1]
num_docs = int(argv[2])
num_dims = int(argv[3])
master_output_file = argv[4]
	
# initialize empty matrix to hold all the data
all_data = [[None for i in range(num_dims+1)] for j in range(num_docs)]
	
# read in the data
print "reading in data from file..."
docs = read_data(input_file)
	
print "adding data to internal matrix..."
for i in range(num_docs):
    weights = docs[i].split(',')
    all_data[i][0] = weights[0]
    print all_data[i][0]
    for j in xrange(1,num_dims+1):
        all_data[i][j] = float(weights[j])

getsimdata(start_stop,all_data,master_output_file)