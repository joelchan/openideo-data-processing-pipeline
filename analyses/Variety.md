OpenIDEO Variety Analysis (K=400[6],t=60)
========================================================

Load data and packages

```
## Loading required package: lattice
## Loading required package: Matrix
```


# Descriptives first
## Descriptive statistics

```r
describe(data.var.k400t60[c("shortlist", "comments_preshortlist", "num_shortlisted_sources", 
    "both_numSources", "both_sourceVariety")])
```

```
##                         var    n mean    sd median trimmed  mad min    max
## shortlist                 1 1182 0.13  0.34    0.0    0.04 0.00 0.0   1.00
## comments_preshortlist     2 1182 7.39  8.48    5.0    5.83 4.45 0.0  67.00
## num_shortlisted_sources   3 1182 0.53  0.97    0.0    0.31 0.00 0.0  11.00
## both_numSources           4 1182 5.58 13.81    3.0    3.50 2.97 1.0 295.00
## both_sourceVariety        5 1182 3.11  0.78    3.1    3.10 0.91 1.1   5.31
##                          range  skew kurtosis   se
## shortlist                 1.00  2.14     2.58 0.01
## comments_preshortlist    67.00  2.56     9.58 0.25
## num_shortlisted_sources  11.00  3.55    22.87 0.03
## both_numSources         294.00 13.15   226.40 0.40
## both_sourceVariety        4.21  0.10    -0.72 0.02
```


## Intercorrelations

```r
library(Hmisc)  # watch out, there is a conflicting named function 'describe' - we want the one from psych
```

```
## Loading required package: grid
## Loading required package: survival
## Loading required package: splines
## Loading required package: Formula
## 
## Attaching package: 'Hmisc'
## 
## The following object is masked from 'package:psych':
## 
##     describe
## 
## The following objects are masked from 'package:base':
## 
##     format.pval, round.POSIXt, trunc.POSIXt, units
```

```r
rcorr(as.matrix(data.var.k400t60[c("shortlist", "comments_preshortlist", "num_shortlisted_sources", 
    "both_numSources", "both_sourceVariety")]))
```

```
##                         shortlist comments_preshortlist
## shortlist                    1.00                  0.34
## comments_preshortlist        0.34                  1.00
## num_shortlisted_sources      0.15                  0.15
## both_numSources              0.09                  0.21
## both_sourceVariety           0.09                  0.22
##                         num_shortlisted_sources both_numSources
## shortlist                                  0.15            0.09
## comments_preshortlist                      0.15            0.21
## num_shortlisted_sources                    1.00            0.23
## both_numSources                            0.23            1.00
## both_sourceVariety                         0.39            0.47
##                         both_sourceVariety
## shortlist                             0.09
## comments_preshortlist                 0.22
## num_shortlisted_sources               0.39
## both_numSources                       0.47
## both_sourceVariety                    1.00
## 
## n= 1182 
## 
## 
## P
##                         shortlist comments_preshortlist
## shortlist                         0.0000               
## comments_preshortlist   0.0000                         
## num_shortlisted_sources 0.0000    0.0000               
## both_numSources         0.0015    0.0000               
## both_sourceVariety      0.0029    0.0000               
##                         num_shortlisted_sources both_numSources
## shortlist               0.0000                  0.0015         
## comments_preshortlist   0.0000                  0.0000         
## num_shortlisted_sources                         0.0000         
## both_numSources         0.0000                                 
## both_sourceVariety      0.0000                  0.0000         
##                         both_sourceVariety
## shortlist               0.0029            
## comments_preshortlist   0.0000            
## num_shortlisted_sources 0.0000            
## both_numSources         0.0000            
## both_sourceVariety
```


# Models
# Null and control

Null

```r
fit.var.k400.t60.both.null = glmer(shortlist ~ (1 | authorURL) + (1 | challenge_x), 
    data = data.var.k400t60, family = binomial)
summary(fit.var.k400.t60.both.null)
```

```
## Generalized linear mixed model fit by maximum likelihood ['glmerMod']
##  Family: binomial ( logit )
## Formula: shortlist ~ (1 | authorURL) + (1 | challenge_x) 
##    Data: data.var.k400t60 
## 
##      AIC      BIC   logLik deviance 
##    885.7    900.9   -439.8    879.7 
## 
## Random effects:
##  Groups      Name        Variance Std.Dev.
##  authorURL   (Intercept) 0.461    0.679   
##  challenge_x (Intercept) 0.511    0.715   
## Number of obs: 1182, groups: authorURL, 574; challenge_x, 12
## 
## Fixed effects:
##             Estimate Std. Error z value Pr(>|z|)    
## (Intercept)    -1.84       0.23   -7.99  1.3e-15 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```


Test sig. of the random effects

```r
fit.var.k400.t60.both.null.authorsOnly = glmer(shortlist ~ (1 | authorURL), 
    data = data.var.k400t60, family = binomial)
fit.var.k400.t60.both.null.challOnly = glmer(shortlist ~ (1 | challenge_x), 
    data = data.var.k400t60, family = binomial)
anova(fit.var.k400.t60.both.null.authorsOnly, fit.var.k400.t60.both.null, test = "LRT")  # is the challenge random-effect sig?
```

```
## Data: data.var.k400t60
## Models:
## fit.var.k400.t60.both.null.authorsOnly: shortlist ~ (1 | authorURL)
## fit.var.k400.t60.both.null: shortlist ~ (1 | authorURL) + (1 | challenge_x)
##                                        Df AIC BIC logLik deviance Chisq
## fit.var.k400.t60.both.null.authorsOnly  2 926 936   -461      922      
## fit.var.k400.t60.both.null              3 886 901   -440      880  41.9
##                                        Chi Df Pr(>Chisq)    
## fit.var.k400.t60.both.null.authorsOnly                      
## fit.var.k400.t60.both.null                  1    9.6e-11 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

```r
anova(fit.var.k400.t60.both.null.challOnly, fit.var.k400.t60.both.null, test = "LRT")  # is the author random-effect sig?
```

```
## Data: data.var.k400t60
## Models:
## fit.var.k400.t60.both.null.challOnly: shortlist ~ (1 | challenge_x)
## fit.var.k400.t60.both.null: shortlist ~ (1 | authorURL) + (1 | challenge_x)
##                                      Df AIC BIC logLik deviance Chisq
## fit.var.k400.t60.both.null.challOnly  2 892 903   -444      888      
## fit.var.k400.t60.both.null            3 886 901   -440      880  8.76
##                                      Chi Df Pr(>Chisq)   
## fit.var.k400.t60.both.null.challOnly                     
## fit.var.k400.t60.both.null                1     0.0031 **
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```


Control

```r
fit.var.k400.t60.both.controls = glmer(shortlist ~ (1 | authorURL) + (1 | challenge_x) + 
    comments_preshortlist + num_shortlisted_sources + both_numSources, data = data.var.k400t60, 
    family = binomial)
summary(fit.var.k400.t60.both.controls)
```

```
## Generalized linear mixed model fit by maximum likelihood ['glmerMod']
##  Family: binomial ( logit )
## Formula: shortlist ~ (1 | authorURL) + (1 | challenge_x) + comments_preshortlist +      num_shortlisted_sources + both_numSources 
##    Data: data.var.k400t60 
## 
##      AIC      BIC   logLik deviance 
##    769.8    800.3   -378.9    757.8 
## 
## Random effects:
##  Groups      Name        Variance Std.Dev.
##  authorURL   (Intercept) 0.350    0.591   
##  challenge_x (Intercept) 0.699    0.836   
## Number of obs: 1182, groups: authorURL, 574; challenge_x, 12
## 
## Fixed effects:
##                          Estimate Std. Error z value Pr(>|z|)    
## (Intercept)             -2.908016   0.292717   -9.93   <2e-16 ***
## comments_preshortlist    0.106576   0.011389    9.36   <2e-16 ***
## num_shortlisted_sources  0.224707   0.087978    2.55    0.011 *  
## both_numSources          0.000177   0.005904    0.03    0.976    
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Correlation of Fixed Effects:
##             (Intr) cmmnt_ nm_sh_
## cmmnts_prsh -0.367              
## nm_shrtlst_ -0.175 -0.041       
## both_nmSrcs -0.009 -0.209 -0.119
```


LRT to compare against

```r
anova(fit.var.k400.t60.both.null, fit.var.k400.t60.both.controls, test = "LRT")
```

```
## Data: data.var.k400t60
## Models:
## fit.var.k400.t60.both.null: shortlist ~ (1 | authorURL) + (1 | challenge_x)
## fit.var.k400.t60.both.controls: shortlist ~ (1 | authorURL) + (1 | challenge_x) + comments_preshortlist + 
## fit.var.k400.t60.both.controls:     num_shortlisted_sources + both_numSources
##                                Df AIC BIC logLik deviance Chisq Chi Df
## fit.var.k400.t60.both.null      3 886 901   -440      880             
## fit.var.k400.t60.both.controls  6 770 800   -379      758   122      3
##                                Pr(>Chisq)    
## fit.var.k400.t60.both.null                   
## fit.var.k400.t60.both.controls     <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```


Confidence intervals

```r
confint.merMod(fit.var.k400.t60.both.controls, method = "Wald")
```

```
##                            2.5 %   97.5 %
## (Intercept)             -3.48173 -2.33430
## comments_preshortlist    0.08425  0.12890
## num_shortlisted_sources  0.05227  0.39714
## both_numSources         -0.01140  0.01175
```


# For real

Now our first model with just variety

```r
fit.var.k400.t60.both.varLinear = glmer(shortlist ~ (1 | authorURL) + (1 | challenge_x) + 
    comments_preshortlist + num_shortlisted_sources + both_numSources + both_sourceVariety, 
    data = data.var.k400t60, family = binomial)
summary(fit.var.k400.t60.both.varLinear)
```

```
## Generalized linear mixed model fit by maximum likelihood ['glmerMod']
##  Family: binomial ( logit )
## Formula: shortlist ~ (1 | authorURL) + (1 | challenge_x) + comments_preshortlist +      num_shortlisted_sources + both_numSources + both_sourceVariety 
##    Data: data.var.k400t60 
## 
##      AIC      BIC   logLik deviance 
##    771.8    807.3   -378.9    757.8 
## 
## Random effects:
##  Groups      Name        Variance Std.Dev.
##  authorURL   (Intercept) 0.354    0.595   
##  challenge_x (Intercept) 0.704    0.839   
## Number of obs: 1182, groups: authorURL, 574; challenge_x, 12
## 
## Fixed effects:
##                         Estimate Std. Error z value Pr(>|z|)    
## (Intercept)             -3.04151    0.55414   -5.49    4e-08 ***
## comments_preshortlist    0.10632    0.01145    9.29   <2e-16 ***
## num_shortlisted_sources  0.21622    0.09279    2.33     0.02 *  
## both_numSources         -0.00040    0.00622   -0.06     0.95    
## both_sourceVariety       0.04562    0.16233    0.28     0.78    
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Correlation of Fixed Effects:
##             (Intr) cmmnt_ nm_sh_ bth_nS
## cmmnts_prsh -0.112                     
## nm_shrtlst_  0.189 -0.007              
## both_nmSrcs  0.283 -0.164  0.005       
## bth_srcVrty -0.848 -0.097 -0.326 -0.339
```


Confidence intervals

```r
confint.merMod(fit.var.k400.t60.both.varLinear, method = "Wald")
```

```
##                            2.5 %   97.5 %
## (Intercept)             -4.12760 -1.95542
## comments_preshortlist    0.08389  0.12876
## num_shortlisted_sources  0.03435  0.39809
## both_numSources         -0.01259  0.01179
## both_sourceVariety      -0.27254  0.36379
```


No real effect of variety, also confirmed by LRT that adding it to the model doesn't really improve our fit to the data

```r
anova(fit.var.k400.t60.both.controls, fit.var.k400.t60.both.varLinear, test = "LRT")
```

```
## Data: data.var.k400t60
## Models:
## fit.var.k400.t60.both.controls: shortlist ~ (1 | authorURL) + (1 | challenge_x) + comments_preshortlist + 
## fit.var.k400.t60.both.controls:     num_shortlisted_sources + both_numSources
## fit.var.k400.t60.both.varLinear: shortlist ~ (1 | authorURL) + (1 | challenge_x) + comments_preshortlist + 
## fit.var.k400.t60.both.varLinear:     num_shortlisted_sources + both_numSources + both_sourceVariety
##                                 Df AIC BIC logLik deviance Chisq Chi Df
## fit.var.k400.t60.both.controls   6 770 800   -379      758             
## fit.var.k400.t60.both.varLinear  7 772 807   -379      758  0.08      1
##                                 Pr(>Chisq)
## fit.var.k400.t60.both.controls            
## fit.var.k400.t60.both.varLinear       0.78
```


Let's add a quadratic term now

```r
data.var.k400t60$both_sourceVariety.sq = data.var.k400t60$both_sourceVariety^2
fit.var.k400.t60.both.varQuadr = glmer(shortlist ~ (1 | authorURL) + (1 | challenge_x) + 
    comments_preshortlist + num_shortlisted_sources + both_numSources + both_sourceVariety + 
    both_sourceVariety.sq, data = data.var.k400t60, family = binomial)
summary(fit.var.k400.t60.both.varQuadr)
```

```
## Generalized linear mixed model fit by maximum likelihood ['glmerMod']
##  Family: binomial ( logit )
## Formula: shortlist ~ (1 | authorURL) + (1 | challenge_x) + comments_preshortlist +      num_shortlisted_sources + both_numSources + both_sourceVariety +      both_sourceVariety.sq 
##    Data: data.var.k400t60 
## 
##      AIC      BIC   logLik deviance 
##    770.9    811.5   -377.5    754.9 
## 
## Random effects:
##  Groups      Name        Variance Std.Dev.
##  authorURL   (Intercept) 0.270    0.519   
##  challenge_x (Intercept) 0.683    0.826   
## Number of obs: 1182, groups: authorURL, 574; challenge_x, 12
## 
## Fixed effects:
##                         Estimate Std. Error z value Pr(>|z|)    
## (Intercept)             -5.89262    1.81425   -3.25   0.0012 ** 
## comments_preshortlist    0.10660    0.01144    9.32   <2e-16 ***
## num_shortlisted_sources  0.23450    0.09196    2.55   0.0108 *  
## both_numSources          0.00644    0.00780    0.83   0.4087    
## both_sourceVariety       2.03262    1.18680    1.71   0.0868 .  
## both_sourceVariety.sq   -0.32846    0.19338   -1.70   0.0894 .  
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Correlation of Fixed Effects:
##             (Intr) cmmnt_ nm_sh_ bth_nS bth_sV
## cmmnts_prsh -0.125                            
## nm_shrtlst_ -0.059  0.008                     
## both_nmSrcs -0.434 -0.078  0.057              
## bth_srcVrty -0.978  0.083  0.078  0.491       
## bth_srcVrt.  0.950 -0.098 -0.125 -0.538 -0.990
```


Notice the very wide confidence intervals

```r
confint.merMod(fit.var.k400.t60.both.varQuadr, method = "Wald")
```

```
##                             2.5 %   97.5 %
## (Intercept)             -9.448481 -2.33676
## comments_preshortlist    0.084176  0.12902
## num_shortlisted_sources  0.054264  0.41473
## both_numSources         -0.008842  0.02173
## both_sourceVariety      -0.293465  4.35870
## both_sourceVariety.sq   -0.707466  0.05055
```


So there's a hint of a positive linear effect of variety with a deceleration function (basically an inverted-U effect).
BUT, it is marginal, and the model with these terms doesn't really fit better than control (the LRT is n.s., and the AIC is *slightly* larger)

```r
anova(fit.var.k400.t60.both.controls, fit.var.k400.t60.both.varQuadr, test = "LRT")
```

```
## Data: data.var.k400t60
## Models:
## fit.var.k400.t60.both.controls: shortlist ~ (1 | authorURL) + (1 | challenge_x) + comments_preshortlist + 
## fit.var.k400.t60.both.controls:     num_shortlisted_sources + both_numSources
## fit.var.k400.t60.both.varQuadr: shortlist ~ (1 | authorURL) + (1 | challenge_x) + comments_preshortlist + 
## fit.var.k400.t60.both.varQuadr:     num_shortlisted_sources + both_numSources + both_sourceVariety + 
## fit.var.k400.t60.both.varQuadr:     both_sourceVariety.sq
##                                Df AIC BIC logLik deviance Chisq Chi Df
## fit.var.k400.t60.both.controls  6 770 800   -379      758             
## fit.var.k400.t60.both.varQuadr  8 771 812   -377      755  2.93      2
##                                Pr(>Chisq)
## fit.var.k400.t60.both.controls           
## fit.var.k400.t60.both.varQuadr       0.23
```

