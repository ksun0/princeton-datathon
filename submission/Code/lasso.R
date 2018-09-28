library('lars')
dat<-read.csv(file.choose(),header=T,fileEncoding = 'utf-8')
dat = dat[,c(4:41)]
n=nrow(dat)
set.seed(1234)
trainindex <- sample(1:n,0.7*n)
trainset <- dat[trainindex,]
testset <- dat[-trainindex,]
# (1) ols
X <- as.matrix(trainset[,-1])
Y <- as.matrix(trainset[,1])
X[is.na(X)] <- 0
attach(trainset)
model.ols <- lm(Y~X)
summary(model.ols)
library(car)
vif(model.ols)

# (3) lasso regression
X <- as.matrix(trainset[,-1])
Y <- as.matrix(trainset[,1])
X[is.na(X)] <- 0
model.lasso <- lars(X, Y, type='lasso')    
plot(model.lasso)
summary(model.lasso)
set.seed(123)
CV.lasso <- cv.lars(X,Y,K=10)
best <- CV.lasso$index[which.min(CV.lasso$cv)]
#best
coef.lasso <- coef.lars(model.lasso, mode='fraction', s=best)
#rename
names(coef.lasso) <- colnames(trainset)[-1]
#result
coef.lasso[coef.lasso!=0] 
laa = lars(X, Y, type = "lar")
laa


