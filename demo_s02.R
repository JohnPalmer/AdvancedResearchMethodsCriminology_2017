########################
# R Script for Class 2 #
########################

# t distribution
x <- seq(-4, 4, length=100)
hx <- dnorm(x)

degf <- c(1, 3, 8, 30)
colors <- c("red", "blue", "darkgreen", "gold", "black")
labels <- c("t gl=1", "t gl=3", "t gl=8", "t gl=30", "normal")

plot(x, hx, type="l", lty=2, xlab="x value",
     ylab="Densitat", main="Comparació de les distribucions t i normal")

for (i in 1:4){
  lines(x, dt(x,degf[i]), lwd=2, col=colors[i])
}

legend("topright",
       labels, lwd=2, lty=c(1, 1, 1, 1, 2), col=colors)

## Sampling distributions

# More on random numbers and chaos: Logistic Map example
n = 5000
r = 3.9
x1 = .5
x = rep(NA, n)
x[1] = x1
for(i in 1:(n-1)){
  x[i+1] = r*x[i]*(1-x[i])
}
plot(x, type="l")

plot(x, jitter(rep(1, n), 10), pch=19, cex=.5, col="#0000ff22")

hist(x)

dx = density(x)
plot(dx)
points(x, jitter(rep(1, n), 10), pch=19, cex=.5, col="#0000ff22")
lines(dx)


# Coin flips
c = rbinom(10, 1, .5)
mean(c)

c = rbinom(100, 100, .5)
hist(c)


# Sampling
pop = x
plot(density(pop))
mean(pop)
var(pop)
sd(pop)
quantile(pop, c(.05, .5, .95))


s = sample(pop, 10, replace=TRUE)
mean(s)
var(s)


s_means = sapply(1:10000, function(i) mean(sample(pop, 50, replace=TRUE)))
plot(density(s_means))

mean(s_means)
mean(pop)
var(s_means)
var(pop)



# checking p-values
1-pnorm(1.96)
1-pt(1.96, 15)

# loading data
D = read.csv2('shoesize.csv')
D


# exploring height
D$Height
mean(D$Height)
sd(D$Height)
quantile(D$Height)
hist(D$Height)
plot(density(D$Height))

sd(D$Height)/sqrt(408)


# Assumming this data is a random sample of the full school populatio, what is our best estimate of the mean height of all students at this university? Provide a point estimate and 95% confidence interval.



# Assumming this data is a random sample of the full school populatio, what is our best estimate of the mean shoe sizeght of all students at this university? Provide a point estimate and 95% confidence interval.

hist(D$Size)
mean(D$Size)
sd(D$Size)

mean(D$Size)+(2*(sd(D$Size)/sqrt(408)))
mean(D$Size)-(2*(sd(D$Size)/sqrt(408)))


# What is the relationship between height and shoe size?

plot(D$Height, D$Size)
cor(D$Height, D$Size)


M = lm(D$Height~D$Size)
summary(M)

M = lm(D$Height~D$Size+D$Gender)
summary(M)

M = lm(D$Height~D$Size+D$Gender + D$Size*D$Gender )
summary(M)

# family planning data
library(foreign)
library(calibrate)

D = read.dta('effort.dta')
head(D)

plot(change~effort, data=D, ylab="CBR change", xlab="program effort", pch=20, col="#000099dd", cex=2)

M = lm(change~effort, data=D)
summary(M)

M = lm(change~effort+setting, data=D)
summary(M)