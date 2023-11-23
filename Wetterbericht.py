# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:34:37 2023

@author: Dauerausleihe04
"""

import pandas as pd
import os

#get the current path and the path where to save the files
path = os.getcwd()

databaseData = pd.read_excel(path + '\\Wetterbericht.xlsx',  index_col=0)
databaseData = databaseData.rename(columns = {'WetterVergleichswerte?':'WetterVergleichswerte', 'WetterZeitreihe?': 'WetterZeitreihe'})
weather = databaseData.drop(databaseData[databaseData.WetterVergleichswerte].index).set_index('Indikator')
weatherCompare = databaseData.drop(databaseData[databaseData.WetterZeitreihe].index).set_index('Indikator')
results = {}

for i in weather.index:
   
    results[i] = {}
    results[i]["reportYear"] = weather.loc[i,"WetterBerichtsjahr"]
    results[i]["reportWeather"] = weather.loc[i, "WetterAktuell"]
    # identify years with values
    yearsWithValues = []
    values = []
    for y in range(2010 ,2025):
        if not pd.isnull(weather.loc[i,str(y)]):
            yearsWithValues.append(y)
            values.append(weather.loc[i, str(y)])
            
    if len(yearsWithValues) > 0:
        results[i]["recentYear"] = yearsWithValues[-1]
    else:
        results[i]["recentYear"] = "Ganz alt"        
        
    if len(yearsWithValues) < 6:
        results[i]["recentWeather"] = "Ganz alt"
    else:    
        wType = weather.loc[i, "Zieltyp"]
        wDir = weather.loc[i, "Zielrichtung"]
        wYear = weather.loc[i, "Zieljahr"]
        if i not in weatherCompare.index:
            wVal = weather.loc[i, "Zielwert"]
            if pd.isnull(wVal):
                wVal = ''
            else:
                wVal = float(wVal.replace(',','.'))
        else:
            wVal = weatherCompare.loc[i, str(yearsWithValues[-1])]
            
        # Cheating: Policy says target for 5.1.c is "equal participation". 
        # In the reports chart this is visualized by a slightly blury triangle at 50%. 
        # But in fact it was decided that 45% is sufficiend to be counted as "equal participation".
        # To have the marker in the chart at 50% this still ist the value that is saved in our database 
        # but for this calculation we need to replace it with 45.
        if i == "5.1.c":
            wVal = 45
            
        # Special case for 10.1: Two targets that should be fulfilled at the same time. 
        # a) is an "R" target with direction "rising" and
        # b) is a "K" target with direction "sinking" and value 0
        if i == "10.1":
            wType = "R"
            wDir = "steigen"
        
        
        # Check if for cases where a defined target value was met before the actual target year of where the target year is reached
        if wType == "K":
            if (wDir == "steigen" and max(values) >= wVal) or (wDir == "sinken" and min(values) <= wVal) or (yearsWithValues[-1] >= wYear):
                wType = "J"
                print(i)
        
        res = ''
        
        if wType == "R":
            meanDir = weather.loc[i, str(yearsWithValues[-1])] - weather.loc[i, str(yearsWithValues[-6])]
            if i == "11.1.b":
                print(meanDir)
            meanDir = 0
            lastDir = weather.loc[i, str(yearsWithValues[-1])] - weather.loc[i, str(yearsWithValues[-2])]
            if (wDir == "steigen" and meanDir > 0) or (wDir == "sinken" and meanDir < 0):
                if (wDir == "steigen" and lastDir > 0) or (wDir == "sinken" and lastDir < 0):
                    res = "S"
                else:
                    res = "L"
            elif (wDir == "steigen" and lastDir > 0) or (wDir == "sinken" and lastDir < 0):
                res = "W"
            else:
                res = "B"
                
            # for 10.1: saving results for part-target and setting new conditions for second part 
            if i == "10.1":
                res10_1_a = res
                wType = "K"
                wDir = "sinken"
        
        elif wType == "J":
            lastTgtDiff = weather.loc[i, str(yearsWithValues[-1])] - float(wVal)
            meanDir = weather.loc[i, str(yearsWithValues[-1])] - weather.loc[i, str(yearsWithValues[-6])]
            if (wDir == "steigen" and lastTgtDiff >= 0) or (wDir == "sinken" and lastTgtDiff <= 0):
                if (wDir == "steigen" and meanDir >= 0) or (wDir == "sinken" and meanDir <= 0):
                    res = "S"
                else:
                    res = "L"
            elif (wDir == "steigen" and meanDir >= 0) or (wDir == "sinken" and meanDir <= 0):
                res = "W"
            else:
                res = "B"
                
        elif wType == "K":
            meanDir = weather.loc[i, str(yearsWithValues[-1])] - weather.loc[i, str(yearsWithValues[-6])]
            hypoTgtVal = weather.loc[i, str(yearsWithValues[-1])] + meanDir / (yearsWithValues[-1] - yearsWithValues[-6]) * (wYear - yearsWithValues[-1])
            hypoTgtDiff = (wVal - hypoTgtVal) / (wVal - weather.loc[i, str(yearsWithValues[-1])])
            
            if hypoTgtDiff < 0.05:
                res = "S"
            elif hypoTgtDiff <= 0.2:
                res = "L"
            elif hypoTgtDiff < 1:
                res = "W"
            else:
                res = "B"

        # set the worse weather for 10.1 as result
        if i == "10.1":
            l = [res10_1_a, res]
            if "B" in l:
                res = "B"
            elif "W" in l:
                res = "W"
            elif "L" in l:
                res = "L"
            elif res10_1_a == res == "S":
                res = "S"
                          
        results[i]["recentWeather"] = res
        
        # if res != weather.loc[i, "WetterAktuell"]:
        #     print(i, results[i])
        
df = pd.DataFrame(results)  
df.to_excel("output.xlsx")     
        
            