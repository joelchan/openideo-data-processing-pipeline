def sum_product(a,b):
	
	if len(a) != len(b):
		raise ValueError, "a and b must be same length"

	result = 0
	for i in range(len(a)):
		result += a[i]*b[i]
	
	return result
# end sum_product function	

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
	
def getsimdata_liststyle(start_stop,all_data):
	# outer loop (running through the start_stop)
	print "started outer start_stop loop..."
	counter = 0; # for the current file name
	#outfile = open("all_simlist.txt",'w')
	for items in start_stop:
	
		start = items[0] # define the starting point to slice from all_data
		stop = items[1] # define the stopping point for the slice
	
		# create the current file
		current_outfile_name = "simlist_for_challenge-%d.csv" % (counter+1)
		current_outfile = open(current_outfile_name, 'w')
	
		# grab appropriate slice of all_data
		nodes = all_data[start:(stop+1)]
		
		# inner loops (create sim list for each start_stop)
		print "creating sim list for item #%d in start_stop slice, starting at %d and ending at %d..." % (counter + 1, start, stop)
		for i in range(len(nodes)):
			for j in range(len(nodes)):
				if not(j == i): # skip identity comparisons
					a = nodes[i]
					b = nodes[j]
					#print a
					#print b
					cosine = sum_product(a[1:-1],b[1:-1])
					towrite = "%s VS %s,%.8f\n" %(a[0], b[0], cosine)
					current_outfile.write(towrite)
					#outfile.write(towrite)
					#if j == len(nodes) - 1: # if it's the last comparison for this i
					#	current_outfile.write("%f\t\n" % cosine) # write it with a new line
					#else:
					#	current_outfile.write("%f\t" % cosine)
			
		counter += 1 # increment the counter for the next file name
	
	current_outfile.close()
	#outfile.close()
	print "Finished!"

start_stop = [[0,630],
			  [631,1004],
			  [1005,1310], 
			  [1311,2347], 
			  [2348,2924],
			  [2925,3475],
			  [3476,3863],
			  [3864,4073],
			  [4074,5297],
			  [5298,5887],
			  [5888,6409],
			  [6410,6912]]

num_dims = 90
num_docs = 6913 # how many docs?
	
# initialize empty matrix to hold all the data
all_data = [[None for i in range(num_dims+1)] for j in range(num_docs)]
	
# read in the data
print "reading in data from file..."
input_file = "weights_90.csv"
docs = read_data(input_file)
	
print "adding data to internal matrix..."
for i in range(num_docs):
	weights = docs[i].split(',')
	all_data[i][0] = weights[0]
	print all_data[i][0]
	for j in range(1,num_dims):
		#print "adding element [%d][%d] to all_data..." %(i, j)
		all_data[i][j] = float(weights[j])

getsimdata_liststyle(start_stop,all_data)

#def main(argv):
#
#	# this array holds start and stop indices that define slices in the data 
#	# the data slices correspond to the design challenges
#	start_stop = [[0,630],
#				  [631,1004],
#				  [1005,1310], 
#				  [1311,2347], 
#				  [2348,2924],
#				  [2925,3475],
#				  [3476,3863],
#				  [3864,4073],
#				  [4074,5297],
#				  [5298,5887],
#				  [5888,6409],
#				  [6410,6912]]
#	
#	#start_stop = [[0,630],[631,1004]]
#	
#	num_dims = 750 # each doc represented with how many dimensions?
#	num_docs = 6913 # how many docs?
#	
#	# initialize empty matrix to hold all the data
#	all_data = [[None for i in range(num_dims)] for j in range(num_docs)]
#	
#	# read in the data
#	print "reading in data from file..."
#	input_file = "weights.csv"
#	docs = read_data(input_file)
#	
#	print "adding data to internal matrix..."
#	for i in range(num_docs):
#		weights = docs[i].split(',')
#		for j in range(num_dims):
#			#print "adding element [%d][%d] to all_data..." %(i, j)
#			all_data[i][j] = float(weights[j])

#if __name__ == '__main__':
#	main(sys.argv[1:])

#def getsimdata_matrixstyle(start_stop,all_data):
#	# outer loop (running through the start_stop)
#	print "started outer start_stop loop..."
#	counter = 0; # for the current file name
#	for items in start_stop:
#	
#		start = items[0] # define the starting point to slice from all_data
#		stop = items[1] # define the stopping point for the slice
#	
#		# create the current file
#		current_outfile_name = "challenge-%d.txt" % (counter+1)
#		current_outfile = open(current_outfile_name, 'w')
#	
#		# grab appropriate slice of all_data
#		nodes = all_data[start:(stop+1)]
#	
#		# inner loops (create sim matrix for each start_stop)
#		print "creating simmatrix for item #%d in start_stop slice, starting at %d and ending at %d..." % (counter + 1, start, stop)
#		for i in range(len(nodes)):
#			for j in range(len(nodes)):
#				if j == i: # for identity comparisons
#					if j == len(nodes) - 1: # if it's the last comparison for this i
#						current_outfile.write("1.0\t\n") # write it with a new line
#					else:
#						current_outfile.write("1.0\t")
#				else:
#					cosine = sum_product(nodes[i],nodes[j])
#					if j == len(nodes) - 1: # if it's the last comparison for this i
#						current_outfile.write("%f\t\n" % cosine) # write it with a new line
#					else:
#						current_outfile.write("%f\t" % cosine)
#			
#		counter += 1 # increment the counter for the next file name
#	
#	print "Finished!"