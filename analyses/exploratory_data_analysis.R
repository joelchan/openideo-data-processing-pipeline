#load the ggplot2 library
library(ggplot2) 

#define where the data file lives
file = "/Users/jchan/Desktop/extsources.csv"

#read in the data
data = read.csv(file,header=T,sep=",")

chart = ggplot(data, aes(x=LDA, y=human)) +
  geom_point(shape=1, size=1.5) +
  geom_smooth(method=lm) +
  theme(panel.grid.minor=element_blank(), panel.grid.major=element_blank(), panel.background = element_rect(fill='white',colour='grey'))

ggsave(file="/Users/joelc/Desktop/LDA-ewaste.png",plot=graph, width=6, height=4)