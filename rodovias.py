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
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os as os


municipios = gpd.read_file('./data/br_municipios/BRMUE250GC_SIR.shp')
municipiosID = np.asarray( municipios['CD_GEOCMU'].values, dtype=int )

casos = pd.read_csv('cases-brazil-cities-time.csv')
casos = casos[casos.state != 'TOTAL']
casos = casos[casos.ibgeID > 100]
num_casos = casos['totalCases'].values.max()

estados = gpd.read_file('./data/br_unidades_da_federacao/BRUFE250GC_SIR.shp')
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
    estados.boundary.plot(ax=ax, edgecolor='black',linewidth=0.2)
    #municipios.plot(ax=ax, cmap='Reds', norm=colors.Normalize(vmin=0.0,vmax=1.0), column=0.5*(cores>0))
    divider = make_axes_locatable(ax)
    #cax = divider.append_axes(position='right',size="5%", pad=0.1)
    municipios.plot(ax=ax, cmap='Reds', norm=colors.LogNorm(vmin=0.1,vmax=num_casos), column=cores, legend=True, legend_kwds={'label': "Casos"})
    plt.axis('off')
    plt.text(-45,-32,data[8:10]+'/'+data[5:7]+'/'+data[0:4],fontsize=16)
    plt.text(-70,-23,'TFSilva-IFUSP',fontsize=9)
    plt.text(-70,-24,'Dados: github.com/wcota',fontsize=8)
    rodovias.plot(ax=ax,linewidth=0.2,color='tab:blue')
    plt.tight_layout()
    plt.savefig('./figs/fig_'+data+'_rodovias.png')
    municipios.boundary.plot(ax=ax, edgecolor='tab:gray',linewidth=0.05)
    plt.xlim(xmin=-53.2,xmax=-44.0)
    plt.ylim(ymin=-25.5,ymax=-19.5)
    plt.text(-47,-25,data[8:10]+'/'+data[5:7]+'/'+data[0:4],fontsize=16)
    plt.text(-52.5,-20,'TFSilva-IFUSP',fontsize=9)
    plt.text(-52.5,-20.2,'Dados: github.com/wcota',fontsize=8)
    plt.tight_layout()
    plt.savefig('./figs/fig_'+data+'_rodovias_SP.png')
    plt.close()


HOME = os.getcwd()
os.chdir(os.path.join(HOME,'figs'))
string_command = 'convert -delay 25 -loop 0 *_rodovias.png fig_animated_roads.gif'
os.system(string_command)
string_command = 'convert -delay 25 -loop 0 *_rodovias_SP.png fig_animated_roads_SP.gif'
os.system(string_command)
os.chdir(HOME)


