# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 11:47:07 2022

@author: Dauerausleihe04
"""

import pandas as pd
import numpy as np
import os

#get the current path and the path where to save the files
path = os.getcwd()
targetPath = path.replace('\\transfer', '\dns-data\data\\')

#read some xlsx files
meta = pd.read_excel(path + '\\Exp_meta.xlsx')
meta.set_index('Tab_4a_Indikatorenblätter.Indikatoren', inplace = True)
indicators = pd.read_excel(path + '\\Tab_5a_Indikatoren.xlsx',  index_col=0)
categories = pd.read_excel(path + '\\Dic_Disagg_Kategorien.xlsx',  index_col=0)
expressions = pd.read_excel(path + '\\Dic_Disagg_Ausprägungen.xlsx',  index_col=0)
units = pd.read_excel(path + '\\Dic_Einheit.xlsx',  index_col=0)
data = pd.read_excel(path + '\\Exp_data.xlsx',  index_col=0)

#for maps
geoCodes = {'A_LAENDER_BW':'code08',
            'A_LAENDER_BY':'code09',
            'A_LAENDER_BE':'code11',
            'A_LAENDER_BB':'code12',
            'A_LAENDER_HB':'code04',
            'A_LAENDER_HH':'code02',
            'A_LAENDER_HE':'code06',
            'A_LAENDER_NI':'code03',
            'A_LAENDER_MV':'code13',
            'A_LAENDER_NW':'code05',
            'A_LAENDER_RP':'code07',
            'A_LAENDER_SL':'code10',
            'A_LAENDER_SN':'code14',
            'A_LAENDER_ST':'code15',
            'A_LAENDER_SH':'code01',
            'A_LAENDER_TH':'code16'}

# change the index of meta ("07.2.a,b") to become the filename of format "7-2-ab"
def getFilename(index):
    filename = index.lstrip('0').replace('.','-').replace(',','')                    
    if filename[-1].isnumeric():
        filename += '-a'
    return 'indicator_' + filename

#since meta contains one dataset per indicator we`re using meta`s index as loop variable
for page in meta.index: 
    #ibNr is present in both, meta and data, so we`re using it to get the relevant part of data                                                            
    ibNr = meta.loc[page, 'Tab_4a_Indikatorenblätter.IbNr']
    #now pageData only consist of the page`s datasets
    pageData = data[data.IbNr == ibNr]
    print(page)
    
    
    #get csv columns
    #default columns are
    columns = ['Year', 'Units', 'time series', 'Value']
    #add all disaggregations that are present for this indicator to the column list
    for disagg in set(list(pageData['Disaggregation 1 Kategorie']) + list(pageData['Disaggregation 2 Kategorie'])):
        if not pd.isnull(disagg) and not disagg in columns:
            columns.append(disagg)
            #get an additional column with geo-codes for map building if 'Länder' is one of the disaggregations
            if disagg == 'K_LAENDER':
                columns.append('GeoCode')
    
    #if we activate 'seriesToggle' for this indicator we need the column head to be 'Series' not 'time series'
    if meta.loc[page, 'Umschalten zwischen Zeitreihen?']:
        columns[2] = 'Series'
    
    #Note that the column 'time series' will contain the indicators titel unless there is a series defined as disaggregation category
    if 'K_SERIES' in list(pageData['Disaggregation 1 Kategorie']):
        try:
            columns.remove('time series')
        except ValueError:
            columns.remove('Series')
        
    
    #create a new dataframe with target shape
    #first create a list containing one dictionary for each year with value, containing the relevant columns
    # e.g. [{'Year':2010, 'Units':'%', 'time series': 'lorem ipsum', 'age': '18 years', 'Value': 99.0},
    #       {'Year':2011, 'Units':'%', 'time series': 'lorem ipsum', 'age': '18 years', 'Value': 88.0},...]
    targetData = []     
    for DNr in pageData.index:  #Dnr is the ID of a dataset that can contain values for year x ... y. 
                                #Every dataset is a unique combination of 'time series', disaggregation expression 1', 'disaggregation expression 2' and 'unit'
        for year in range(2000, 2030):  #loop through the years for every possible combination
            line = {}
            if not pd.isnull(pageData.loc[DNr, str(year)]):   #fill the dictionaries           
                for column in columns:
                    if column == 'Year':
                        line['Year'] = str(year)
                    elif column == 'Units':
                        line[column] = units.loc[pageData.loc[DNr, 'Einheit'],'Einheit En'].lower()
                    elif (column == 'time series' or column == 'Series'):
                        if 'K_SERIES' in list(pageData['Disaggregation 1 Kategorie']):
                            line[column] = expressions.loc[pageData.loc[DNr, 'Disaggregation 1 Ausprägung'], 'Ausprägung En'].lower()
                        else:
                            line[column] = indicators.loc[pageData.loc[DNr, 'INr'], 'Indikator En'].lower()
                    for d in ['1', '2']:
                        if column == pageData.loc[DNr, 'Disaggregation ' + d + ' Kategorie']:
                            if meta.loc[page, 'Umschalten zwischen Zeitreihen?'] and column == 'K_SERIES':
                                print("e")
                                line['Series'] = expressions.loc[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung'], 'Ausprägung En'].lower()
                            else:   
                                line[categories.loc[column, 'Kategorie En'].lower()] = expressions.loc[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung'], 'Ausprägung En'].lower()
                            if column == 'K_LAENDER':
                                line['GeoCodes'] = geoCodes[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung']]
                    if column == 'Value':
                        line[column] = pageData.loc[DNr, str(year)]
            if len(line) > 0:
                targetData.append(line)
    if page == '02.1.a':
        z = targetData
    if len(targetData) > 0:
        df = pd.DataFrame(targetData)
        
        #make sure Values are at right most column
        cols = df.columns.tolist()
        newCols = cols[:cols.index('Value')] + cols[cols.index('Value') + 1:] + cols[cols.index('Value'):cols.index('Value') + 1]
        df = df[newCols]
        
        #delete columns that contain only same values to not show disaggregations where there isn`t anything to select
        for column in df.columns:
            if not (column == 'Year' or column == 'Units' or column == 'Series' or column == 'Value') and (df[column] == df[column][0]).all():
                df.pop(column)
        
        #create a csv file from dataframe
        df.to_csv( targetPath + getFilename(page) + '.csv',  encoding='utf-8', index=False)
                    
        
