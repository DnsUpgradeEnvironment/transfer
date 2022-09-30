# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:40:46 2022

@author: Dauerausleihe04
"""

import pandas as pd
import codecs
import os
import datetime
import fnmatch

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
links = pd.read_excel(path + '\\Tab_8a_Links.xlsx',  index_col=0)
orgas = pd.read_excel(path + '\\Tab_7a_Quellen.xlsx',  index_col=0)
categories = pd.read_excel(path + '\\Dic_Disagg_Kategorien.xlsx',  index_col=0)
expressions = pd.read_excel(path + '\\Dic_Disagg_Ausprägungen.xlsx', index_col=0)
units = pd.read_excel(path + '\\Dic_Einheit.xlsx',  index_col=0)


# Get current year foe copyright
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")

# ----- Variables -----------

dataState = {'De': 'Der Indikatorenbericht 2021 hat den Datenstand 31.12.2020. Die Daten auf der DNS-Online Plattform werden regelmäßig aktualisiert, sodass online aktuellere Daten verfügbar sein können als im Indikatorenbericht 2021 veröffentlicht.',
             'En': 'The data published in the indicator report 2021 is as of 31.12.2020. The data shown on the DNS-Online-Platform is updated regularly, so that more current data may be available online than published in the indicator report 2021.'}

dicFootnoteLabels = {'Sing De':'Anmerkung',
               'Plur De': 'Anmerkungen',
               'Sing En':'Note',
               'Plur En': 'Notes'}

contentText = {'De': '<a href="https://dns-indikatoren.de/assets/publications/reports/de/2021.pdf">Text aus dem Indikatorenbericht 2021 </a>',
               'En': '<a href="https://dns-indikatoren.de/assets/publications/reports/en/2021.pdf">Text from the Indicator Report 2021 </a>'}

keyDict = {'Grafiktitel': 'graph_titles: ',
           'Untertitel': 'graph_subtitles: ',
           'Grafiktyp': 'graph_types: ',
           'Dezimalstellen': 'precision: ',
           'Achsenlimit': 'graph_limits: ',
           'Schrittweite y-Achse': 'graph_stepsize: ',
           'Zeitreihenbruch': 'graph_series_breaks: ',
           'minimum': ' Min',
           'maximum': ' Max',
           'title': '',
           'type': '',
           'decimals': '',
           'step': '',
           '': '',
           'value': ''}

pageLinkDic = {'Staging':{'De': 'www.dns-indikatoren.de/status',
                      'En': 'www.dns-indikatoren.de/en/status'},
               'Prüf': {'De': 'www.dnsTestEnvironment.github.io/dns-indicators/status',
                      'En': 'www.dnsTestEnvironment.github.io/dns-indicators/en/status'},
               'Upgrade': {'De': 'https://dnsUpgradeEnvironment.github.io/dns-indicators/status',
                      'En': 'https://dnsUpgradeEnvironment.github.io/dns-indicators/en/status'}}

replaceDic = {'De':
                  {' %': '&nbsp;%',
                   '1.000':'1&nbsp;000',
                   '1 000':'1&nbsp;000',
                   '100.000': '100&nbsp;000',
                   '100 000': '100&nbsp;000',
                   'CO2': u'CO\u2082',
                   'PM10': u'PM\u2081\u2080',
                   'PM2,5': u'PM\u2082,\u2085',
                   'PM0,1': u'PM\u2080,\u2081',
                   'PM₅﮳₂': u'PM\u2082,\u2085',
                   '\n':'<br>',
                   'm3': u'm\u00B3',
                   'm2': u'm\u00B2',
                   'SO2': u'SO\u2082',
                   'NOx': 'NO\u2093',
                   'NH3': 'NH\u2083',
                   'PM2.5': u'PM\u2082,\u2085',
                   'CH4': u'CH\u2084',
                   'N2O': u'N\u2082O',
                   'SF6': u'SF\u2086',
                   'NF3': u'NF\u2083'},
              'En':
                  {' %': '&nbsp;%',
                   '1.000':'1&nbsp;000',
                   '1 000':'1&nbsp;000',
                   '100.000': '100&nbsp;000',
                   '100 000': '100&nbsp;000',
                   'CO2': u'CO\u2082',
                   'PM10': u'PM\u2081\u2080',
                   'PM2,5': u'PM\u2082.\u2085',
                   'PM2.5': u'PM\u2082.\u2085',
                   'PM₅﮳₂': u'PM\u2082.\u2085',
                   'm3': u'm\u00B3',
                   'm2': u'm\u00B2',
                   'SO2': u'SO\u2082',
                   'NOx': 'NO\u2093',
                   'NH3': 'NH\u2083',
                   'PM2.5': u'PM\u2082.\u2085',
                   'CH4': u'CH\u2084',
                   'N2O': u'N\u2082O',
                   'SF6': u'SF\u2086',
                   'NF3': u'NF\u2083'}}

titleDic = {'linkToSrcOrga':{
                'De':{
                    'pre': 'Klicken Sie hier um zur Homepage der Organisation ',
                    'post': ' zu gelangen.'
                    },
                'En':{ 
                    'pre': 'Click here to visit the homepage of the organization',
                    'post': ''
                    }
                }
            }

weatherTitleDic= {'K':
                      {'Sonne':{'De': 'Bei Fortsetzung der Entwicklung würde der Zielwert erreicht oder um weniger als 5 % der Differenz zwischen Zielwert und aktuellem Wert verfehlt.',
                               'En': 'If the trend continues, the target value would be reached or missed by less than 5% of the difference between the target value and the current value.'},
                      'Leicht bewölkt':{'De': 'Bei Fortsetzung der Entwicklung würde das Ziel voraussichtlich um mindestens 5 %, aber maximal um 20 % der Differenz zwischen Zielwert und aktuellem Wert verfehlt.',
                               'En': 'If the development continues, the target would probably be missed by at least 5%, but by a maximum of 20% of the difference between the target value and the current value.'},
                      'Wolke':{'De': 'Der Indikator entwickelt sich zwar in die gewünschte Richtung auf das Ziel zu, bei Fortsetzung der Entwicklung würde das Ziel im Zieljahr aber um mehr als 20 % der Differenz zwischen Zielwert und aktuellem Wert verfehlt.',
                               'En': 'Although the indicator is moving in the desired direction toward the target, if the trend were to continue, the target would be missed in the target year by more than 20% of the difference between the target value and the current value.'},
                      'Blitz':{'De': 'Der Abstand zum Ziel ist konstant hoch oder vergrößert sich. Der Indikator entwickelt sich also nicht in die gewünschte Richtung.',
                               'En': 'The distance to the target is constantly high or increases. Thus, the indicator does not develop in the desired direction.'}},
                    'J':
                          {'Sonne':{'De': 'Der Zielwert oder ein besserer Wert wurde im letzten Jahr erreicht und die durchschnittliche Veränderung deutet nicht in Richtung einer Verschlechterung.',
                                   'En': 'The target value or a better value was achieved in the last year and the average change does not point in the direction of deterioration.'},
                          'Leicht bewölkt':{'De': 'Der Zielwert oder ein besserer Wert wurde im letzten Jahr erreicht, aber die durchschnittliche Veränderung deutet in Richtung einer Verschlechterung.',
                                   'En': 'The target value or a better value was achieved last year, but the average change points in the direction of deterioration.'},
                          'Wolke':{'De': 'Der Zielwert wurde nicht erreicht, aber die durchschnittliche Entwicklung weist in die gewünschte Richtung.',
                                   'En': 'The target value was not reached, but the average development points in the desired direction.'},
                          'Blitz':{'De': 'Der Zielwert wurde verfehlt und der Indikator hat sich im Durchschnitt der letzten Veränderungen nicht in Richtung des Ziels bewegt.',
                                   'En': 'The target value was missed and the indicator has not moved towards the target on average over the last changes.'}},
                    'R':
                          {'Sonne':{'De': 'Sowohl der Durchschnittswert als auch die letzte jährliche Veränderung deuten in die richtige Richtung.',
                                   'En': 'Both the average value and the last annual change point in the right direction.'},
                          'Leicht bewölkt':{'De': 'Die durchschnittliche Entwicklung zielt in die richtige Richtung, im letzten Jahr ergab sich jedoch eine Entwicklung in die falsche Richtung oder gar keine Veränderung.',
                                   'En': 'The average development aims in the right direction, but in the last year there was a development in the wrong direction or no change at all.'},
                          'Wolke':{'De': 'Der Durchschnittswert zielt in die falsche Richtung oder zeigt eine Stagnation an, im letzten Jahr zeigte sich jedoch eine Wende in die gewünschte Richtung.',
                                   'En': 'The average value aims in the wrong direction or indicates stagnation, but last year showed a turn in the desired direction.'},
                          'Blitz':{'De': 'Weder Durchschnittswert noch die letzte Veränderung deuten in die richtige Richtung.',
                                   'En': 'Neither the average value nor the last change point in the right direction.'}}}

# ----- Functions -----------
# ---- Functions to get stuff ---------
def addLinkFct(text, lang):
    indList = list(meta.index)
    indList.remove(page)
    for i in indList:
        repl = i.lstrip('0').replace(',',', ')
        if '1' + i.lstrip('0') in text:
            text = text.replace('1' + repl, '<a href="' + pageLinkDic[toggle][lang].replace('status','') + getFilename('1'+repl) + '">' + '1'+repl + '</a>')
            indList.remove('1'+i.lstrip('0'))
        else:
            text = text.replace(repl, '<a href="' + pageLinkDic[toggle][lang].replace('status','') + getFilename(i) + '">' + repl + '</a>')
    return text

transl = {'De': 'Ziel', 'En': 'Target', 'DeEveryYear': 'Jährliches Ziel', 'EnEveryYear': 'Constant target'}
def getAnnotations(index, lang):
    re = ''
    values = []
    allreadyMentioned = []
    # first look what tragte values there are to avoid printig multiple lines ober one another
    for iNr in indicators[indicators.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].index:
        if iNr in weather.index:
            for i in ['Zielwert', 'Etappenziel 1 Wert', 'Etappenziel 2 Wert', 'Etappenziel 3 Wert', 'Etappenziel 4 Wert']:
                if not pd.isnull(weather.loc[iNr, i]):
                    values.append(str(weather.loc[iNr, i]))
    
    for iNr in indicators[indicators.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].index:
        if iNr in weather.index:
            for i in ['Zielwert', 'Etappenziel 1 Wert', 'Etappenziel 2 Wert', 'Etappenziel 3 Wert', 'Etappenziel 4 Wert']:
                if not (pd.isnull(weather.loc[iNr, i]) or str(weather.loc[iNr, i]) in allreadyMentioned):
                    allreadyMentioned.append(str(weather.loc[iNr, i]))
                    #case: we have K_SERIES as Disaggregation category for this indicator and want to show the annotation only for one series
                    if not pd.isnull(weather.loc[iNr,'Spezifikation']):
                        re += '\n  - series: ' + expressions.loc[weather.loc[iNr, 'Spezifikation'], 'Ausprägung En'].lower() + '\n    '
                        
                    elif meta.loc[index, 'Umschalten zwischen Zeitreihen?']:
                        re += '\n  - series: ' + indicators.loc[iNr, 'Bezeichnung für Plattform En'].lower() + '\n    '
                    else:
                        re += '\n  - '
                    re += 'value: ' + str(weather.loc[iNr, i])
                    re += '\n    label:'
                    year = weather.loc[iNr, i.replace('wert','jahr').replace('Wert','Jahr')]
                    if not (pd.isnull(year) or year == 0):
                        re += '\n      content: ' + transl[lang] + ' ' + str(int(year))
                    else:
                        re += '\n      content: ' + transl[lang + 'EveryYear']
                    if len(set(indicators[indicators.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].index)) > 1 and not meta.loc[index, 'Umschalten zwischen Zeitreihen?'] and not values.count(str(weather.loc[iNr, i])) > 1:
                        re += ' - ' + indicators.loc[iNr,'Indikator kurz ' + lang] 
                    re += '\n      position: left'
                    re += '\n    preset: target_line'
    if len(re) > 0:
        re = 'graph_annotations:' + re
    return re

def getFilename(index):
    filename = index.lstrip('0').replace('.','-').replace(',','')                    # filename = 7-2-ab
    #if filename[-1].isnumeric():
    #    filename += '-a'
    return filename

def getFootnotes(index, lang):
    footnote = meta.loc[index, 'Fußnote ' + lang]
    re = ''
    
    if pd.isnull(meta.loc[index, 'Fußnote 1 De']):
        if not pd.isnull(footnote):
            footnote = footnote.replace('\n','<br>')
            if '<br>' in footnote:
                return 'data_footnotes: ' + txtFct(footnote.replace('<br>', '<br>• '), lang)
            else:
                return 'data_footnote: ' + txtFct(footnote, lang)
        else:
            return re       
    else:
        re += 'footer_fields:'
        for i in range(1,3):
            case = 'Sing '
            if not pd.isnull(meta.loc[index, 'Fußnote ' + str(i) + ' ' + lang]):
                spec = meta.loc[index, 'Fußnote ' + str(i) + ' Spezifikation']
                value = meta.loc[index, 'Fußnote ' + str(i) + ' ' + lang]
                if not pd.isnull(footnote):
                    value = footnote + '<br>' + value
                if '<br>' in value:
                    case = 'Plur '
                    value = '<br>' + value
                
                if not pd.isnull(spec):
                    if spec[0:2] == 'E_':
                        re += '\n  - unit: ' + units.loc[spec, 'Bezeichnung En'].lower() + '\n    '
                    elif spec[0:2] == 'A_':
                        re += '\n  - series: ' + expressions.loc[spec, 'Ausprägung En'].lower() + '\n    '
                    elif spec[0] == 'Z':
                        re += '\n  - series: ' + indicators.loc[spec, 'Bezeichnung für Plattform En'].lower() + '\n    '
                    else:
                        print("Error: Wrong key at footer field specificaion. ", index)
                else:
                        re += '\n  - '
                re += 'label: ' + txtFct(dicFootnoteLabels[case + lang], lang)
                re += '\n    value: ' + txtFct(value.replace('<br>', '<br>• '), lang)            
    return re

def getHeader(index, lang):
    re = ''
    wth = ''
    for iNr in indicators[indicators.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].index:
        if not pd.isnull(indicators.loc[iNr, 'Ziel kurz ' + lang]):
            re += '\n<div>'
            re += '\n  <div class="my-header">'
            re += '\n    <h5>' + txtFct(indicators.loc[iNr, 'Indikator kurz ' + lang], lang) + ': ' 
            re += txtFct(indicators.loc[iNr, 'Ziel kurz ' + lang], lang)
            if not pd.isnull(weather.loc[iNr, 'Ws t-0']):
                wth = weather.loc[iNr, 'Ws t-0']
            elif not pd.isnull(weather.loc[iNr, 'Etappenziel 1 Ws t-0']):
                wth = weather.loc[iNr, 'Etappenziel 1 Ws t-0']
            if wth != '':
                re += '\n      <a href="' + pageLinkDic[toggle][lang] + '"><img src="https://g205sdgs.github.io/sdg-indicators/public/Wettersymbole/' + wth + '.png" title="' + weatherTitleDic[weather.loc[iNr, 'Zieltyp']][wth][lang] + '" alt="' + getAltWeather(wth, lang) + '"/>'
                re += '\n      </a>'
            re += '\n    </h5>'
            re += '\n  </div>'
            re += '\n  <div class="my-header-note">'
            re += '\n  </div>'
            re += '\n</div>'
    return re

def getAltWeather(wth, lang):
    if lang == 'De':
        return 'Wettersymbol: ' + wth
    else: 
        return 'Weathersymbol: ' + wth.replace('Sonne', 'Sun').replace('Leicht bewölkt', 'Clouded sun').replace('Wolke', 'cloud').replace('Blitz', 'Thuder strom')


def getLanguageDependingContent(df, index, key, lang):
    if lang == 'De':
        otherLang = 'En'
    else: 
        otherLang = 'De'
    if not pd.isnull(df.loc[index, key + lang]):
        return df.loc[index, key + lang]
    elif not pd.isnull(df.loc[index, key + otherLang]):
        return df.loc[index, key + otherLang]
    else:
        return ''
    
def getPreviousIndex(index, case):
    positionPage = meta.index.get_loc(page)
    if positionPage == len(meta.index) -1:
        nextPosition = 0
        prevPosition = positionPage -1
    elif positionPage == 0:
        nextPosition = 1
        prevPosition = len(meta.index) -1
    else:
        nextPosition = positionPage + 1
        prevPosition = positionPage - 1
        
    if case == 'prev':
        return meta.index[prevPosition]
    elif case == 'next':
        return meta.index[nextPosition]
    
def getTargetId(BNr):
    re = list(BNr.replace('Z','').replace('_B','.').replace('_P','.'))
    for i in [6,3,0]:
        if re[i] == '0':
            re[i] = ''
    return "".join(re)

def getTitle(case, content, lang):
    return titleDic[case][lang]['pre'] + content + titleDic[case][lang]['post']

def getSomething(key, value):
    if not pd.isnull(value):
        return key + ': '+ value
    else:
        return ''
 
def getSourcesFct(index, lang):
    re = ''
    srcDic = {}
    c = 0
    for src in range(1, 19):
        if not pd.isnull(meta.loc[index, 'Link' + str(src)]):
            if meta.loc[index, 'Link' + str(src)][0] == 'L':
                lNr = meta.loc[index, 'Link' + str(src)]
                qNr = links.loc[lNr, 'QNr']
                if not qNr in srcDic:
                    srcDic[qNr] = [lNr]
                else: 
                    srcDic[qNr].append(lNr)
            elif meta.loc[index, 'Link' + str(src)][0] == 'Q':
                qNr = meta.loc[index, 'Link' + str(src)]
                if not qNr in srcDic:
                    srcDic[qNr] = []

    for orgaId in srcDic:
        c += 1
        d = -1
        appendix = ['','b','c','d','e','f']
        re += '\nsource_active_' + str(c) + ': true'
        re += '\nsource_organisation_' + str(c) + ": '" + '<a href="' + orgas.loc[orgaId, 'Homepage ' +lang] +'">' + orgas.loc[orgaId, 'Bezeichnung ' + lang] +"</a>'"
        re += '\nsource_organisation_' + str(c) + "_short: '" + '<a href="' + orgas.loc[orgaId, 'Homepage ' +lang] +'">' +  orgas.loc[orgaId, 'Bezeichnung lang ' + lang] +"</a>'"
        re += '\nsource_organisation_logo_' + str(c) + ': ' + "'" + '<a href="' + getLanguageDependingContent(orgas, orgaId, 'Homepage ', lang) + '"><img src="' + pageLinkDic[toggle][lang].replace('status','public/OrgImgDe/') + orgas.loc[orgaId, 'imgId'] + '.png" alt="' + orgas.loc[orgaId, 'Bezeichnung ' + lang] + '" title=" ' + getTitle('linkToSrcOrga', orgas.loc[orgaId, 'Bezeichnung ' + lang], lang) + '" style="height:60px; width:148px; border: transparent"/></a>' + "'"
        
        for linkId in srcDic[orgaId]:
            d += 1
            re += '\nsource_url_' + str(c) + appendix[d] + ": '" + getLanguageDependingContent(links, linkId, 'Link ', lang) + "'"
            re += '\nsource_url_text_' + str(c) + appendix[d] + ': ' + txtFct(links.loc[linkId, 'Text ' + lang], lang)
        re += '\n'  
    return re

def getSpecifiedStuff(index, key, upperRange, nameOne, nameTwo, lang):
    re = ''
    if pd.isnull(meta.loc[index, key + ' 1'+ keyDict[nameOne] + lang]) and nameTwo == '':
        return ''
    
    if (key == 'Grafiktitel' and pd.isnull(meta.loc[index, 'Grafiktitel 1 Spezifikation'])) or (key == 'Untertitel' and pd.isnull(meta.loc[index, 'Untertitel 1 Spezifikation'])):
        # graph_title would be overwritten by Seriesn names
        if meta.loc[index, 'Umschalten zwischen Zeitreihen?']:
            ibNr = meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']
            allSeries = list(set(data[data['IbNr'] == ibNr]['INr'])) 
            
            allKSeries = list(set(data[data['IbNr'] == ibNr]['Disaggregation 1 Ausprägung']))
            allKSeries = [x for x in allKSeries if not pd.isnull(x)]
            allKSeries = fnmatch.filter(allKSeries,'A_SERIES_*')
            if len(allKSeries) > 0:
                allSeries = allKSeries
            re += keyDict[key]
            for i in allSeries:
                if i[0] == 'Z' and not pd.isnull(indicators.loc[i, 'Bezeichnung für Plattform En']):
                    re += '\n  - series: ' + indicators.loc[i, 'Bezeichnung für Plattform En'].lower()
                    re += '\n    title: ' + txtFct(meta.loc[index, key + ' 1' + lang], lang[1:3]) 
                elif i[0:2] == 'A_':
                    re += '\n  - series: ' + expressions.loc[i, 'Ausprägung En'].lower()
                    re += '\n    title: ' + txtFct(meta.loc[index, key + ' 1' + lang], lang[1:3])              
            
        else:
            re += keyDict[key].replace('titles','title') + txtFct(meta.loc[index, key + ' 1' + lang], lang[1:3])
    elif key == 'Grafiktyp' and pd.isnull(meta.loc[index, 'Grafiktyp 1 Spezifikation']):
        re += 'graph_type: ' + meta.loc[index, 'Grafiktyp 1']
    else:
        re += keyDict[key] 
        for i in range(1, upperRange):
            spec = meta.loc[index, key + ' ' + str(i) + ' ' + 'Spezifikation']
            if not pd.isnull(spec):
                if spec[0:2] == 'E_':
                    re += '\n  - unit: ' + units.loc[spec, 'Einheit En'].lower() + '\n    '
                elif spec[0:2] == 'A_':
                    re += '\n  - series: ' + expressions.loc[spec, 'Ausprägung En'].lower() + '\n    '
                elif spec[0] == 'Z':
                    re += '\n  - series: ' + indicators.loc[spec, 'Bezeichnung für Plattform En'].lower() + '\n    '
                else:
                    print('Error at specification of ', key)
            elif not pd.isnull(meta.loc[index, key + ' ' + str(i) + keyDict[nameOne] + lang]):
                re +=  '\n  - '
            elif nameTwo != '':
                if not pd.isnull(meta.loc[index, key + ' ' + str(i) + keyDict[nameTwo] + lang]):
                    re +=  '\n  - '
            if not pd.isnull(meta.loc[index, key + ' ' + str(i) + keyDict[nameOne] + lang]):
                re += nameOne + ': ' + getSeriesBreakValue(index, meta.loc[index, key + ' ' + str(i) + keyDict[nameOne] + lang], key, spec, lang) + '\n    '
            if  nameTwo != '' and not pd.isnull(meta.loc[index, key + ' ' + str(i) + keyDict[nameTwo] + lang]):
                re += nameTwo + ': ' + str(meta.loc[index, key + ' ' + str(i) + keyDict[nameTwo] + lang]) 
    if re == keyDict[key] or re == '\n' or re == '\n\n':
        re = ''
    return re
# we get the series break year as an absolute year before that the break line should appear (i.e. 2020) --> 2016  2017  2018  2019 | 2020
# However we need a relativ position on x axis (first year == 0). In the example above: 2020 - 2016 - 0.5 = 3.5
def getSeriesBreakValue(index, breakYear, key, spec, lang):
    if not key == 'Zeitreihenbruch':
        if lang != '':
            return txtFct(breakYear, lang[1:3])
        else:
            return str(breakYear)
    else:
        df = data[data['IbNr'] == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']]
        if not pd.isnull(spec):
            if meta.loc[index, 'Umschalten zwischen Zeitreihen?'] and spec[0:9] == 'A_SERIES_':
                df = df[df['Disaggregation 1 Ausprägung'] == spec]  
        if len(df) > 0:
            for i in range(1990,2025):
                for j in df.index:
                    if (not pd.isnull(df.loc[j,str(i)])):
                        return str(breakYear - i - 0.5)
        else:
            return ''
            
def getStackedDisagg(index):
    if not pd.isnull(meta.loc[page, 'Gestapelte Disaggregation']):
        return '\n\ngraph_stacked_disaggregation: ' + categories.loc[meta.loc[index, 'Gestapelte Disaggregation'], 'Kategorie En'].lower()
    else:
        return ''
    
def getStartValues(index):
    re = ''
    allStartDatasets = data[(data['IbNr'] == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']) & (data['Beim Start anzeigen?'])]
    allreadyMentioned = []
    if len(allStartDatasets) > 0:
        re += '\n\ndata_start_values: '
        for INr in list(set(allStartDatasets.INr)):
            if not 'K_SERIES' in list(allStartDatasets['Disaggregation 1 Kategorie']) and not pd.isnull(indicators.loc[INr, 'Bezeichnung für Plattform En']):
                re += '\n  - field: time series'
                re += '\n    value: ' + indicators.loc[INr, 'Bezeichnung für Plattform En'].lower()
        for DNr in allStartDatasets.index:
            cat1 = allStartDatasets.loc[DNr, 'Disaggregation 1 Kategorie']
            exp1 = allStartDatasets.loc[DNr, 'Disaggregation 1 Ausprägung']
            cat2 = allStartDatasets.loc[DNr, 'Disaggregation 2 Kategorie']
            exp2 = allStartDatasets.loc[DNr, 'Disaggregation 2 Ausprägung']
            cat3 = allStartDatasets.loc[DNr, 'Disaggregation 3 Kategorie']
            exp3 = allStartDatasets.loc[DNr, 'Disaggregation 3 Ausprägung']
            if not (pd.isnull(cat1) or (cat1 + exp1) in allreadyMentioned):
                re += '\n  - field: ' + categories.loc[cat1, 'Kategorie En'].lower()
                re += '\n    value: ' + expressions.loc[exp1, 'Ausprägung En'].lower()
                allreadyMentioned.append(cat1 + exp1)
            if not (pd.isnull(cat2) or (cat2 + exp2) in allreadyMentioned):
                re += '\n  - field: ' + categories.loc[cat2, 'Kategorie En'].lower()
                re += '\n    value: ' + expressions.loc[exp2, 'Ausprägung En'].lower() 
                allreadyMentioned.append(cat2 + exp2)
            if not (pd.isnull(cat3) or (cat3 + exp3) in allreadyMentioned):
                re += '\n  - field: ' + categories.loc[cat3, 'Kategorie En'].lower()
                re += '\n    value: ' + expressions.loc[exp3, 'Ausprägung En'].lower() 
                allreadyMentioned.append(cat3 + exp3)
        if meta.loc[index, 'Umschalten zwischen Zeitreihen?']:
            re = re.replace('field: time series', 'field: Series')
    return re
    
def getWeatherFct(index, lang):
    c = 0
    re = ''
    for iNr in indicators[indicators.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].index:
        if iNr in weather.index and not pd.isnull(indicators.loc[iNr, 'Bezeichnung für Plattform ' + lang]):
            c += 1
            appendix = ['a','b','c','d','e','f','g','h']
            if lang == 'De':
                re += '\n\nweather_active_' + str(c) + ': true'
            re += '\nweather_indicator_' + str(c) + ': ' + indicators.loc[iNr, 'Indikator'] + ' ' + txtFct(indicators.loc[iNr, 'Bezeichnung für Plattform ' + lang], lang)
            if lang == 'De':
                # -- years -- 
                for t in range(7):
                    if not pd.isnull(weather.loc[iNr, 'Jahr t-' + str(t)]):
                        re += '\nweather_indicator_' + str(c) + '_year_' + appendix[t] + ": '" + str(int(weather.loc[iNr, 'Jahr t-' + str(t)])) + "'"
                    elif t == 0:
                        re += '\nweather_indicator_' + str(c) + '_year_' + appendix[t] + ": ''"  
                re += '\n'
            
            # -- multiple targets? ---
            if pd.isnull(weather.loc[iNr, 'Etappenziel 1 Jahr']):   # -- single target
                # -- old single target? ---
                new = ''
                value = weather.loc[iNr, 'Altes Ziel ' + lang]
                if not pd.isnull(value):
                    new = '_new'
                    re += '\nweather_indicator_' + str(c) + '_target_old: ' + txtFct(weather.loc[iNr, 'Altes Ziel ' + lang], lang) + '\n'
                    if lang == 'De':
                        re += '\nweather_indicator_' + str(c) + "_target_old_date: '" + str(int(weather.loc[iNr, 'Altes Ziel gültig bis'])) + "'\n"
                    # -- weather --
                    for t in range(7):
                        value = weather.loc[iNr, 'Ws altes Ziel t-' + str(t)]                       
                        if not pd.isnull(value):
                            title = weatherTitleDic[weather.loc[iNr, 'Zieltyp']][value][lang]
                            if lang == 'De':
                                re += '\nweather_indicator_' + str(c) + '_old_item_' + appendix[t] + ': ' + value
                            re += '\nweather_indicator_' + str(c) + '_old_item_' + appendix[t] + '_title: ' + title                         
                        elif t == 0:
                            re += '\nweather_indicator_' + str(c) + "_old_item_a: '-'"
                re += '\nweather_indicator_' + str(c) + '_target' + new + ': ' + txtFct(indicators.loc[iNr, 'Ziel ' + lang], lang) + '\n'
                
                # -- weather --
                for t in range(7):
                    value = weather.loc[iNr, 'Ws t-' + str(t)]
                    if not pd.isnull(value):
                        title = weatherTitleDic[weather.loc[iNr, 'Zieltyp']][value][lang]
                        if lang == 'De':
                            re += '\nweather_indicator_' + str(c) + new + '_item_' + appendix[t] + ': ' + value
                        re += '\nweather_indicator_' + str(c) + new + '_item_' + appendix[t] + '_title: ' + title
                    elif t == 0:
                        re += '\nweather_indicator_' + str(c) + new + "_item_a: '-'"    
            else:                                                   # -- multi targets        
                re += '\nweather_indicator_' + str(c) + '_target: ' + txtFct(indicators.loc[iNr, 'Ziel ' + lang], lang)
                for multiTarget in range(1,5):
                    re += '\n'
                    # -- old multi target? ---
                    new = ''
                    value = weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' ' + lang]
                    if not pd.isnull(value):
                        re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old: ' + txtFct(value, lang)
                        if lang == 'De':
                            re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + "_old_date: '" + str(int(weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' gültig bis'])) + "'"
                            if weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' Jahr'] != 0:
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + "_old_year: '" + str(int(weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' Jahr'])) + "'\n"
                        new = '_new'
                        
                        # -- weather --
                        for t in range(7):
                            value = weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' Ws t-' + str(t)]
                            if not pd.isnull(value):
                                title = weatherTitleDic[weather.loc[iNr, 'Zieltyp']][value][lang]
                                if lang == 'De':
                                    re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old_item_' + appendix[t] + ': ' + value
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old_item_' + appendix[t] + '_title: ' + title
                            elif t == 0:
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + "_old_item_a: '-'"
                    if not pd.isnull(weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' ' + lang]):                       
                        re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + ': ' + txtFct(weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' ' + lang], lang)
                        if weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' Jahr'] != 0:
                            re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + "_year: '" + str(int(weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' Jahr'])) + "'\n"
                        # -- weather --
                        for t in range(7):
                            value = weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' Ws t-' + str(t)]
                            if not pd.isnull(value):
                                title = weatherTitleDic[weather.loc[iNr, 'Zieltyp']][value][lang]
                                if lang == 'De':
                                    re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + '_item_' + appendix[t] + ': ' + value
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + '_item_' + appendix[t] + '_title: ' + title   
                            elif t == 0:
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + "_item_a: '-'"    
    return re


# -- Text functions ---------
def nanFct(inpt):
    if pd.isnull(inpt):
        return ''
    else:
        return inpt

def quotationFct(inpt):
    if ':' in inpt and not ((inpt[0] == "'" and inpt[-1] =="'") or (inpt[0] == '"' and inpt[-1] == '"')):
        if "'" in inpt:
            return '"' + inpt + '"'
        else:
            return "'" + inpt + "'"
    else:
        return inpt

def replaceFct(inpt, lang):
    for i in replaceDic[lang]:
        inpt = inpt.replace(i, replaceDic[lang][i])
    return inpt
        
def txtFct (inpt, lang):
    return quotationFct(replaceFct(wrappingFct(nanFct(inpt)), lang))
        
def wrappingFct(inpt):
    return inpt.replace('\n','<br><br>')
    
def getSdgIndicators(index):
    re = ''
    if not pd.isnull(meta.loc[index, 'SDG1']):
        re += "sdg_indicator: " + meta.loc[index, 'SDG1']
    if not pd.isnull(meta.loc[index, 'SDG2']):            
        re += "\nsdg_indicator2: " + meta.loc[index, 'SDG2']
    return re
# --------------------------------------
for page in meta.index:                                                             # page = 07.1.a,b
    
    print(page)
    
    file = codecs.open(targetPath + '\\'+ getFilename(page) + '.md', 'w', 'utf-8')
    fileEn = codecs.open(targetPath + '\\en\\' + getFilename(page) + '.md', 'w', 'utf-8')
    
    file.write("---\n\nlayout: indicator\
    \ngoal: '" + str(meta.loc[page, 'Ziel']) + "'\
    \nindicator: '" + getFilename(page).replace('-','.') + "'\
    \nindicator_display: '" + page.lstrip('0').replace(',',', ') + "'\
    \nindicator_sort_order: '" + getFilename(page) + "'\
    \npermalink: /" + getFilename(page) + "/\
    \n" + getSdgIndicators(page) + "\
    \n\n#\nreporting_status: complete\
    \npublished: true\
    \ndata_non_statistical: false\
    \n\n\n#Metadata\
    \nnational_indicator_available: " + txtFct(meta.loc[page, 'Tab_4a_Indikatorenblätter.BezDe'], 'De') + "\
    \n\ndns_indicator_definition: " + txtFct(meta.loc[page, 'DefinitionDe'], 'De') + "\
    \n\ndns_indicator_intention: "+ txtFct(meta.loc[page, 'IntentionDe'], 'De') +"\
    \n\ndata_state: " + dataState['De'] + "\
    \n\nindicator_name: " + txtFct(meta.loc[page, 'Tab_4a_Indikatorenblätter.BezDe'], 'De') + "\
    \nsection: " + txtFct(meta.loc[page, 'Tab_2a_Bereiche.BezDe'], 'De') + "\
    \npostulate: " + txtFct(meta.loc[page, 'Tab_3a_Postulate.BezDe'], 'De') + "\
    \ntarget_id: " + getTargetId(meta.loc[page, 'Tab_3a_Postulate.PNr']) + "\
    \nprevious: " + getFilename(getPreviousIndex(page, 'prev')) + "\
    \nnext: " + getFilename(getPreviousIndex(page, 'next')) + "\
    \n\n#content \
    \ncontent_and_progress: " + addLinkFct(txtFct("<i>" + contentText['De'] + "</i><br>" + meta.loc[page, 'InhaltDe'], 'De'), 'De') + "\
    \n\n#Sources\
    \n" + getSourcesFct(page, 'De') + "\
    \n\n#Status\
    \n" + getWeatherFct(page, 'De') + "\
    \n\ndata_show_map: " + str(meta.loc[page, 'Karte anzeigen?']).lower() + "\
    \ncopyright: '&copy; Statistisches Bundesamt (Destatis), " + year + "'\
    \n\n" + getFootnotes(page, 'De') + "\
    \n\n" + getSpecifiedStuff(page,'Grafiktitel', 5, 'title', '', ' De') + "\
    \n\n" + getSpecifiedStuff(page,'Untertitel', 5, 'title', '', ' De') + "\
    \n\n" + getAnnotations(page, 'De') + "\
    \n\n" + getSpecifiedStuff(page, 'Dezimalstellen', 4, 'decimals', '', '') +"\
    \n\nspan_gaps: " + str(meta.loc[page, 'Lücken füllen?']).lower() + "\
    \nshow_line: " + str(meta.loc[page, 'Linie anzeigen?']).lower() + "\
    \n\n" +  getSpecifiedStuff(page, 'Grafiktyp', 3, 'type', '', '') + "\
    " + getStartValues(page) +"\
    \n\n" + getSpecifiedStuff(page, 'Achsenlimit', 4, 'minimum', 'maximum', '') + "\
    \n\n" + getSpecifiedStuff(page, 'Schrittweite y-Achse', 4, 'step', '', '') + "\
    \n\n" + getSpecifiedStuff(page, 'Zeitreihenbruch', 4, 'value', '', '') + "\
    " + getStackedDisagg(page) + "\
    \n\n" + getSomething('national_geographical_coverage', meta.loc[page,'Geografische Abdeckung De']) + "\
    \n---\n\n" + getHeader(page, 'De'))
    
    fileEn.write("---\n\nlanguage: en\
    \nnational_indicator_available: " + txtFct(meta.loc[page, 'Tab_4a_Indikatorenblätter.BezEn'], 'En') + "\
    \n\ndns_indicator_definition: " + txtFct(meta.loc[page, 'DefinitionEn'], 'En') + "\
    \n\ndns_indicator_intention: "+ txtFct(meta.loc[page, 'IntentionEn'], 'En') +"\
    \n\ndata_state: " + dataState['En'] + "\
    \n\nindicator_name: " + txtFct(meta.loc[page, 'Tab_4a_Indikatorenblätter.BezEn'], 'En') + "\
    \nsection: " + txtFct(meta.loc[page, 'Tab_2a_Bereiche.BezEn'], 'En') + "\
    \npostulate: " + txtFct(meta.loc[page, 'Tab_3a_Postulate.BezEn'], 'En') + "\
    \n\n#content \
    \ncontent_and_progress: " + txtFct("<i>" + contentText['En'] + "</i><br>" + meta.loc[page, 'InhaltEn'], 'En') + "\
    \n\n#Sources\
    \n" + getSourcesFct(page, 'En') + "\
    \ncopyright: '&copy; Federal Statistical Office (Destatis), " + year + "'\
    \n\n" + getFootnotes(page, 'En') + "\
    \n\n" + getSpecifiedStuff(page,'Grafiktitel', 5, 'title', '', ' En') + "\
    \n\n" + getSpecifiedStuff(page,'Untertitel', 5, 'title', '', ' En') + "\
    \n\n" + getAnnotations(page, 'En') + "\
    \n\n" + getSomething('national_geographical_coverage', meta.loc[page,'Geografische Abdeckung En']) + "\
    \n" + getWeatherFct(page, 'En') +"\
    \n---\n\n" + getHeader(page, 'En'))
    
    fileEn.close()
    file.close()