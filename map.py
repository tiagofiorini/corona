#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 23:21:48 2020

@author: tiago
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os as os


# ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2015/Brasil/BR/br_municipios.zip
# ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2015/Brasil/BR/br_unidades_da_federacao.zip

municipios = gpd.read_file('./data/br_municipios/BRMUE250GC_SIR.shp')
#fig, ax = plt.subplots(1)
#plt.title('Casos totais de COVID-19')
#municipios.plot(ax=ax, cmap='jet', column='CD_GEOCMU')

municipiosID = np.asarray( municipios['CD_GEOCMU'].values, dtype=int )

casos = pd.read_csv('cases-brazil-cities-time.csv')
casos = casos[casos.state != 'TOTAL']
casos = casos[casos.ibgeID > 100]
num_casos = casos['totalCases'].values.max()


#data = '2020-03-31'
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
    #municipios.plot(ax=ax, cmap='Reds', norm=colors.Normalize(vmin=0.0,vmax=1.0), column=0.5*(cores>0))
    municipios.plot(ax=ax, cmap='Reds', norm=colors.LogNorm(vmin=0.1,vmax=num_casos), column=cores, legend=True, legend_kwds={'label': "Casos"})
    plt.axis('off')
    plt.text(-45,-32,data[8:10]+'/'+data[5:7]+'/'+data[0:4],fontsize=16)
    plt.text(-70,-23,'TFSilva-IFUSP',fontsize=9)
    plt.text(-70,-24,'Dados: github.com/wcota',fontsize=8)
    plt.tight_layout()
    plt.savefig('./figs/fig_'+data+'_cases.png')
    plt.close()

# para gerar o gif:
# instalar o imagemagick: sudo apt install imagemagick
# dar o comando: convert -delay 10 -loop 0 *.png teste.gif
# dentro da pasta com as imagens

HOME = os.getcwd()
os.chdir(os.path.join(HOME,'figs'))
string_command = 'convert -delay 25 -loop 0 *_cases.png fig_animated.gif'
os.system(string_command)
os.chdir(HOME)