#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 23:59:09 2020

@author: tiago
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os as os


municipios = gpd.read_file('./data/br_municipios/BRMUE250GC_SIR.shp')
municipiosID = np.asarray( municipios['CD_GEOCMU'].values, dtype=int )

casos = pd.read_csv('cases-brazil-cities-time.csv')
casos = casos[casos.state != 'TOTAL']
casos = casos[casos.ibgeID > 100]
num_casos = casos['totalCases'].values.max()

rodovias = gpd.read_file('./data/rodovias/ST_DNIT_Rodovias_SNV2015_03.shp')

datas = ['2020-04-03']
datas = casos.date.values
datas = np.unique(datas)

for data in datas:

    casos_dia  = casos['totalCases'][casos['date']==data].values
    ibgeID_dia = casos['ibgeID'][casos['date']==data].values
    
    cores = np.zeros(municipiosID.shape)
    for i,id in enumerate(ibgeID_dia):
        cores[municipiosID == id] = casos_dia[i]
    
    fig, ax = plt.subplots(1,figsize=(8,8))
    plt.title('Municípios com casos de COVID-19',fontsize=18)
    estados = gpd.read_file('./data/br_unidades_da_federacao/BRUFE250GC_SIR.shp')
    estados.boundary.plot(ax=ax, edgecolor='black',linewidth=0.2)
    colors.Normalize(vmin=0.0,vmax=1.0)
    municipios.plot(ax=ax, cmap='Reds', norm=colors.Normalize(vmin=0.0,vmax=1.0), column=0.5*(cores>0))
    plt.axis('off')
    plt.text(-45,-32,data[8:10]+'/'+data[5:7]+'/'+data[0:4],fontsize=16)
    plt.text(-70,-23,'TFSilva-IFUSP',fontsize=9)
    plt.text(-70,-24,'Dados: github.com/wcota',fontsize=8)
    plt.tight_layout()
    rodovias.plot(ax=ax,linewidth=0.2,color='tab:gray')
    plt.savefig('./figs/fig_'+data+'_rodovias.png')
    plt.close()


HOME = os.getcwd()
os.chdir(os.path.join(HOME,'figs'))
string_command = 'convert -delay 25 -loop 0 *_rodovias.png fig_animated_roads.gif'
os.system(string_command)
os.chdir(HOME)


