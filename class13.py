# importa paquets
import pysal as ps
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import os
import math

# Comprova el directori de treball
os.getcwd()

# Canvia el directori de treball
os.chdir('/Users/palmer/Dropbox/upf_criminology/2017/slides/MICA2017/data')
# especifica la ruta de l'arxiu de formes
shp_path = 'nyc_assaults_subway_data.shp'

# càrrega l'arxiu de formes
D = ps.pdio.read_files(shp_path)

D = D[D.app.notnull()]

M = ols('app ~ n_subwayex', data=D).fit()
print(M.summary())

fig = plt.figure(figsize=(12,8))
fig = smg.regressionplots.plot_regress_exog(M, 'n_subwayex', fig=fig)
plt.show()


qW = ps.queen_from_shapefile(shp_path)

D = ps.pdio.read_files(shp_path)

D.head()

mi = ps.Moran(D.n_assaults.values[:, None], qW, two_tailed=False)

mi.I
mi.EI

y = D.n_assaults.values[:, None]
xs = D.n_subwayex.values[:, None]

m1 = ps.spreg.OLS(y, xs, w=qW, spat_diag=True)

print(m1.summary)

sl = ps.lag_spatial(qW, D.n_subwayex.values[:, None])

D_sl = D.assign(w_subway = sl)


m2 = ps.spreg.OLS(D.n_assaults.values[:, None], D_sl[['n_subwayex', 'w_subway']].values, w=qW, spat_diag=True, name_x=D_sl[['n_subwayex', 'w_subway']].columns.tolist(), name_y='assaults')


m3 = ps.spreg.GM_Lag(D.n_assaults.values[:, None], D_sl[['n_subwayex', 'w_subway']].values, w=qW, spat_diag=True, name_x=D_sl[['n_subwayex', 'w_subway']].columns.tolist(), name_y='assaults')

print(m3.summary)


f = ps.pdio.read_files(ps.examples.get_path("stl_hom.csv"))
f.head()