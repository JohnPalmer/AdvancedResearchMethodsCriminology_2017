# importa paquets
import pysal as ps
import pandas as pd
import numpy as np
import os
from ggplot import *
import math

# Comprova el directori de treball
os.getcwd()

# Canvia el directori de treball
os.chdir('/Users/palmer/Dropbox/upf_criminology/2017/slides/MICA2017/data')
# especifica la ruta de l'arxiu de formes
shp_path = 'nyc_assaults_subway_data.shp'

# càrrega l'arxiu de formes
D = ps.pdio.read_files(shp_path)

# limitant l'àrea d'anàlisi
# D = D[D.COUNTY != "Richmond"]
# D = D[D.COUNTY == "Kings"]

# gràfic de dispersió
ggplot(aes(x='POPULATION', y="n_assaults"), data=D) + geom_point()
ggplot(aes(x='n_subwayex', y="n_assaults"), data=D) + geom_point()

# ponderacions espacials
qW = ps.weights.Contiguity.Rook.from_dataframe(D)

# I del Moran
mi = ps.Moran(D.n_assaults.values[:, None], qW, two_tailed=False)
print mi.I
print mi.EI
print mi.p_norm

# regressio normal
m1 = ps.spreg.OLS(D[['n_assaults']].values, D[['n_subwayex', 'POPULATION']].values, w=qW, moran=True, spat_diag=True, name_x=D[['n_subwayex', 'POPULATION']].columns.tolist(), name_y='n_assaults')
print m1.summary

# regressio amb retard espacial en variables independents
sl = ps.lag_spatial(qW, D.n_subwayex.values[:, None])
D_sl = D.assign(w_subway = sl)
m2 = ps.spreg.OLS(D[['n_assaults']].values, D_sl[['n_subwayex', 'w_subway', 'POPULATION']].values, w=qW, spat_diag=True, moran=True, name_x=D_sl[['n_subwayex', 'w_subway', 'POPULATION']].columns.tolist(), name_y='assaults')
print m2.summary

# regressio amb retard espacial en variables dependents
m3 = ps.spreg.GM_Lag(D[['n_assaults']].values, D[['n_subwayex', 'POPULATION']].values, w=qW, spat_diag=True, name_x=D[['n_subwayex', 'POPULATION']].columns.tolist(), name_y='assaults')
print m3.summary

# regressio amb retard espacial en variables independents i dependents
m4 = ps.spreg.GM_Lag(D[['n_assaults']].values, D_sl[['n_subwayex', 'w_subway', 'POPULATION']].values, w=qW, spat_diag=True, name_x=D_sl[['n_subwayex', 'w_subway', 'POPULATION']].columns.tolist(), name_y='assaults')
print m4.summary
D_sl['m4_e'] = m4.u
ggplot(aes(x='n_subwayex', y='m4_e'), data=D_sl) + geom_point()
mi = ps.Moran(D_sl.m4_e.values[:, None], qW, two_tailed=False)
print mi.I
print mi.EI
print mi.p_norm


# regressio amb errors espacials
m5 = ps.spreg.GM_Error(D[['n_assaults']].values, D_sl[['n_subwayex', 'w_subway', 'POPULATION']].values, w=qW, name_x=D_sl[['n_subwayex', 'w_subway', 'POPULATION']].columns.tolist(), name_y='assaults')
print m5.summary
D_sl['m5_e'] = m5.u
ggplot(aes(x='n_subwayex', y='m5_e'), data=D_sl) + geom_point()
mi = ps.Moran(D_sl.m5_e.values[:, None], qW, two_tailed=False)
print mi.I
print mi.EI
print mi.p_norm


# guardar com csv
D_sl.to_csv('models_errors.csv')



