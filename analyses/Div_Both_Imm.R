# lme4 for multilevel, arm for various auxiliary computing and graphing functions
library(lme4)
library(arm)

#load the data
path = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControlsAndDiversity_n813.csv"
data.div = read.csv(path,header=TRUE,sep=',')
attach(data.div)

######## SINGLE-LEVEL ########

# null level-1 model
fitLR.div.null = glm(shortlist ~ 1, data=data.div, family=binomial)
summary(fitLR.div.null)

# controls
fitLR.div.controls = glm(shortlist ~ num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitLR.div.controls)

# both_div_min
fitLR.div.min = glm(shortlist ~ both_div_min + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitLR.div.min)
anova(fitLR.div.null, fitLR.div.controls, fitLR.div.min, test='LRT')

# both_div_max
fitLR.div.max = glm(shortlist ~ both_div_max + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitLR.div.max)
anova(fitLR.div.null, fitLR.div.controls, fitLR.div.max, test='LRT')

# both_div_mean
fitLR.div.mean = glm(shortlist ~ both_div_mean + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitLR.div.mean)
anova(fitLR.div.null, fitLR.div.controls, fitLR.div.mean, test='LRT')

# both_div_mean with quadratic
both_div_mean.sq = both_div_mean^2
fitLR.div.mean.sq = glm(shortlist ~ both_div_mean + both_div_mean.sq + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitLR.div.mean.sq)
anova(fitLR.div.null, fitLR.div.controls, fitLR.div.mean, fitLR.div.mean.sq, test='LRT')

# both_div_sd
fitLR.div.null.small = glm(shortlist ~ 1, data=data.div.sd, family=binomial)
fitLR.div.controls.small = glm(shortlist ~ num_shortlisted_sources + comments_preshortlist, data=data.div.sd, family=binomial)
fitLR.div.sd = glm(shortlist ~ both_div_sd + num_shortlisted_sources + comments_preshortlist, data=data.div.sd, family=binomial)
summary(fitLR.div.sd)
anova(fitLR.div.null.small, fitLR.div.controls.small, fitLR.div.sd, test='LRT')
anova(fitLR.div.null.small, fitLR.div.sd, test='LRT')
confint(fitLR.div.sd, method='Wald')

# both_div_sd ln, with quadratic
both_div_sd.ln = log(data.div.sd$both_div_sd)
both_div_sd.ln.sq = both_div_sd.ln^2
fitLR.div.sd.sq = glm(shortlist ~ both_div_sd.ln + both_div_sd.ln.sq + num_shortlisted_sources + comments_preshortlist, data=data.div.sd, family=binomial)
summary(fitLR.div.sd.sq)
anova(fitLR.div.null.small, fitLR.div.sd, fitLR.div.sd.sq, test='LRT')

######## MULTILEVEL AUTHOR ########

# fully unconditional
fitML.div.authors.null = glmer(shortlist ~ 1 + (1|authorURL), data=data.div, family=binomial)
summary(fitML.div.authors.null)

# controls
fitML.div.authors.controls = glmer(shortlist ~ 1 + (1|authorURL) + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitML.div.authors.controls)
anova(fitML.div.authors.null,fitML.div.authors.controls, test='LRT')

# both_div_mean
fitML.div.authors.mean = glmer(shortlist ~ 1 + (1|authorURL) + both_div_mean + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitML.div.authors.mean)
anova(fitML.div.authors.null,fitML.div.authors.controls, fitML.div.authors.mean, test='LRT')

# both_div_sd
fitML.div.authors.null.small = glmer(shortlist ~ 1 + (1|authorURL), data=data.div.sd, family=binomial)
fitML.div.authors.control.small = glmer(shortlist ~ 1 + (1|authorURL) + num_shortlisted_sources + comments_preshortlist, data=data.div.sd, family=binomial)
fitML.div.authors.sd = glmer(shortlist ~ 1 + (1|authorURL) + both_div_sd + num_shortlisted_sources + comments_preshortlist, data=data.div.sd, family=binomial)
summary(fitML.div.authors.sd)
anova(fitML.div.authors.null.small,fitML.div.authors.control.small, fitML.div.authors.sd, test='LRT')

######## MULTILEVEL CHALLENGE ########

# fully unconditional
fitML.div.chall.null = glmer(shortlist ~ 1 + (1|challenge), data=data.div, family=binomial)
summary(fitML.div.chall.null)

# controls
fitML.div.chall.controls = glmer(shortlist ~ 1 + (1|challenge) + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitML.div.chall.controls)
anova(fitML.div.chall.null,fitML.div.chall.controls, test='LRT')

# both_div_mean RI
fitML.div.chall.mean = glmer(shortlist ~ both_div_mean + (both_div_mean|challenge) + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitML.div.chall.mean)
anova(fitML.div.chall.null,fitML.div.chall.controls, fitML.div.chall.mean, test='LRT')

# both_div_mean fixed
fitML.div.chall.mean.fixed = glmer(shortlist ~ 1 + (1|challenge) + both_div_mean + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitML.div.chall.mean.fixed)
anova(fitML.div.chall.null,fitML.div.chall.controls, fitML.div.chall.mean.fixed, test='LRT')

# both_div_sd RI
fitML.div.chall.null.small = glmer(shortlist ~ 1 + (1|challenge), data=data.div.sd, family=binomial)
fitML.div.chall.control.small = glmer(shortlist ~ 1 + (1|challenge) + num_shortlisted_sources + comments_preshortlist, data=data.div.sd, family=binomial)
fitML.div.chall.sd = glmer(shortlist ~ both_div_sd + (both_div_sd|challenge) + num_shortlisted_sources + comments_preshortlist, data=data.div.sd, family=binomial)
summary(fitML.div.chall.sd)
anova(fitML.div.chall.null.small,fitML.div.chall.control.small, fitML.div.chall.sd, test='LRT')

# both_div_sd fixed
fitML.div.chall.sd.fixed = glmer(shortlist ~ 1 + (1|challenge) + both_div_sd + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitML.div.chall.sd.fixed)
anova(fitML.div.chall.null,fitML.div.chall.controls, fitML.div.chall.sd.fixed, test='LRT')

# both_div_sd fixed plus quadratic
both_div_sd.sq = both_div_sd^2
fitML.div.chall.sd.sq.fixed = glmer(shortlist ~ 1 + (1|challenge) + both_div_sd + both_div_sd.sq + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitML.div.chall.sd.sq.fixed)
anova(fitML.div.chall.null,fitML.div.chall.controls, fitML.div.chall.sd.sq.fixed, test='LRT')

# both_div_sd.ln fixed plus quadratic
fitML.div.chall.sd.ln.sq.fixed = glmer(shortlist ~ 1 + (1|challenge) + both_div_sd.ln + both_div_sd.ln.sq + num_shortlisted_sources + comments_preshortlist, data=data.div, family=binomial)
summary(fitML.div.chall.sd.ln.sq.fixed)
anova(fitML.div.chall.null,fitML.div.chall.controls, fitML.div.chall.sd.ln.sq.fixed, test='LRT')