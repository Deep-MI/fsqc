# libraries
library(data.table)
library(lme4)
library(ModelGood)
library(boot)
library(Epi)

# preprocess data
m<-droplevels(subset(m,subset=Sex!="X"))
m$Research.Group.3<-factor(
    ifelse(m$Research.Group=="CN"|m$Research.Group=="SMC","Ctrl",ifelse(m$Research.Group=="LMCI"|m$Research.Group=="EMCI"|m$Research.Group=="MCI","MCI",ifelse(m$Research.Group=="AD","AD",NA))),
    levels=c("Ctrl","MCI","AD")
    )

# calculate vars
m$mayo.SERIES_QUALITY_BIN<-m$mayo.SERIES_QUALITY>2

# read QC data
q<-read.csv("/groups/ag-reuter/projects/adni-qc/quality_checker_v2.csv")

# merge with quality checker table
m5<-m
m<-merge(m,q,by.x="Image.ID",by.y="Subject",all.x=T)
m<-droplevels(m)

# set order
setorder(m,Subject.ID,Visit,mprage.SeriesID,mprage.ImageUID)

# select one (arbitrary) image per visit
m$Type.Vis.Subj.N<-ave(as.character(m$Type),m$Subject.ID,m$Visit,FUN=function(x){length(x)})
m$Type.Vis.Subj.Idx<-ave(as.character(m$Type),m$Subject.ID,m$Visit,FUN=function(x){c(1:length(x))})
m6<-m
m<-subset(m,subset=Type.Vis.Subj.Idx==1)
m<-droplevels(m)

# compute longitudinal GLMM
m8<-m
m<-subset(m,subset=!is.na(mayo.SERIES_QUALITY_BIN))
m<-droplevels(m)
m$Age.At.Baseline<-ave(m$Age,m$Subject.ID,FUN=min)
m$Time.From.Baseline<-m$Age-ave(m$Age,m$Subject.ID,FUN=min)
summary(glmer(mayo.SERIES_QUALITY_BIN~scale(Age,scale=F)+(1|Subject.ID),data=m,family=binomial(link="logit")))
summary(glmer(mayo.SERIES_QUALITY_BIN~Time.From.Baseline+scale(Age.At.Baseline,scale=F)+(1|Subject.ID),data=m,family=binomial(link="logit")))

# select one (first) visit per subject
m$mprage.ScanDate<-as.Date(m$mprage.ScanDate,format="%Y-%m-%d")
m$Visit.Num<-ave(as.numeric(m$mprage.ScanDate),m$Subject.ID,FUN=function(x){rank(x)})

m7<-m
m<-subset(m,subset=Visit.Num==1)
m<-droplevels(m)

# get stats
table(m$mayo.SERIES_QUALITY,useNA="i")

# compute models
summary(glm(mayo.SERIES_QUALITY_BIN~Age,data=m,family=binomial(link="logit")))
summary(glm(mayo.SERIES_QUALITY_BIN~Sex,data=m,family=binomial(link="logit")))
summary(glm(mayo.SERIES_QUALITY_BIN~Research.Group.3,data=m,family=binomial(link="logit")))

summary(glm(mayo.SERIES_QUALITY_BIN~Holes_LH,data=m,family=binomial(link="logit")))
summary(glm(mayo.SERIES_QUALITY_BIN~Holes_RH,data=m,family=binomial(link="logit")))

summary(glm(mayo.SERIES_QUALITY_BIN~lh_defects,data=m,family=binomial(link="logit")))
summary(glm(mayo.SERIES_QUALITY_BIN~rh_defects,data=m,family=binomial(link="logit")))

summary(lm(Holes_LH~mayo.SERIES_QUALITY_BIN,data=m))
summary(lm(Holes_RH~mayo.SERIES_QUALITY_BIN,data=m))

boxplot(m$Holes_LH~m$mayo.SERIES_QUALITY_BIN)
boxplot(m$Holes_RH~m$mayo.SERIES_QUALITY_BIN)

summary(lm(lh_defects~mayo.SERIES_QUALITY_BIN,data=m))
summary(lm(rh_defects~mayo.SERIES_QUALITY_BIN,data=m))

boxplot(m$lh_defects~m$mayo.SERIES_QUALITY_BIN)
boxplot(m$rh_defects~m$mayo.SERIES_QUALITY_BIN)

# ------------------------------------------------------------------------------
# Sex prediction

mx<-m

vals<-seq(50,100,1)

boxplot(m$Weight~m$Sex)

mx.eval<-as.data.frame(cbind(
    val=vals,
    sens=unlist(sapply(vals,Sensitivity,event=mx$Sex=="M",x=mx$Weight)[1,]),
    spec=unlist(sapply(vals,Specificity,event=mx$Sex=="M",x=mx$Weight)[1,])
    ))

mx.cutoff<-vals[which.max(mx.eval$sens+mx.eval$spec)]

Sensitivity(event=mx$Sex,x=mx$Weight,cutoff=mx.cutoff)
Specificity(event=mx$Sex,x=mx$Weight,cutoff=mx.cutoff)

# get accuracy
addmargins(table(mx$Sex,mx$Weight>=mx.cutoff))

# boot
r<-Roc(Sex~Weight,data=mx)
print(r)
plot(r)

# Epi
ROC(stat=mx$Sex=="M",test=mx$Weight,MX=TRUE,PS=FALSE,cuts=seq(50,100,5))

# CV
p<-glm(Sex~Weight,data=mx,family=binomial(link=logit))
summary(p)

cost<-function(observed,predicted) {mean(abs(observed-predicted)>0.5)}
cost<-function(observed,predicted) {sum(abs(observed-predicted)>0.5)/length(observed)}
cv.glm(mx,p,cost,K=10)

# misc
inv.logit(predict(p)) # see also fitted(p)
addmargins(table(p$data$Sex,inv.logit(p$linear.predictors)>0.5))


# ------------------------------------------------------------------------------
# Quality prediction

mx<-m[complete.cases(m[,c("mayo.SERIES_QUALITY_BIN","Holes_LH","Holes_RH","lh_defects","rh_defects")]),]

vals<-seq(0,200,5)

mx.eval<-as.data.frame(cbind(
    val=vals,
    sens=unlist(sapply(vals,Sensitivity,event=mx$mayo.SERIES_QUALITY_BIN,x=mx$Holes_LH)[1,]),
    spec=unlist(sapply(vals,Specificity,event=mx$mayo.SERIES_QUALITY_BIN,x=mx$Holes_LH)[1,])
))

mx.cutoff<-vals[which.max(mx.eval$sens+mx.eval$spec)]

Sensitivity(event=mx$mayo.SERIES_QUALITY_BIN,x=mx$Holes_LH,cutoff=mx.cutoff)
Specificity(event=mx$mayo.SERIES_QUALITY_BIN,x=mx$Holes_LH,cutoff=mx.cutoff)

addmargins(table(mx$mayo.SERIES_QUALITY_BIN,mx$Holes_LH>=mx.cutoff))

# boot
r<-Roc(mayo.SERIES_QUALITY_BIN~Holes_LH,data=mx)
print(r)
plot(r)

# Epi
ROC(stat=mx$mayo.SERIES_QUALITY_BIN,test=mx$Holes_LH,MX=TRUE,PS=FALSE,cuts=seq(0,100,20))

# CV
p<-glm(mayo.SERIES_QUALITY_BIN~Holes_LH,data=mx,family=binomial(link=logit))
summary(p)

p<-glm(mayo.SERIES_QUALITY_BIN~Holes_LH+Holes_RH+lh_defects+rh_defects,data=mx,family=binomial(link=logit))
summary(p)

cost<-function(observed,predicted) {mean(abs(observed-predicted)>0.5)}
cv.glm(mx,p,cost,K=10)

# misc
inv.logit(predict(p)) # see also fitted(p)
addmargins(table(p$data$mayo.SERIES_QUALITY_BIN,inv.logit(p$linear.predictors)>=0.2))


