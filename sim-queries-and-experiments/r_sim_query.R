# this package has the cosine function. 
library(lsa) 

d = 6908 #number of documents
k = 90 #number of topics

## Read in the data
path = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/GetCTM/ctm-dist/CFgt1_DFgt50_K90/final-lambda.dat"
lambda = matrix(scan(path),byrow=TRUE,nrow=d,ncol=k)

## Transpose to prepare for sim query
lambda.t = t(lambda)
anchor = lambda.t[,1003]
cosines = vector()
for (i in 1110:1308) {
  cosine = cosine(anchor,lambda.t[,i])
  cosines = c(cosines, cosine)
  print(cosine)
}
write.csv(cosines,file = "/Users/jchan/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/Validation/CTM_e-waste_insp-cosines.csv")