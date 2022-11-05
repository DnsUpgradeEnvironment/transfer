# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 10:17:59 2022

@author: Dauerausleihe04
"""

import pandas as pd
import codecs
import os
import datetime
import fnmatch
import re
import string
import numpy as np

path = os.getcwd()

toggle = 'Upgrade'
#toggle = 'Prüf'
#toggle = 'Staging'

if toggle == 'Staging':
    targetPath = path.replace('\\transfer', '\dns-data\meta')
else:   
    targetPath = path.replace('\\transfer','\dns-data\meta')
    

meta = pd.read_excel(path + '\\Exp_meta.xlsx')
meta.set_index('Tab_4a_Indikatorenblätter.Indikatoren', inplace = True)
data = pd.read_excel(path + '\\Exp_data.xlsx',  index_col=0)
indicators = pd.read_excel(path + '\\Tab_5a_Indikatoren.xlsx',  index_col=0)
weather = pd.read_excel(path + '\\Tab_5b_Wetter.xlsx',  index_col=0)
weather2 = pd.read_excel(path + '\\Tab_5c_Wetter.xlsx',  index_col=0)

weatherWithIndicatorInfos = pd.merge(weather2, indicators, left_on="INr", right_index=True, how="left", sort=False)

def txtFct(text, lang):
    return text

def getWeatherFct(index, lang):
    IbNr = meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']
    df = weatherWithIndicatorInfos[(weatherWithIndicatorInfos.IbNr == IbNr)]
    counter = 0
    re = ''
    if len(df) > 0:
        for INr in df['INr'].unique():
            years = [str(x) for x in range(2010, 2026)]
            dfI = df[df.INr == INr].dropna(axis='columns', how='all') #df with one indicator only and no columns with nan only
            #readd some columns
            for column in ['VorherigesZieljahr', 'Gültig bis', 'Gültig seit']:
                if not column in dfI.columns:
                    l = [np.nan for x in range(len(dfI))]
                    dfI[column] = l
            
                
            counter += 1
            if lang == 'De':
                re += '\n\nweather_active_' + str(counter) + ': true' 
            re += '\nweather_indicator_' + str(counter) + ': ' + indicators.loc[INr, 'Indikator'] + ' ' + txtFct(indicators.loc[INr, 'Bezeichnung für Plattform ' + lang], lang)
            
            # Years
            years = [str(x) for x in range(2010, 2026)]
            yearCounter = 0
            for year in list(reversed(years)):
                if year in dfI.columns: 
                    re += '\nweather_indicator_' + str(counter) + '_year_' + string.ascii_lowercase[yearCounter] +': ' + year
                    yearCounter += 1
            
            # Actual target
            re += '\n\nweather_indicator_' + str(counter) + '_target: ' + indicators.loc[INr, 'Ziel ' + lang]
            
            # Loop through all available targets
            targetCounter = 0
            for target in dfI.index:
                targetCounter +=1
                re += '\n\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + ': '
                if 'ZielÜbersichtDe' in dfI.columns:
                    re += txtFct(dfI.loc[target, 'ZielÜbersicht' + lang], lang)
                else:
                    re += txtFct(indicators.loc[INr, 'Ziel ' + lang])
                
                # type of target
                targetType = 'normal'
               
                if not pd.isnull(dfI.loc[target, 'Gültig seit']):
                    targetType = 'new'                
                if not pd.isnull(dfI.loc[target, 'Gültig bis']):
                    targetTpe = 'old'
                    
                re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_category: ' + targetType
                if targetType == 'new':
                    re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_validFrom: ' + str(int(dfI.loc[target, 'Gültig seit']))
                if targetType == 'old':
                    re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_validUntil: ' + str(int(dfI.loc[target, 'Gültig bis']))
                
                re += '\n'
                
                # items
                yearCounter = 0
                for year in list(reversed(years)):
                    if year in dfI.columns: 
                        print(year)
                        re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_item_' + string.ascii_lowercase[yearCounter] + ': ' + ifNanFct(dfI.loc[target, year])
                        re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_item_' + string.ascii_lowercase[yearCounter] + '_title: ' #+ getTitleFct(dfI.loc[target, year], lang)
                        re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_item_' + string.ascii_lowercase[yearCounter] + '_valid: ' + getValidFct(year, dfI.loc[target, 'VorherigesZieljahr'], dfI.loc[target, 'Gültig bis'])
                        yearCounter += 1
                
                print(counter,target)
            
    return re
def getValidFct (year, prevTgtYear, validTill):
    if pd.isnull(year) or not pd.isnull(validTill):
        return 'false'
    elif not pd.isnull(prevTgtYear):
        if prevTgtYear >= int(year):
            return 'false'
        else:
            return"true"
    else:
        return 'true'

def ifNanFct(x):
    if pd.isnull(x):
        return ''
    else:
        return x
for page in meta.index:    
    
                                                             # page = 07.1.a,b
    if page == "07.1.a,b":
        print(page)
        print(getWeatherFct(page, 'De'))