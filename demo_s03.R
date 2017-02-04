########################
# R Script for Class 3 #
########################
library(ggplot2)
library(scatterplot3d)
library(rgl)
library(stargazer)

DS = data.frame(city=c("AMG STGO", "Los Angeles", "Curico", "Temuco/Las Casas", "Serena-Coquimbo", "Talca", "AMGS CONCEP", "Iquique", "Rancagua", "Antofagusta", "Osorno", "Coyhaique", "Puenta Arenas", "Calama", "Copupo, T Amarilla", "AMG VALPSO", "Chulan-Ch Viejo", "Valdivia", "P.Montt", "Arica"), D=c(.36, .33, .32, .31, .30, .29, .29, .26, .26, .26, .25, .25, .23, .23, .23, .21, .19, .19, .17, .14), VT=c(23.4, 33.5, 32.1, 23.6, 17.9, 17.2, 17.0, 9.9,13.6, 13.9, 25.0, 23.9, 11.7, 10.0, 14.6, 9.5, 15.4, 10.7, 16.0, 6.7),  DMCS=c(2222.4, 2039.0, 3442.9, 2775.8, 2773.8, 2933.3, 1885.5, 2342.6, 2248.3, 1949.4, 1325.4, 1620.2, 1525.1, 2207.5,2908.0, 1921.6, 2160.0, 2021.9, 1474.5, 1802.1))

p = ggplot(DS, aes(x = D, y = DMCS))
p + geom_point()
p + geom_point() + geom_smooth(method = "lm", se = TRUE)

M0 = lm(DMCS~D, data=DS)
summary(M0)

M = lm(DMCS~D+VT, data=DS)
summary(M)

stargazer(M0, M, type="html")

newdat <- expand.grid(D=seq(.14,.36,by=.01),VT=seq(6.7,33.5,by=.1))

newdat$DMCS = predict(M, newdata=newdat)

with(DS,plot3d(D,VT,DMCS, col="blue", size=1, type="s", main="3D Linear Model Fit"))
with(newdat,surface3d(unique(D),unique(VT),DMCS,alpha=0.3,front="line", back="line"))
writeWebGL(dir="3Dreg", width=1000)
