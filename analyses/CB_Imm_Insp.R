# lme4 for multilevel, arm for various auxiliary computing and graphing functions
library(lme4)
library(arm)

#load the data
path = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControls_n707.csv"
data = read.csv(path,header=TRUE,sep=',')
attach(data)

#fully unconditional model
fitLRnull = glm(shortlist ~ 1, data=data, family=binomial)
fitLR = glm(shortlist ~ insp_dist_z_insp_mean + comments_preshortlist + num_shortlisted_sources, data=data, family=binomial)
summary(fitLR)

anova(fitLR,test='Chisq') #tests for each predictor
nagR2(707,logLik(fitLRnull)[1],logLik(fitLR)[1]) #Naglkerke R2
-2*(logLik(fitLRnull)[1]-logLik(fitLR)[1]) #Likelihood ratio
1-pchisq(-2*(fitLRnull.LL-fitLR.LL),3) #Likelihood ratio
# confidence intervals

# Naglkerke R2
nagR2 = function(n, nullLike, modelLike)
{
  lr = -2*(nullLike-modelLike) #likelihood ratio
  coxR2 = 1-exp(-lr/n) #Cox and Snell R2
  R2max = 1-exp(nullLike/n) #max R2 for scaling on 0 to 1 scale
  return(coxR2/R2max)
}

# Graph the logistic regression
curve(invlogit(fitLR$coef[1] + fitLR$coef[2]*x + fitLR$coef[3]*mean(data$comments_preshortlist) + fitLR$coef[4]*mean(data$num_shortlisted_sources)), 
      -2, 1, ylim=c(-.01,.4),
     xlim=c(-2,1), xaxt="n", xaxs="i", mgp=c(2,.5,0),
     ylab="Pr (Shortlist vote)", xlab="Mean inspiration distance (normalized)", lwd=1)
axis(1, -2:1, mgp=c(2,.5,0))
mtext("(low)", 1, 1.5, at=-5, adj=.5)
mtext("(high)", 1, 1.5, at=2, adj=.5)
#points(insp_dist_z_insp_mean, jitter(shortlist, .08), pch=19, cex=1, col="#00000032")

#curve(invlogit(fitLR$coef[1] + fitLR$coef[2]*x), -5.5, 2.5, ylim=c(-.01,1.01),
#       xlim=c(-5.5,2.5), xaxt="n", xaxs="i"), mgp=c(2,.5,0),
#       ylab="Pr (Shortlist)", xlab="Mean inspiration distance", lwd=1)
#for(j in 1:20){
#  curve (invlogit(sim.LR$coef[j,1] + sim.LR$coef[j,2]*x), col="gray", lwd=.5, add=T)
#}
#curve(invlogit(fitLR$coef[1] + fitLR$coef[2]*x), add=T)
#sim.LR <- sim(fitLR)

#fully unconditional challenge-nestedcoef
fitML.chall.null = glmer(shortlist ~ 1 + (1|challenge), data=data, family=binomial)
summary(fitML.chall.null)

#random intercepts varying by challenge
fitML.chall.RI = glmer(shortlist ~ 1 + insp_dist_z_insp_mean + (insp_dist_z_insp_mean|challenge) + comments_preshortlist + num_shortlisted_sources, data=data, family=binomial)
summary(fitML.chall.RI)

#control only
fitLRcontrol = glm(shortlist ~ comments_preshortlist + num_shortlisted_sources, data=data, family=binomial)
summary(fitLRcontrol)

#drop num shortlisted
fitLRnosls = glm(shortlist ~ comments_preshortlist + insp_dist_z_insp_mean, data=data, family=binomial)
anova(fitLRnosls,fitLR, test='LRT')

#random intercepts varying by challenge
fitML.chall.full.RI = glmer(shortlist ~ 1 + (1|challenge) + insp_dist_z_insp_mean + (insp_dist_z_insp_mean|challenge) + comments_preshortlist + num_shortlisted_sources, data=data, family=binomial)
summary(fitML.chall.full.RI)