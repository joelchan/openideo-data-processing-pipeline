"""
0 - seed
1 - level
2 - source
3- target
"""

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
	f.close()
	return data

def get_seedlevel_sources(items):
    itemsources = {}
    for item in items:
        itemsplit = item.split(",") #split the row into columns
        seedlevel = itemsplit[0] #get the seedlevel info
        if seedlevel in itemsources: #if we've already seen this seedlevel
            itemsources[seedlevel].append(itemsplit[1]) #add this source to this seedlevel's list of sources
        else: #otherwise create a new entry
            temparr = []
            temparr.append(itemsplit[1])
            itemsources[seedlevel] = temparr
    return itemsources
    
def get_seedlevel_sourcepairs(seedlevel, itemsources):
    sourcelist = itemsources[seedlevel]
    sourcepairlist = []
    for i in xrange(len(sourcelist)): #do combinations, not permutations, i.e., n choose 2
        for j in xrange(i+1,len(sourcelist)):
            query = "%s VS %s" %(sourcelist[i], sourcelist[j])
            sourcepairlist.append(query)
    return sourcepairlist

def get_mean_pairwisecosine(simindex,queries,debugfile):
	cosine_sum = 0.0
	for query in queries:
		if query not in simindex:
			debugfile.write(query + "\n")
		else:
			cosine_sum += simindex[query]
	return cosine_sum/len(queries)

def process_challenge(pathfilename,simfilename,resultsfilename):

	"""
	Read in the list of seed-levels with their source-target pair data
	"""
	print "\tReading in list of seed-levels with data..."
	items = read_data(pathfilename)
	
	"""
	Get list of sources for each seed-level
	""" 
	print "\tGetting list of sources for each seed-level..."
	itemsources = get_seedlevel_sources(items)
	
	"""
	Get all source pairings for each seed-level
	"""
	print "\tGetting all source pairings for each seed-level..."
	for key in itemsources:
		itemsources[key] = get_seedlevel_sourcepairs(key, itemsources)
	
	"""
	Read in the sim data
	"""
	print "\tReading in the sim data..."
	sims = read_data(simfilename)
	simindex = {}
	for i in xrange(len(sims)-1):
		simsplit = sims[i].split(',')
		simindex[simsplit[0]] = float(simsplit[1])
	
	"""
	Get the mean parwise cosines for each seed-level's source pair list
	"""
	print "\tGetting mean pairwise cosines for each seed-level's source pair list..."
	results = []
	debugfile = open("debugfile.txt",'w')
	for key in itemsources:
		#print "Processing seed-level %s..." %key
		if len(itemsources[key]) == 0: #if there's only one source at that level, diversity is undefined
			result = "%s,-9999" %key #-9999 is missing value
			results.append(result)
		else:
			cosine = get_mean_pairwisecosine(simindex,itemsources[key],debugfile)
			result = "%s,%.8f" %(key, cosine)
			results.append(result)
	debugfile.close()
	itemsources.clear()
	
	"""
	Write the results to file
	"""
	print "\tWriting results..."
	outfile = open(resultsfilename,'w')
	results.sort()
	for result in results:
		outfile.write(result + "\n")
	outfile.close()
	
#"""
#Read in list of simdata filenames and path filenames
#"""
#pathfilenames = read_data("pathfilenames.txt")
#print pathfilenames
#simfilenames = read_data("simfilenames.txt")
#print simfilenames
#
#resultsfile = open("all_diversitydata.txt",'w')
#for i in xrange(len(pathfilenames)):
#	print "Processing %s" %pathfilenames[i]
#	process_challenge(pathfilenames[i],simfilenames[i],resultsfile)
#resultsfile.close()

script, pathfilename, simfilename, resultsfilename = argv
process_challenge(pathfilename, simfilename, resultsfilename)