#! /usr/bin/python
#

from sys import argv
from scipy.stats.stats import pearsonr
import numpy
import os

"""
first, compute cosines vs challenge brief for all concepts and inspirations
write to csv file - do the pandas stuff later

store in a list of dicts, like so:
data = [{"name": <name>, "challenge": <challenge>, "type": <type>, "cosine": <cosine>},{} etc. ]

make it into a data frame
frame = DataFrame(data)

now we can summarize by the various columns

for item in 

"""