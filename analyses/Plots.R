library(ggplot2)
library(Hmisc)
library(dplyr)

#### Make the summarized df ####

data.var.k400t60$bin_meanDist4 <- cut2(data.var.k400t60$insp_dist_z_insp_mean, g=4)

# summarize the data for the bins
summarized <- data.var.k400t60 %.% 
  group_by(bin_meanDist4) %.% 
  summarise(propShortlist=mean(shortlist), 
            meanVal=mean(insp_dist_z_insp_mean),
            sdVal=sd(insp_dist_z_insp_mean),
            n=length(shortlist))

# compute standard errors
summarized$error_propShortlist <- sqrt(summarized$propShortlist*(1-summarized$propShortlist)/summarized$n)
summarized$error_meanVal <- summarized$sdVal/sqrt(summarized$n)

#### Make the predicted df ####
xFake = seq(-1.5,1,.05)
yhat = 1/(1+exp(-(fixef(fit.dist.mean)[1] + 
                    fixef(fit.dist.mean)[2]*0.51 + 
                    fixef(fit.dist.mean)[3]*8.43 + 
                    fixef(fit.dist.mean)[4]*xFake + 
                    fixef(fit.dist.mean)[5]*xFake^2))))
fitted = data.frame(xFake,yhat)

#### Plot it! ####

plot <- ggplot(summarized) + 
  geom_errorbar(mapping=aes(x=meanVal, ymin=propShortlist-1.95* error_propShortlist, ymax=propShortlist+1.95* error_propShortlist),width=0.0) + 
  geom_errorbarh(aes(x=meanVal,y=propShortlist,xmin=meanVal-1.95*error_meanVal, xmax=meanVal+1.95* error_meanVal),height=0.0) + 
  geom_point(mapping=aes(x=meanVal,y=propShortlist), size=3, shape=21, fill="white") + 
  geom_line(data=fitted,aes(x=xFake,y=yhat)) + #fitted line
  labs(x="Mean distance",y="Pr(shortlist)") + 
  scale_x_continuous(breaks=seq(-1.5,1,.5),limits=c(-1.5,1)) + 
  scale_y_continuous(breaks=seq(0,.3,.1),limits=c(0,.3)) + 
  theme_bw()