import os

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

messedupwords = read_data("bone-marrow_messedupwords.txt")
atomwords = ["awareness",
         "registration",
         "spread",
         "donation",
         "misunderstanding",
         "fear",
         "cost",
         "time",
         "cultural",
         "feeling",
         "rushed",
         "beliefs"]

filelist = read_data("bone-marrow-docs.txt")
outfile = open("fix_bone-marrow_words.txt",'w')

"""
Build the hash
"""

atomizedwordhash = {}
for filename in filelist:
    
    docwords = open(filename).read().split(" ") #read in the doc's words
    
    # iterate over the words
    for word in docwords:
        atomizedword = ""
        if word in messedupwords: #if it's a messed up word     
            # build the "atomized"
            for atomword in atomwords:
                if atomword in word:
                    atomizedword = atomizedword + atomword + " "
                    
        if atomizedword != "":
            atomizedwordhash[word] = atomizedword
    
    # print out the mappings - this part is expendable
    if len(atomizedwordhash) > 0:
        for key in atomizedwordhash:
            towrite = "%s,%s\n" %(key, atomizedwordhash[key])
            outfile.write(towrite)
outfile.close()

"""
Now rewrite the files
"""

for filename in filelist:
    docwords = open(filename).read().split(" ")
    doctext = ""
    for word in docwords:
        if word in messedupwords:
            doctext += atomizedwordhash[word]
        else:
            doctext = doctext + word + " "
    currentoutfile = open(filename,'w')
    doctext = doctext.strip()
    currentoutfile.write(doctext)
    currentoutfile.close()