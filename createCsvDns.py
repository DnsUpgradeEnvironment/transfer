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

#toggle = 'Upgrade'
toggle = 'Prüf'
#toggle = 'Staging'

imgTargetPath = path.replace('\\transfer', '\dns-data\data\\')

if toggle == 'Upgrade':
    targetPath = path.replace('\\transfer', '\dns-data\data\\')
elif toggle == 'Prüf':
    targetPath = path.replace('\\Documents\\MoBosse\\DnsUpgradeEnvironment\\transfer','\\Documents\\DNS\\DnsTestEnvironment\\dns-data\\data\\')
else:
    targetPath = path.replace('\\Documents\\MoBosse\\DnsUpgradeEnvironment\\transfer','\\Documents\\DNS\\Plattform\\open-sdg-data-starter\\data\\')


#read some xlsx files
meta = pd.read_excel(path + '\\Exp_meta.xlsx')
meta.set_index('Tab_4a_Indikatorenblätter.Indikatoren', inplace = True)
indicators = pd.read_excel(path + '\\Tab_5a_Indikatoren.xlsx',  index_col=0)
categories = pd.read_excel(path + '\\Dic_Disagg_Kategorien.xlsx',  index_col=0)
expressions = pd.read_excel(path + '\\Dic_Disagg_Ausprägungen.xlsx',  index_col=0)
units = pd.read_excel(path + '\\Dic_Einheit.xlsx',  index_col=0)
data = pd.read_excel(path + '\\Exp_data.xlsx',  index_col=0)
weather2 = pd.read_excel(path + '\\Tab_5b_Wetter.xlsx',  index_col=0)

geoCodesKreis = pd.read_excel(path + '\\Dic_GeoCodes.xlsx',  index_col=2)

#concat weather and indicators
weatherWithIndicatorInfos = pd.merge(weather2, indicators, left_on="INr", right_index=True, how="left", sort=False)
weatherWithIndicatorInfos.rename(columns={'InGrafikAnzeigen?': 'InGrafikAnzeigen'}, inplace=True)

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
    #if filename[-1].isnumeric():
    #   filename += '-a'
    return 'indicator_' + filename

def txtFct(string):
    if string == '1.000':
        return '1 000'
    else:
        return string
    
#since meta contains one dataset per indicator we`re using meta`s index as loop variable
for page in meta.index: 
    if (meta.loc[page, 'Indikator gesperrt?'] and toggle == 'Staging'):
        continue
    else:
        #ibNr is present in both, meta and data, so we`re using it to get the relevant part of data                                                            
        ibNr = meta.loc[page, 'Tab_4a_Indikatorenblätter.IbNr']
        #now pageData only consist of the page`s datasets
        pageData = data[data.IbNr == ibNr]
        
        print(page)
        
        
        #get csv columns
        #default columns are
        columns = ['Year', 'Units', 'time series', 'Value']
        #add all disaggregations that are present for this indicator to the column list
        for disagg in list(pageData['Disaggregation 1 Kategorie']) + list(pageData['Disaggregation 2 Kategorie']) + list(pageData['Disaggregation 3 Kategorie']):
            if not pd.isnull(disagg) and not disagg in columns:
                columns.append(disagg)
                #get an additional column with geo-codes for map building if 'Länder' is one of the disaggregations
                if disagg == 'K_LAENDER' or disagg == 'K_KREIS' and 'GeoCode' not in columns:
                    columns.append('GeoCode')
        
        #if we activate 'seriesToggle' for this indicator we need the column head to be 'Series' not 'time series'
        if meta.loc[page, 'Umschalten zwischen Zeitreihen?']:
            columns[2] = 'Series'
        
        #Note that the column 'time series' will contain the indicators titel unless there is a series defined as disaggregation category
        if 'K_SERIES' in list(pageData['Disaggregation 1 Kategorie']) and len(list(set(pageData['INr']))) == 1:
            if not meta.loc[page, 'Umschalten zwischen Zeitreihen?']:
                columns.remove('time series')
            else:
                columns.remove('Series')
        
        #lets find out which years contain data for this indicator
        yearsWithValues = []
        if page == '08.4x':
            ys = np.arange(2000,2017)
        else: 
            ys = np.arange(1990, 2025)
        for year in ys:  
            year = str(year)
            if (year in pageData.dropna(axis=1,how='all').columns and not meta.loc[page,str(year)]):
                yearsWithValues.append(year)
  
        # Fill in years without data if mor than 3 years are available
        if len(yearsWithValues) > 3:
            for year in range(int(yearsWithValues[0]), int(yearsWithValues[-1])):
                if not str(year) in yearsWithValues:
                    yearsWithValues.append(str(year))
                     
            
        # we also need a row for the target year(s)
        IbNr = meta.loc[page, 'Tab_4a_Indikatorenblätter.IbNr']
        #dfT = weatherWithIndicatorInfos[(weatherWithIndicatorInfos.IbNr == IbNr)]
        dfT = weatherWithIndicatorInfos.loc[(weatherWithIndicatorInfos.IbNr == IbNr) & (weatherWithIndicatorInfos.InGrafikAnzeigen == True)]
        
        for zielJahr in dfT.Zieljahr:
            if not pd.isnull(zielJahr):
                if not str(int(zielJahr)) in yearsWithValues:
                    yearsWithValues.append(str(int(zielJahr)))
        
        #create a new dataframe with target shape
        #first create a list containing one dictionary for each year with value, containing the relevant columns
        # e.g. [{'Year':2010, 'Units':'%', 'time series': 'lorem ipsum', 'age': '18 years', 'Value': 99.0},
        #       {'Year':2011, 'Units':'%', 'time series': 'lorem ipsum', 'age': '18 years', 'Value': 88.0},...]
        targetData = []     
        for DNr in pageData.index:  #Dnr is the ID of a dataset that can contain values for year x ... y. 
                                    #Every dataset is a unique combination of 'time series', disaggregation expression 1', 'disaggregation expression 2' and 'unit'
            
            #add "special years" like half years or time periods like "2010-2020"
            specials = {}
            for s in range(1,61):
                if 'AltLabel' + str(s) in pageData.dropna(axis=1,how='all').columns:
                    specials[s] = [pageData.loc[DNr,'AltLabel' + str(s)], pageData.loc[DNr,'Alt' + str(s)]]
            
            for year in yearsWithValues:  #loop through the years for every possible combination
                
                line = {}
                #if not pd.isnull(pageData.loc[DNr, str(year).replace('.',',')]):   #fill the dictionaries           
                for column in columns:
                    if column == 'Year':
                        line['Year'] = str(year)
                    elif column == 'Units' and not pd.isnull(units.loc[pageData.loc[DNr, 'Einheit'],'Einheit En']):
                        line[column] = txtFct(units.loc[pageData.loc[DNr, 'Einheit'],'Einheit En'].lower())
                    elif (column == 'time series' or column == 'Series'):
                        if 'K_SERIES' in list(pageData['Disaggregation 1 Kategorie']):
                            try:
                                line[column] = expressions.loc[pageData.loc[DNr, 'Disaggregation 1 Ausprägung'], 'Ausprägung En'].lower()
                            except KeyError:
                                line[column] = indicators.loc[pageData.loc[DNr, 'INr'], 'Indikator in Auswahlfeld En'].lower()
                        elif not pd.isnull(indicators.loc[pageData.loc[DNr, 'INr'], 'Indikator in Auswahlfeld En']):
                            line[column] = indicators.loc[pageData.loc[DNr, 'INr'], 'Indikator in Auswahlfeld En'].lower()
                    for d in ['1', '2', '3']:
                        if column == pageData.loc[DNr, 'Disaggregation ' + d + ' Kategorie']:
                            
                            if column == 'K_SERIES':
                                line['time series'] = expressions.loc[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung'], 'Ausprägung En'].lower()
                                if meta.loc[page, 'Umschalten zwischen Zeitreihen?']:
                                    line['Series'] = line.pop('time series')
                            
                            elif float(str(year).replace(',','.')) < 2025:   
                                line[categories.loc[column, 'Kategorie En'].lower()] = expressions.loc[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung'], 'Ausprägung En'].lower()
                                
                            elif pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung'] in list(dfT.Spezifikation):
                                print("222")
                                line[categories.loc[column, 'Kategorie En'].lower()] = expressions.loc[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung'], 'Ausprägung En'].lower()
                             
                            elif len(list(dfT.Spezifikation)) > 0:
                                line = {}
                                
                            if column == 'K_LAENDER' and float(year) < 2025:
                                line['GeoCode'] = geoCodes[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung']]
                            elif column == 'K_KREIS' and float(year) < 2025:
                                geo = str(geoCodesKreis.loc[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung'],'Code'])
                                if len(geo) == 4:
                                    geo = '0' + geo
                                line['GeoCode'] = 'code' + geo
                            
                    if column == 'Value' and str(year) in pageData.columns:
                        line[column] = pageData.loc[DNr, str(year).replace('.',',')]
                        
                # delete rows with GeoCode if there are no values to not show those years in map
                if 'GeoCode' in line and pd.isnull(line['Value']):
                    line = {}
                
                #if page == "06.2.a,b" and pd.isnull(line['Value']):
                    #line = {}
                   
                if len(line) > 0:
                    targetData.append(line)
                    
            for s in specials:
                label = specials[s][0]
                val = specials[s][1]
                line = {}
                for column in columns:
                    if column == 'Year':
                        line['Year'] = label
                    elif column == 'Units' and not pd.isnull(units.loc[pageData.loc[DNr, 'Einheit'],'Einheit En']):
                        line[column] = txtFct(units.loc[pageData.loc[DNr, 'Einheit'],'Einheit En'].lower())
                    elif (column == 'time series' or column == 'Series'):
                        if 'K_SERIES' in list(pageData['Disaggregation 1 Kategorie']):
                            try:
                                line[column] = expressions.loc[pageData.loc[DNr, 'Disaggregation 1 Ausprägung'], 'Ausprägung En'].lower()
                            except KeyError:
                                line[column] = indicators.loc[pageData.loc[DNr, 'INr'], 'Indikator in Auswahlfeld En'].lower()
                        elif not pd.isnull(indicators.loc[pageData.loc[DNr, 'INr'], 'Indikator in Auswahlfeld En']):
                            line[column] = indicators.loc[pageData.loc[DNr, 'INr'], 'Indikator in Auswahlfeld En'].lower()
                    for d in ['1', '2', '3']:
                        if column == pageData.loc[DNr, 'Disaggregation ' + d + ' Kategorie']:
                            
                            if column == 'K_SERIES':
                                line['time series'] = expressions.loc[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung'], 'Ausprägung En'].lower()
                                if meta.loc[page, 'Umschalten zwischen Zeitreihen?']:
                                    line['Series'] = line.pop('time series')                                                           
                            else:
                                line[categories.loc[column, 'Kategorie En'].lower()] = expressions.loc[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung'], 'Ausprägung En'].lower()                      
                            if column == 'K_LAENDER':
                                line['GeoCode'] = geoCodes[pageData.loc[DNr, 'Disaggregation ' + d + ' Ausprägung']]   
                    if column == 'Value':
                        line[column] = val
                        
                # delete rows with GeoCode if there are no values to not show those years in map
                if 'GeoCode' in line and pd.isnull(line['Value']):
                    line = {}
                
                #if page == "06.2.a,b" and pd.isnull(line['Value']):
                    #line = {}
                   
                if len(line) > 0:
                    targetData.append(line)
    
    # replace the 'K_...' key with the translation keys
    if 'time series' in columns and 'K_SERIES' in columns:
        columns.pop(columns.index('time series'))
    for column in columns:
        if column == 'K_SERIES':
            if meta.loc[page, 'Umschalten zwischen Zeitreihen?']:
                columns[columns.index(column)] = 'Series'
            else:
                columns[columns.index(column)] = 'time series'
        elif column[:2] == 'K_':
            columns[columns.index(column)] = categories.loc[column, 'Kategorie En'].lower()
            
   
    
    if len(targetData) > 0:
        df = pd.DataFrame(targetData) 
        
        #sort columns in same order as are in columns list
        df = df[columns]
            
        #make sure Values are at right most column
        cols = df.columns.tolist()
        newCols = cols[:cols.index('Value')] + cols[cols.index('Value') + 1:] + cols[cols.index('Value'):cols.index('Value') + 1]
        df = df[newCols]
        
        #delete columns that contain only same values to not show disaggregations where there isn`t anything to select
        for column in df.columns:
            if not (column == 'Year' or column == 'Units' or column == 'Series') and (df[column] == df[column][0]).all():
                df.pop(column)
        
        #create a csv file from dataframe
        df.to_csv( targetPath + getFilename(page) + '.csv',  encoding='utf-8', index=False)
                    
        
