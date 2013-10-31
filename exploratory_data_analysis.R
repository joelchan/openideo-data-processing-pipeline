#load the ggplot2 library
library(ggplot2) 

#define where the data file lives
file = "/Users/jchan/Desktop/extsources.csv"

#read in the data
data = read.csv(file,header=T,sep=",")