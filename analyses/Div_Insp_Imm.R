# lme4 for multilevel, arm for various auxiliary computing and graphing functions
library(lme4)
library(arm)

#load the data
path = "/Users/joelc/Dropbox/Research/dissertation/OpenIDEO/Pipeline/Challenge_and_High-level_Data/iPython intermediate inputs and outputs/ConceptLevel_AfterDistanceAndControlsAndDiversity_n456.csv"
data.div = read.csv(path,header=TRUE,sep=',')
data.div.insp <- subset(data.div,insp_dist_count > 1) # drop the single-insp and no-insp cases

# plot distribution of diversity
ggplot(data.div.insp, aes(insp_div_mean)) + geom_histogram(fill=NA,color="black") + theme_bw()

# scatterplot matrix
pairs(~shortlist+comments_preshortlist+num_shortlisted_sources+insp_dist_z_insp_mean+insp_div_mean,data=data.div.insp,
      panel=function(x,y){
        points(x,y)
        abline(lm(y~x),lty=2)
        lines(lowess(x,y))
        },
      diag.panel=function(x){
        par(new=T)
        hist(x,main="",axes=F)
        }
      )

### NULLS ###

# fully unconditional cross-classified
fit.div.insp.null = glmer(shortlist ~ (1|authorURL) + (1|challenge), data=data.div.insp, family=binomial)
summary(fit.div.insp.null)
confint.merMod(fit.div.insp.null,method='Wald')

# test sig. of variance components
# challenge
fit.div.insp.auth = glmer(shortlist ~ (1|authorURL), data=data.div.insp, family=binomial)
anova(fit.div.insp.auth,fit.div.insp.null,test='LRT') # yes, chisq(1) = 5.19, p = .01
# author
fit.div.insp.chall = glmer(shortlist ~ (1|challenge), data=data.div.insp, family=binomial)
anova(fit.div.insp.chall,fit.div.insp.null,test='LRT') # yes, chisq(1) = 4.41, p = .02

### CONTROLS ###

fit.div.insp.controls = glmer(shortlist ~ (1|authorURL) + (1|challenge) + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.controls)
confint.merMod(fit.div.insp.controls,method='Wald')
anova(fit.div.insp.null,fit.div.insp.controls,test='LRT') # yes, chisq(2) = 61.14, p < .001

### MEAN DIVERSITY ALONE ###
data.div.insp$insp_div_mean_rescaled <- data.div.insp$insp_div_mean*10 #rescale for easier interpretation of coefficient
fit.div.insp.divmean = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_div_mean_rescaled + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.divmean)
confint.merMod(fit.div.insp.divmean,method='Wald')
anova(fit.div.insp.controls,fit.div.insp.divmean,test='LRT') # add anything over control?

# quadratic?
data.div.insp$insp_div_mean_rescaled_sq <- data.div.insp$insp_div_mean^2
fit.div.insp.divmean.quadr = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_div_mean_rescaled + insp_div_mean_rescaled_sq + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.divmean.quadr)
confint.merMod(fit.div.insp.divmean.quadr,method='Wald')
anova(fit.div.insp.divmean,fit.div.insp.divmean.quadr,test='LRT')

# any problem variation?
fit.div.insp.divmean.RE = glmer(shortlist ~ (1|authorURL) + (insp_div_mean_rescaled|challenge) + insp_div_mean_rescaled + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.divmean.RE)
confint.merMod(fit.div.insp.divmean.RE,method='Wald')
anova(fit.div.insp.divmean,fit.div.insp.divmean.RE,test='LRT') 

# outlier influence
influence.div.insp.divmean = influence.ME(fit.div.insp.divmean,obs=TRUE) #drop individual cases, not higher-level units
dfbetas.divmean = dfbetas.estex(influence.div.insp.divmean,parameters='insp_div_mean')
boxplot(dfbetas.divmean,ylab="DFBETAS for mean diversity")

### REPEAT DISTANCE ###
# base
fit.div.insp.distmean = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_dist_z_insp_mean + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.distmean) # effect is in the same direction, of similar size, but with more noise (now "marginal")
confint.merMod(fit.div.insp.distmean,method='Wald') # 95% CI = [-0.91,0.07]

# add (control for?) diversity
fit.div.insp.distmean.divmean = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_dist_z_insp_mean + insp_div_mean_rescaled + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.distmean.divmean)
confint.merMod(fit.div.insp.distmean.divmean,method='Wald')

# not much point, but see if there's an interaction between distance and diversity? (bivariate linear r = ~.3)
data.div.insp$insp_distmeanXdivmean = data.div.insp$insp_dist_z_insp_mean * data.div.insp$insp_div_mean # create interaction term
fit.div.insp.distmean.divmean.inter = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_dist_z_insp_mean + insp_div_mean_rescaled + insp_distmeanXdivmean + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.distmean.divmean.inter)
confint.merMod(fit.div.insp.distmean.divmean.inter,method='Wald')

anova(fit.div.insp.controls,fit.div.insp.distmean,fit.div.insp.distmean.divmean, fit.div.insp.distmean.divmean.inter,test='LRT')

### MIN, MAX, SD ###

## min
data.div.insp$insp_div_min_rescaled <- data.div.insp$insp_div_min*10 #rescale for easier interpretation of coefficient
fit.div.insp.divmin = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_div_min_rescaled + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.divmin)

# min RE
fit.div.insp.divmin.RE = glmer(shortlist ~ (1|authorURL) + (insp_div_min_rescaled|challenge) + insp_div_min_rescaled + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.divmin.RE)

## max
data.div.insp$insp_div_max_rescaled <- data.div.insp$insp_div_max*10 #rescale for easier interpretation of coefficient
fit.div.insp.divmax = glmer(shortlist ~ (1|authorURL) + (1|challenge) + insp_div_max_rescaled + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.divmax)

# max RE
fit.div.insp.divmax.RE = glmer(shortlist ~ (1|authorURL) + (insp_div_max_rescaled|challenge) + insp_div_max_rescaled + num_shortlisted_sources + comments_preshortlist, data=data.div.insp, family=binomial)
summary(fit.div.insp.divmax.RE)

#########

data.div.insp$dfBETAdivmean <- influence.stats[,2]
ggplot(data.div.insp,aes(x=challenge,y=dfBETAdivmean)) + geom_boxplot() + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1)) + ylim(-1,1)

# quick check if votes gives us different results
summary(glmer(votes ~ (1|challenge) + (1|authorURL) + insp_dist_z_insp_mean + comments_preshortlist + num_shortlisted_sources, data=data.div.insp,family=poisson))
# not really. but there is a high degree of overdispersion (~16!)
var(data.div.insp$insp_div_mean)/mean(data.div.insp$insp_div_mean)

# get sense of standardized betas
data.div.insp$insp_div_mean_z <- scale(data.div.insp$insp_div_mean,scale=TRUE,center=TRUE)
data.div.insp$feedback_z <- scale(data.div.insp$comments_preshortlist,scale=TRUE,center=TRUE)
data.div.insp$shortSource_z <- scale(data.div.insp$num_shortlisted_sources,scale=TRUE,center=TRUE)
summary(glmer(shortlist ~ (1|challenge) + (1|authorURL) + insp_div_mean_z + feedback_z + shortSource_z, data=data.div.insp, family=binomial))
confint.merMod(glmer(shortlist ~ (1|challenge) + (1|authorURL) + insp_div_mean_z + feedback_z + shortSource_z, data=data.div.insp, family=binomial),method='Wald')