# lme4 for multilevel, arm for various auxiliary computing and graphing functions
library(lme4)
library(arm)

#load the data
path = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControls_n707.csv"
data = read.csv(path,header=TRUE,sep=',')
data.insp.imm <- subset(data, insp_dist_count > 0) # grab only cases wiht at least one inspiration cited

### IGNORING NESTING ###

# null model
fitLRnull = glm(shortlist ~ 1, data=data.insp.imm, family=binomial)
summary(fitLRnull)

# controls
fitLRcontrol = glm(shortlist ~ comments_preshortlist + num_shortlisted_sources, data=data.insp.imm, family=binomial)
summary(fitLRcontrol)

# add MEAN dist
fitLRfull.mean = glm(shortlist ~ insp_dist_z_insp_mean + comments_preshortlist + num_shortlisted_sources, data=data.insp.imm, family=binomial)
summary(fitLRfull.mean)
anova(fitLRfull.mean,fitLRcontrol,fitLR,test='LRT') # LRT

# add MAX dist (separate model, not nested in mean)
fitLRfull.max = glm(shortlist ~ insp_dist_z_insp_max + comments_preshortlist + num_shortlisted_sources, data=data.insp.imm, family=binomial)
summary(fitLRfull.max)
anova(fitLRfull.mean,fitLRcontrol,fitLR,test='LRT') # LRT

### CROSS-CLASSIFIED ###

# null
fitML.null = glmer(shortlist ~ 1 + (1|challenge) + (1|authorURL), data=data.insp.imm, family=binomial)
summary(fitML.null)

# control
fitML.control = glmer(shortlist ~ 1 + (1|challenge) + (1|authorURL) + comments_preshortlist + num_shortlisted_sources, data=data.insp.imm, family=binomial)
summary(fitML.control)

# MEAN dist fixed slope
fitML.full.mean.fix = glmer(shortlist ~ 1 + (1|challenge) + (1|authorURL) + insp_dist_z_insp_mean + comments_preshortlist + num_shortlisted_sources, data=data.insp.imm, family=binomial)
summary(fitML.full.mean.fix)

# MEAN dist random slope
fitML.full.mean.ran = glmer(shortlist ~ 1 + (insp_dist_z_insp_mean |challenge) + (1|authorURL) + insp_dist_z_insp_mean + comments_preshortlist + num_shortlisted_sources, data=data.insp.imm, family=binomial)
summary(fitML.full.mean.ran)
anova(fitML.null,fitML.control, fitML.full.mean.fix, fitML.full.mean.ran,test='LRT')

# MAX dist fixed slope
fitML.full.max.fix = glmer(shortlist ~ 1 + (1|challenge) + (1|authorURL) + insp_dist_z_insp_max + comments_preshortlist + num_shortlisted_sources, data=data.insp.imm, family=binomial)

# mean dist random slope
fitML.full.max.ran = glmer(shortlist ~ 1 + (insp_dist_z_insp_max |challenge) + (1|authorURL) + insp_dist_z_insp_max + comments_preshortlist + num_shortlisted_sources, data=data.insp.imm, family=binomial)
summary(fitML.full.mean.ran)
anova(fitML.null,fitML.control, fitML.full.max.fix, fitML.full.max.ran,test='LRT')
