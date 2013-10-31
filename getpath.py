from sys import argv

script, edgefilename, seedfilename, resultsfilename, depth = argv 

"""
	Helper functions.
"""

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

def find(probe, list):
	"""
	Check if a probe string is in a list of strings.
	Returns true or false.
	Parameters:
	1) probe: string you want to search for
	2) list: list of strings to search in
	"""
	found = False
	for l in list:
		if probe == l:
			found = True
	return found

def get_path(seeds, edges, splitchar, depth, resultsfilename):
	"""
	Find all the sources of a list of seeds (to a specified depth), skipping duplicates.
	Returns a count for debugging purposes (to check if any seeds were skipped)
	Parameters:
	1) seeds: list of seeds to be checked
	2) edges: list of edges from which seed paths will be extracted
	3) split: character that will be used to split source-target pairs in the edge list
	4) depth: int that specifies depth to which paths will be followed
	5) resultsfilename: file to which results will be written
	"""
	currentstack = []
	nextstack = []
	history = []
	counter = 0
	
	# prepare the results file
	resultsfile = open(resultsfilename, 'w')
	resultsfile.write("seed\tlevel\tsource\ttarget\n")
	
	for s in seeds: # for each seed
		
		currentstack.append(s)	# initialize currentstack with current seed
		for i in range(1,depth+1): # for d levels, where d is specified by the depth parameter
			
			for target in currentstack: # for each target in the current stack
				
				# get all immediate sources from the edge list
				for e in edges:
					temp = e.split(splitchar)
					if target == temp[1] and not(find(temp[0], history)): # if the target matches our current target, and its source is not in our history
						
						# write it to the results file
						towrite = "%s\t%d\t%s\t%s\n" % (s, i, temp[0], target)
						resultsfile.write(towrite) 
						
						history.append(temp[0]) # add the source to the history list
						nextstack.append(temp[0]) # remember the source so we can find its sources in the next iteration
			
			# done getting all sources for all targets in currentstack 
			# now dump those sources onto the current stack so we can find their sources
			dump(nextstack, currentstack) 
		
		# done getting the path for the current seed
		# now clear the history and current stack for the next seed
		del history[:] 
		del currentstack[:]
		counter += 1
	
	# end function. done getting paths for all the seeds
	# now close the resultsfile and pass the counter value to the calling statement
	resultsfile.close()
	return counter
		
def dump(listfrom, listto):
	"""Replace all contents in a destination list with contents from a source list, and clear the source list."""
	del listto[:]
	for l in listfrom:
		listto.append(l)
	del listfrom[:]
	
""""
	MAIN function body starts here
	IMPORTANT note on data inputs: before running the code, check how the source-target pairs are separated.
	If csv, the comma should work; else, may have to change to \t
"""

# this variable defines what character will be used to split the source-target
# pairs for edges in the edge list
# change it if the edge input file is not csv (or equivalent)
splitchar = ','

# read in the seeds and edges
seeds = read_data(seedfilename)
edges = read_data(edgefilename)

# get the paths
deep = int(depth)
processed = get_path(seeds, edges, splitchar, deep, resultsfilename)

# final report
if len(seeds) == processed:
	print "Success! There were %d edges, and we processed %d out of %d seeds." % (len(edges), processed, len(seeds))
else:
	print "Finished, but something went wrong. There were %d edges, and we only processed %d out of %d seeds." % (len(edges), processed, len(seeds))