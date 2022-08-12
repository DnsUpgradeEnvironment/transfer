# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 13:20:42 2022

@author: Dauerausleihe04
"""

import pandas as pd
import numpy as np
import codecs
import yaml
import os


path = os.getcwd()

toggle = 'Prüf'
#toggle = 'Staging'

if toggle == 'Staging':
    targetPath = path.replace('\\transfer', '\sdg-translations')
else:   
    targetPath = path.replace('\\transfer','\sdg-translations')
    

meta = pd.read_excel(path + '\\Exp_meta.xlsx')
meta.set_index('Tab_4a_Indikatorenblätter.Indikatoren', inplace = True)
indicators = pd.read_excel(path + '\\Tab_5a_Indikatoren.xlsx',  index_col=0)
weather = pd.read_excel(path + '\\Tab_5b_Wetter.xlsx',  index_col=0)
links = pd.read_excel(path + '\\Tab_8a_Links.xlsx',  index_col=0)
orgas = pd.read_excel(path + '\\Tab_7a_Quellen.xlsx',  index_col=0)

data = pd.read_excel(path + '\\Exp_data.xlsx',  index_col=0)


expressions = pd.read_excel(path + '\\Dic_Disagg_Ausprägungen.xlsx',  index_col=0)
categories = pd.read_excel(path + '\\Dic_Disagg_Kategorien.xlsx',  index_col=0)
units = pd.read_excel(path + '\\Dic_Einheit.xlsx',  index_col=0)


file = codecs.open(targetPath + '\\translations\de\data.yml', 'w', 'utf-8')
fileEn = codecs.open(targetPath + '\\translations\en\data.yml', 'w', 'utf-8')

dic = {'a': {'title De': 'Ausprägungen',
             'title En': 'Expressions',
             'df': expressions,
             'key': 'Ausprägung'},
       'b': {'title De': 'Kategorien',
             'title En': 'Expressions',
             'df': categories,
             'key': 'Kategorie'},
       'c': {'title De': 'Einheiten',
             'title En': 'Units',
             'df': units,
             'key': 'Einheit'}}

additions = {'a':{'key':['total'],
                  'De':['Insgesamt'],
                  'En':['Total']},
             'b':{'key':[],
                  'De':[],
                  'En':[]},
             'c':{'key':[],
                  'De':[],
                  'En':[]}}

replaceDic = {' %': '&nbsp;%'}

def nanFct(inpt):
    if pd.isnull(inpt):
        return ''
    else:
        return inpt

def quotationFct(inpt):
    if (':' in inpt or str(inpt).replace('.','').isnumeric()) and not ((inpt[0] == "'" and inpt[-1] =="'") or (inpt[0] == '"' and inpt[-1] == '"')):
        if "'" in inpt:
            return '"' + inpt + '"'
        else:
            return "'" + inpt + "'"
    else:
        return inpt

def replaceFct(inpt):
    for i in replaceDic:
        if i in inpt:
            inpt = inpt.replace(i, replaceDic[i])
    return inpt
        

def txtFct (inpt):
    return quotationFct(replaceFct(nanFct(inpt)))



for x in dic:
    print(x)
    file.write('\n#' + dic[x]['title De'] + '\n')
    fileEn.write('\n#' + dic[x]['title En'] + '\n')
    for dataset in dic[x]['df'].index:
        if not pd.isnull(dic[x]['df'].loc[dataset, dic[x]['key'] + ' En']):
            file.write(txtFct(dic[x]['df'].loc[dataset, dic[x]['key'] + ' En'].lower()) + ': ' + txtFct(dic[x]['df'].loc[dataset, dic[x]['key'] + ' De'] )+ '\n')
            fileEn.write(txtFct(dic[x]['df'].loc[dataset, dic[x]['key'] + ' En'].lower()) + ': ' + txtFct(dic[x]['df'].loc[dataset, dic[x]['key'] + ' En']) + '\n')
    
    if x == 'a':
        file.write('\n# Additions\n')
        fileEn.write('\n# Additions\n')
    for i in range(len(additions[x]['key'])):
        file.write(txtFct(additions[x]['key'][i-1]) + ': ' + txtFct(additions[x]['De'][i-1]) + '\n')
        fileEn.write(txtFct(additions[x]['key'][i-1]) + ': ' + txtFct(additions[x]['En'][i-1]) + '\n')
file.close()    
fileEn.close()    
    
    
    
    

