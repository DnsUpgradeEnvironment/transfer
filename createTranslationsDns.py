# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 13:20:42 2022

@author: Dauerausleihe04
"""

import pandas as pd
import codecs
import os


path = os.getcwd()

toggle = 'Prüf'
#toggle = 'Staging'

if toggle == 'Staging':
    targetPath =  'C:\\Users\\Dauerausleihe04\\Documents\\DNS\\Plattform\\sdg-translations'
else:   
    targetPath = path.replace('\\MoBosse\DnsUpgradeEnvironment\\transfer','\\DNS\DnsTestEnvironment\sdg-translations')

meta = pd.read_excel(path + '\\Exp_meta.xlsx')
meta.set_index('Tab_4a_Indikatorenblätter.Indikatoren', inplace = True)
indicators = pd.read_excel(path + '\\Tab_5a_Indikatoren.xlsx',  index_col=0)
weather = pd.read_excel(path + '\\Tab_5b_Wetter.xlsx',  index_col=0)
links = pd.read_excel(path + '\\Tab_8a_Links.xlsx',  index_col=0)
orgas = pd.read_excel(path + '\\Tab_7a_Quellen.xlsx',  index_col=0)
goals = pd.read_excel(path + '\\Tab_1a_Ziele.xlsx',  index_col=0)
areas = pd.read_excel(path + '\\Tab_2a_Bereiche.xlsx',  index_col=0)
postulates = pd.read_excel(path + '\\Tab_3a_Postulate.xlsx',  index_col=0)



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
             'key': 'Einheit'},
       'd': {'title De': 'Indikatoren für Auswahlfelder',
             'title En': 'Indicators for selection filelds',
             'df': indicators,
             'key': 'Indikator in Auswahlfeld'},
       'e': {'title De': 'Indikatoren für Statusübersicht',
             'title En': 'Indicators for status overview',
             'df': indicators,
             'key': 'Indikator'}}

additions = {'a':{'key':['total','Year'],
                  'De':['Insgesamt','Jahr'],
                  'En':['Total','Year']},
             'b':{'key':[],
                  'De':[],
                  'En':[]},
             'c':{'key':[],
                  'De':[],
                  'En':[]},
             'd':{'key':[],
                  'De':[],
                  'En':[]},
             'e':{'key':[],
                  'De':[],
                  'En':[]}}


replaceDic = {'De':{' %': '&nbsp;%',
              'CO2': u'CO\u2082',
              #'PM10':'PM<sub>10</sub>',
              'PM10': u'PM\u2081\u2080',
              #'PM2,5':'PM<sub>2,5</sub>',
              'PM2,5': u'PM\u2082.\u2085',
              'PM2.5': u'PM\u2082.\u2085',
              'PM₅﮳₂': u'PM\u2082,\u2085'},
              'En':{'CO2': u'CO\u2082',
              #'PM10':'PM<sub>10</sub>',
              'PM10': u'PM\u2081\u2080',
              #'PM2,5':'PM<sub>2,5</sub>',
              'PM2,5': u'PM\u2082.\u2085',
              'PM2.5': u'PM\u2082.\u2085',
              'PM₅﮳₂': u'PM\u2082.\u2085'}}

def nanFct(inpt):
    if pd.isnull(inpt):
        return ''
    else:
        return inpt

def quotationFct(inpt):
    if (':' in inpt or str(inpt).replace('.','').isnumeric() or str(inpt).replace(' ','').isnumeric()) and not ((inpt[0] == "'" and inpt[-1] =="'") or (inpt[0] == '"' and inpt[-1] == '"')):
        if "'" in inpt:
            return '"' + inpt + '"'
        else:
            return "'" + inpt + "'"
    else:
        return inpt

def replaceFct(inpt, lang):
    for i in replaceDic[lang]:
        if i in inpt:
            inpt = inpt.replace(i, replaceDic[lang][i])
    return inpt
        

def txtFct (inpt, lang):
    return quotationFct(replaceFct(nanFct(inpt), lang))



for x in dic:
    print(x)
    file.write('\n#' + dic[x]['title De'] + '\n')
    fileEn.write('\n#' + dic[x]['title En'] + '\n')
    for dataset in dic[x]['df'].index:
        if not (pd.isnull(dic[x]['df'].loc[dataset, dic[x]['key'] + ' En']) or dic[x]['df'].loc[dataset, dic[x]['key'] + ' En'] == ' '):
            file.write(txtFct(dic[x]['df'].loc[dataset, dic[x]['key'] + ' En'].lower(), 'De') + ': ' + txtFct(dic[x]['df'].loc[dataset, dic[x]['key'] + ' De'], 'De')+ '\n')
            fileEn.write(txtFct(dic[x]['df'].loc[dataset, dic[x]['key'] + ' En'].lower(), 'En') + ': ' + txtFct(dic[x]['df'].loc[dataset, dic[x]['key'] + ' En'],'En') + '\n')
    
    if x == 'a':
        file.write('\n# Additions\n')
        fileEn.write('\n# Additions\n')
    for i in range(len(additions[x]['key'])):
        file.write(txtFct(additions[x]['key'][i-1], 'De') + ': ' + txtFct(additions[x]['De'][i-1], 'De') + '\n')
        fileEn.write(txtFct(additions[x]['key'][i-1], 'En') + ': ' + txtFct(additions[x]['En'][i-1], 'En') + '\n')
file.close()    
fileEn.close()    
    
    
file = codecs.open(targetPath + '\\translations\de\dns_goals.yml', 'w', 'utf-8')
fileEn = codecs.open(targetPath + '\\translations\en\dns_goals.yml', 'w', 'utf-8')  

for goal in goals.index:
    file.write(str(goals.loc[goal, "Ziel"])+'-title: ' + goals.loc[goal, "BezLangDe"] + '\n' + str(goals.loc[goal, "Ziel"]) + '-short: ' + goals.loc[goal, "BezKurzDe"] + '\n')
    fileEn.write(str(goals.loc[goal, "Ziel"])+'-title: ' + goals.loc[goal, "BezLangEn"] + '\n' + str(goals.loc[goal, "Ziel"]) + '-short: ' + goals.loc[goal, "BezKurzEn"] + '\n')
    
file.close()    
fileEn.close()

file = codecs.open(targetPath + '\\translations\de\dns_ranges.yml', 'w', 'utf-8')
fileEn = codecs.open(targetPath + '\\translations\en\dns_ranges.yml', 'w', 'utf-8')  

for area in areas.index:
    if area[1] == '0':
        sdg = area[2:3]
    else:
        sdg = area[1:3]
    key = sdg  + '.' + area[-1] + '-title: '
    file.write(key + areas.loc[area, "BezDe"] + '\n')
    fileEn.write(key + areas.loc[area, "BezEn"] + '\n')
    
file.close()    
fileEn.close()

file = codecs.open(targetPath + '\\translations\de\dns_targets.yml', 'w', 'utf-8')
fileEn = codecs.open(targetPath + '\\translations\en\dns_targets.yml', 'w', 'utf-8')  

for postulate in postulates.index:
    if postulate[1] == '0':
        sdg = postulate[2:3]
    else:
        sdg = postulate[1:3]
    key = sdg  + '.' + postulate[6] + '.' + postulate[-1] + '-title: '
    file.write(key + postulates.loc[postulate, "BezDe"] + '\n')
    fileEn.write(key + postulates.loc[postulate, "BezEn"] + '\n')
    
file.close()    
fileEn.close()