# lme4 for multilevel, arm for various auxiliary computing and graphing functions
library(lme4)
library(arm)

#load the data
path = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControlsAndDiversity_n456.csv"
data.div456 = read.csv(path,header=TRUE,sep=',')
attach(data.div456)

# plot distribution of diversity
ggplot(data.div456, aes(insp_div_mean)) + geom_histogram(fill=NA,color="black") + theme_bw()

# scatterplot matrix
pairs(~shortlist+comments_preshortlist+num_shortlisted_sources+insp_dist_z_insp_mean+insp_div_mean,data=data.div456)

### NULLS ###

# fully unconditional cross-classified
model.div456.null = glmer(shortlist ~ (1|authorURL) + (1|challenge), data=data.div456, family=binomial)
summary(model.div456.null)

# test sig. of variance components
# challenge
model.div456.auth = glmer(shortlist ~ (1|authorURL), data=data.div456, family=binomial)
anova(model.div456.auth,model.div456.null,test='LRT') # yes, chisq(1) = 5.19, p = .01
# author
model.div456.chall = glmer(shortlist ~ (1|challenge), data=data.div456, family=binomial)
anova(model.div456.chall,model.div456.null,test='LRT') # yes, chisq(1) = 4.41, p = .02

### CONTROLS ###

model.div456.controls = glmer(shortlist ~ (1|authorURL) + (1|challenge) + num_shortlisted_sources + comments_preshortlist, data=data.div456, family=binomial)
summary(model.div456.controls)
confint.merMod(model.div456.controls,method='Wald')
anova(model.div456.null,model.div456.controls,test='LRT') # yes, chisq(2) = 61.14, p < .001

### REPEAT DISTANCE ###
# base
model.div456.distmean = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_dist_z_insp_mean + num_shortlisted_sources + comments_preshortlist, data=data.div456, family=binomial)
summary(model.div456.distmean) # effect is in the same direction, of similar size, but with more noise (now "marginal")
confint.merMod(model.div456.distmean,method='Wald') # 95% CI = [-0.91,0.07]

# add (control for?) diversity
model.div456.distmean.divmean = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_dist_z_insp_mean + insp_div_mean + num_shortlisted_sources + comments_preshortlist, data=data.div456, family=binomial)
summary(model.div456.distmean.divmean)
confint.merMod(model.div456.distmean.divmean,method='Wald')

# not much point, but see if there's an interaction between distance and diversity? (bivariate linear r = ~.3)
model.div456.distmean.divmean.inter = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_dist_z_insp_mean + insp_div_mean + insp_dist_z_insp_mean*insp_div_mean + num_shortlisted_sources + comments_preshortlist, data=data.div456, family=binomial)
summary(model.div456.distmean.divmean.inter)
confint.merMod(model.div456.distmean.divmean.inter,method='Wald')

# could it be because of a mismatch in standardization? 
model.div456.distmeanRAW.divmean = glmer(shortlist ~ (1|challenge) + (1|authorURL) + insp_dist_raw_mean + insp_div_mean + comments_preshortlist + num_shortlisted_sources, data=data.div456,family=binomial)
summary(model.div456.distmean.divmean.inter) # no, but also be careful because correlation between mean raw distance and mean div is much higher (linear r = ~.6)
confint.merMod(model.div456.distmean.divmean.inter,method='Wald')

anova(model.div456.null,model.div456.controls,model.div456.distmean,model.div456.distmean.divmean,model.div456.distmean.divmean.inter,test='LRT')

### DIVERSITY ALONE ###
model.div456.divmean = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_div_mean + num_shortlisted_sources + comments_preshortlist, data=data.div456, family=binomial)
summary(model.div456.divmean) ## hmm, sign flips pretty big! where it was ever so slightly positive before, div_mean now is pretty strongly negative. collinearity??
confint.merMod(model.div456.divmean,method='Wald')

# any problem variation?
model.div456.divmean.RE = glmer(shortlist ~ (1|authorURL) + (insp_div_mean|challenge) + insp_div_mean + num_shortlisted_sources + comments_preshortlist, data=data.div456, family=binomial)
summary(model.div456.divmean.RE)
confint.merMod(model.div456.divmean.RE,method='Wald')
anova(model.div456.divmean,model.div456.divmean.RE,test='LRT') # no, AIC goes up (from 338.97 to 340.32), chisq(2) = 2.65, p = 0.2664/2 = .13

### ROBUSTNESS/SENSITIVITY ###

# guess at outlier influence
model.div456.divmean.single = glm(shortlist ~ insp_div_mean + num_shortlisted_sources + comments_preshortlist, data=data.div456, family=binomial)
summary(model.div456.divmean.single)
confint(model.div456.divmean.single,method='Wald')
inf.model.div456.divmean.single = influence.measures(model.div456.divmean.single)
inf.model.div456.divmean.single

# plot DFBETA for div mean (boxplot) by challenge
influence.stats <- inf.model.div456.divmean.single$infmat

data.div456$dfBETAdivmean <- influence.stats[,2]
ggplot(data.div456,aes(x=challenge,y=dfBETAdivmean)) + geom_boxplot() + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1)) + ylim(-1,1)

# quick check if votes gives us different results
summary(glmer(votes ~ (1|challenge) + (1|authorURL) + insp_dist_z_insp_mean + comments_preshortlist + num_shortlisted_sources, data=data.div456,family=poisson))
# not really. but there is a high degree of overdispersion (~16!)
var(data.div456$insp_div_mean)/mean(data.div456$insp_div_mean)

# get sense of standardized betas
data.div456$insp_div_mean_z <- scale(data.div456$insp_div_mean,scale=TRUE,center=TRUE)
data.div456$feedback_z <- scale(data.div456$comments_preshortlist,scale=TRUE,center=TRUE)
data.div456$shortSource_z <- scale(data.div456$num_shortlisted_sources,scale=TRUE,center=TRUE)
summary(glmer(shortlist ~ (1|challenge) + (1|authorURL) + insp_div_mean_z + feedback_z + shortSource_z, data=data.div456, family=binomial))
confint.merMod(glmer(shortlist ~ (1|challenge) + (1|authorURL) + insp_div_mean_z + feedback_z + shortSource_z, data=data.div456, family=binomial),method='Wald')

