# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:40:46 2022

@author: Dauerausleihe04
"""

import pandas as pd
import numpy as np
import codecs
import os
import datetime
import fnmatch
import re
import string

path = os.getcwd()

toggle = 'Upgrade'
#toggle = 'Prüf'
#toggle = 'Staging'

if toggle == 'Upgrade':
    targetPath = path.replace('\\transfer', '\dns-data\meta')
else:   
    targetPath = path.replace('\\Documents\\MoBosse\\DnsUpgradeEnvironment\\transfer','\\Documents\\DNS\\Plattform\\open-sdg-data-starter\\meta')

    

meta = pd.read_excel(path + '\\Exp_meta.xlsx')
meta.set_index('Tab_4a_Indikatorenblätter.Indikatoren', inplace = True)
meta.sort_values(by='Tab_4a_Indikatorenblätter.Indikatoren', ascending=True, inplace=True)
data = pd.read_excel(path + '\\Exp_data.xlsx',  index_col=0)
data.sort_values(by='DNr', ascending=True, inplace=True)
indicators = pd.read_excel(path + '\\Tab_5a_Indikatoren.xlsx',  index_col=0)
weather = pd.read_excel(path + '\\Tab_5b_Wetter.xlsx',  index_col=0)
weather2 = pd.read_excel(path + '\\Tab_5c_Wetter.xlsx',  index_col=0)
weather2.sort_values(by='WNr', ascending=True, inplace=True)
links = pd.read_excel(path + '\\Tab_8a_Links.xlsx',  index_col=0)
orgas = pd.read_excel(path + '\\Tab_7a_Quellen.xlsx',  index_col=0)
categories = pd.read_excel(path + '\\Dic_Disagg_Kategorien.xlsx',  index_col=0)
expressions = pd.read_excel(path + '\\Dic_Disagg_Ausprägungen.xlsx', index_col=0)
units = pd.read_excel(path + '\\Dic_Einheit.xlsx',  index_col=0)
abbreviations = pd.read_excel(path + '\\Dic_Abkürzungen.xlsx',  index_col=0)

#concat weather and indicators
weatherWithIndicatorInfos = pd.merge(weather2, indicators, left_on="INr", right_index=True, how="left", sort=False)


# Get current year foe copyright
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")

# ----- Variables -----------

dataState = {'De': 'Der Indikatorenbericht 2022 hat den Datenstand 31.10.2022. Die Daten auf dieser Plattform werden regelmäßig aktualisiert, sodass online aktuellere Daten verfügbar sein können als im <a href="https://dns-indikatoren.de/facts_publications/">Indikatorenbericht 2022</a> veröffentlicht.',
             'En': 'The data published in the indicator report 2022 is as of Oct 31 2022. The data shown on this platform is updated regularly, so that more current data may be available online than published in the <a href="https://dns-indikatoren.de/en/facts_publications/">indicator report 2022</a>.'}

dicFootnoteLabels = {'Sing De':'Anmerkung',
               'Plur De': 'Anmerkungen',
               'Sing En':'Note',
               'Plur En': 'Notes'}

contentText = {'De': 'Text aus dem <a href="https://dns-indikatoren.de/facts_publications/">Indikatorenbericht 2022 </a>',
               'En': 'Text from the <a href="https://dns-indikatoren.de/en/facts_publications/">Indicator Report 2021 </a>'}

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
                  {'1.000':'1&nbsp;000',
                   '1 000':'1&nbsp;000',
                   '100.000': '100&nbsp;000',
                   '100 000': '100&nbsp;000',
                   'CO2': u'CO\u2082',
                   'PM10': u'PM\u2081\u2080',
                   'PM2,5': u'PM\u2080.\u2085',
                   'PM0,1': u'PM\u2080.\u2081',
                   'PM0.1': u'PM\u2080.\u2081',
                   'PM₅﮳₂': u'PM\u2082.\u2085',
                   '\n':'<br>',
                   'm3': u'm\u00B3',
                   'm2': u'm\u00B2',
                   'SO2': u'SO\u2082',
                   'NOx': 'NO\u2093',
                   'NH3': 'NH\u2083',
                   'PM2.5': u'PM\u2082.\u2085',
                   'CH4': u'CH\u2084',
                   'N2O': u'N\u2082O',
                   'SF6': u'SF\u2086',
                   'NF3': u'NF\u2083',
                   ' – ': '&nbsp;–&nbsp;'},
              'En':
                  {'1.000':'1&nbsp;000',
                   '1 000':'1&nbsp;000',
                   '100.000': '100&nbsp;000',
                   '100 000': '100&nbsp;000',
                   'CO2': u'CO\u2082',
                   'PM0.1': u'PM\u2080.\u2081',
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
                   'NF3': u'NF\u2083',
                   ' – ': '&nbsp;–&nbsp;'}}
replaceDicTextOnly = {'De':
                  {' -':' &#8209;',
                   '+ ': '+&nbsp;',
                   '‒ ': '‒&nbsp;'},
              'En':
                  {}}

sdgColors =    [['e5243b', '891523', 'ef7b89', '2d070b', 'f4a7b0', 'b71c2f', 'ea4f62', '5b0e17', 'fce9eb'],
                ['dda63a', '896d1f', 'efd385', '2d240a', 'f4e2ae', 'b7922a', 'eac55d', '5b4915', 'f9f0d6'],
                ['4c9f38', '2d5f21', '93c587', '0f1f0b', 'c9e2c3', '3c7f2c', '6fb25f', '1e3f16', 'a7d899'],
                ['c5192d', '760f1b', 'dc7581', '270509', 'f3d1d5', '9d1424', 'd04656', '4e0a12', 'e7a3ab'],
                ['ff3a21', 'b22817', 'ff7563', '330b06', 'ffd7d2', 'cc2e1a', 'ff614d', '7f1d10', 'ff9c90'],
                ['26bde2', '167187', '7cd7ed', '07252d', 'd3f1f9', '1e97b4', '51cae7', '0f4b5a', 'a8e4f3'],
                ['fcc30b', '977506', 'fddb6c', '322702', 'fef3ce', 'c99c08', 'fccf3b', '644e04', 'fde79d'],
                ['a21942', '610f27', 'c7758d', '610F28', 'ecd1d9', '811434', 'b44667', '400a1a', 'd9a3b3'],
                ['fd6925', '973f16', 'fda57c', '321507', 'fee1d3', 'ca541d', 'fd8750', '652a0e', 'fec3a7'],
                ['dd1367', '840b3d', 'ea71a3', '2c0314', 'f8cfe0', 'b00f52', 'd5358b', '580729', 'f1a0c2'],
                ['fd9d24', '653e0e', 'fed7a7', 'b16d19', 'fdba65', 'b14a1e', 'fd976b', '000000', 'fed2bf'],
                ['bf8b2e', '785b1b', 'dec181', '281e09', 'f4ead5', 'a07a24', 'd3ad56', '503d12', 'e9d6ab'],
                ['3f7e44', '254b28', '8bb18e', '0c190d', 'd8e5d9', '326436', '659769', '19321b', 'b2cbb4'],
                ['0a97d9', '065a82', '6cc0e8', '021e2b', 'ceeaf7', '0878ad', '3aabe0', '043c56', '9dd5ef'],
                ['56c02b', '337319', '99d97f', '112608', 'ddf2d4', '449922', '77cc55', '224c11', 'bbe5aa'],
                ['00689d', '00293e', '99c2d7', '00486d', '4c95ba', '126b80', 'cce0eb', '5a9fb0', 'a1c8d2'],
                ['19486a', '0a1c2a', '8ca3b4', '16377c', 'd1dae1', '11324a', '466c87', '5b73a3', '0f2656']]    

#for finding numbers with whitespace as decimal seperator:
decmark_reg = re.compile('(?<=\d) ')

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

def getWeatherTitel(year, asOfData, typus, ws, lang):
    if pd.isnull(ws):
        return 'No evaluation possible.'
    elif pd.isnull(typus):
        if lang == 'De':
            return 'Hier sind die unterschiedlichen Zieltypen der beiden, zeitgleich zu erreichenden, Ziele kombiniert worden.'
        else:
            return 'Different target types.'
    elif year == "current":
        return weatherTitleDic['current'][typus][ws][lang]
    else:
        return weatherTitleDic['former'][typus][ws][lang].replace('XXX', year + asOfData[lang])
    
weatherTitleDic= {'current':
                  {'K':
                      {'S':{'De': 'Bei Fortsetzung der Entwicklung würde der Zielwert erreicht oder um weniger als 5&nbsp;% der Differenz zwischen Zielwert und aktuellem Wert verfehlt.',
                               'En': 'If the trend continues, the target value would be reached or missed by less than 5% of the difference between the target value and the current value.'},
                      'L':{'De': 'Bei Fortsetzung der Entwicklung würde das Ziel voraussichtlich um mindestens 5&nbsp;%, aber maximal um 20&nbsp;% der Differenz zwischen Zielwert und aktuellem Wert verfehlt.',
                               'En': 'If the development continues, the target would probably be missed by at least 5%, but by a maximum of 20% of the difference between the target value and the current value.'},
                      'W':{'De': 'Der Indikator entwickelt sich zwar in die gewünschte Richtung auf das Ziel zu, bei Fortsetzung der Entwicklung würde das Ziel im Zieljahr aber um mehr als 20&nbsp;% der Differenz zwischen Zielwert und aktuellem Wert verfehlt.',
                               'En': 'Although the indicator is moving in the desired direction toward the target, if the trend were to continue, the target would be missed in the target year by more than 20% of the difference between the target value and the current value.'},
                      'B':{'De': 'Der Abstand zum Ziel ist konstant hoch oder vergrößert sich. Der Indikator entwickelt sich also nicht in die gewünschte Richtung.',
                               'En': 'The distance to the target is constantly high or increases. Thus, the indicator does not develop in the desired direction.'}},
                    'J':
                          {'S':{'De': 'Der Zielwert oder ein besserer Wert wurde im letzten Jahr erreicht und die durchschnittliche Veränderung deutet nicht in Richtung einer Verschlechterung.',
                                   'En': 'The target value or a better value was achieved in the last year and the average change does not point in the direction of deterioration.'},
                          'L':{'De': 'Der Zielwert oder ein besserer Wert wurde im letzten Jahr erreicht, aber die durchschnittliche Veränderung deutet in Richtung einer Verschlechterung.',
                                   'En': 'The target value or a better value was achieved last year, but the average change points in the direction of deterioration.'},
                          'W':{'De': 'Der Zielwert wurde nicht erreicht, aber die durchschnittliche Entwicklung weist in die gewünschte Richtung.',
                                   'En': 'The target value was not reached, but the average development points in the desired direction.'},
                          'B':{'De': 'Der Zielwert wurde verfehlt und der Indikator hat sich im Durchschnitt der letzten Veränderungen nicht in Richtung des Ziels bewegt.',
                                   'En': 'The target value was missed and the indicator has not moved towards the target on average over the last changes.'}},
                    'R':
                          {'S':{'De': 'Sowohl der Durchschnittswert als auch die letzte jährliche Veränderung deuten in die richtige Richtung.',
                                   'En': 'Both the average value and the last annual change point in the right direction.'},
                          'L':{'De': 'Die durchschnittliche Entwicklung zielt in die richtige Richtung, im letzten Jahr ergab sich jedoch eine Entwicklung in die falsche Richtung oder gar keine Veränderung.',
                                   'En': 'The average development aims in the right direction, but in the last year there was a development in the wrong direction or no change at all.'},
                          'W':{'De': 'Der Durchschnittswert zielt in die falsche Richtung oder zeigt eine Stagnation an, im letzten Jahr zeigte sich jedoch eine Wende in die gewünschte Richtung.',
                                   'En': 'The average value aims in the wrong direction or indicates stagnation, but last year showed a turn in the desired direction.'},
                          'B':{'De': 'Weder Durchschnittswert noch die letzte Veränderung deuten in die richtige Richtung.',
                                   'En': 'Neither the average value nor the last change points in the right direction.'}}},
                  'former':
                    {'K':
                      {'S':{'De': 'Bei Fortsetzung der Entwicklung aus XXX wäre der Zielwert erreicht oder um weniger als 5&nbsp;% der Differenz zwischen Zielwert und dem Wert aus XXX verfehlt worden.',
                               'En': 'If the trend from XXX had continued, the target value would have been reached or missed by less than 5% of the difference between the target value and the value at that time.'},
                      'L':{'De': 'Bei Fortsetzung der Entwicklung von XXX wäre das Ziel um mindestens 5&nbsp;%, aber maximal um 20&nbsp;% der Differenz zwischen Zielwert und dem Wert aus XXX verfehlt worden.',
                               'En': 'If the development from XXX had continued, the target had been missed by at least 5%, but by a maximum of 20% of the difference between the target value and the value at that time.'},
                      'W':{'De': 'Der Indikator entwickelte sich in XXX zwar in die gewünschte Richtung auf das Ziel zu, bei Fortsetzung der Entwicklung wäre das Ziel im Zieljahr aber um mehr als 20 % der Differenz zwischen Zielwert und dem Wert aus XXX verfehlt worden.',
                               'En': 'Although the indicator has in XXX been moving in the desired direction toward the target, if the trend had to continued, the target would have been missed in the target year by more than 20% of the difference between the target value and the value at that time.'},
                      'B':{'De': 'Der Abstand zum Ziel war in XXX konstant hoch oder hat sich vergrößert. Der Indikator entwickelte sich also nicht in die gewünschte Richtung.',
                               'En': 'In XXX the distance to the target was constantly high or had increased. Thus, the indicator did not develop in the desired direction.'}},
                    'J':
                          {'S':{'De': 'Der Zielwert oder ein besserer Wert wurde in XXX erreicht und die durchschnittliche Veränderung deutete nicht in Richtung einer Verschlechterung.',
                                   'En': 'In XXX the target value or a better value was achieved and the average change did not point in the direction of deterioration.'},
                          'L':{'De': 'Der Zielwert oder ein besserer Wert wurde in XXX erreicht, aber die durchschnittliche Veränderung deutete in Richtung einer Verschlechterung.',
                                   'En': 'In XXX the target value or a better value was achieved, but the average change pointed in the direction of deterioration.'},
                          'W':{'De': 'Der Zielwert wurde in XXX nicht erreicht, aber die durchschnittliche Entwicklung wies in die gewünschte Richtung.',
                                   'En': 'In XXX the target value was not reached, but the average development pointed in the desired direction.'},
                          'B':{'De': 'Der Zielwert wurde in XXX verfehlt und der Indikator hat sich im Durchschnitt der vorangegangenen Veränderungen nicht in Richtung des Ziels bewegt.',
                                   'En': 'In XXX the target value was missed and the indicator had not moved towards the target on average over the previous changes.'}},
                    'R':
                          {'S':{'De': 'Sowohl der Durchschnittswert als auch die vorangegangene jährliche Veränderung deuteten in XXX in die richtige Richtung.',
                                   'En': 'In XXX both the average value and the previous annual change pointed in the right direction.'},
                          'L':{'De': 'Die durchschnittliche Entwicklung zielte in XXX in die richtige Richtung, im vorangegangenen Jahr ergab sich jedoch eine Entwicklung in die falsche Richtung oder gar keine Veränderung.',
                                   'En': 'In XXX the average development aimed in the right direction, but in the previous year there had been a development in the wrong direction or no change at all.'},
                          'W':{'De': 'Der Durchschnittswert zielte in XXX in die falsche Richtung oder zeigt eine Stagnation an, im vorangegangenen Jahr zeigte sich jedoch eine Wende in die gewünschte Richtung.',
                                   'En': 'In XXX the average value aimed in the wrong direction or indicates stagnation, but the previous year had shown a turn in the desired direction.'},
                          'B':{'De': 'Weder Durchschnittswert noch die vorherige Veränderung deuten in XXX in die richtige Richtung.',
                                   'En': 'In XXX neither the average value nor the last change pointed in the right direction.'}}}}

# ----- Functions -----------
# ---- Functions to get stuff ---------
def addLinkFct(text, lang):
    indList = list(meta.index)
    indList.remove(page)
    for i in indList:
        repl = i.lstrip('0').replace(',',', ')
        if ('1' + repl + ' ' in text or '1' + repl + ')' in text) and not page == '1' + i.lstrip('0') :
            text = text.replace('1' + repl, '<a href="' + pageLinkDic[toggle][lang].replace('status','') + getFilename('1'+repl) + '">' + '1' + repl + '</a>')
            indList.remove('1'+i.lstrip('0'))
        elif repl + '&nbsp;' in text or repl + ' ' in text or repl + ')' in text:
            text = text.replace(repl, '<a href="' + pageLinkDic[toggle][lang].replace('status','') + getFilename(i) + '">' + repl + '</a>')
            
    for i in singleIndList:
        text = text.replace(' ' + i, ' ' + singleIndList[i])
    return text

singleIndList = {'1.1.a': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '1-1-ab">1.1.a</a>',
                 '1.1.b': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '1-1-ab">1.1.b</a>',
                 '3.1.a': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '3-1-ab">3.1.a</a>',
                 '3.1.b': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '3-1-ab">3.1.b</a>',
                 '3.1.c': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '3-1-cd">3.1.c</a>',
                 '3.1.d': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '3-1-cd">3.1.d</a>',
                 '4.2.a': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '4-2-ab">4.2.a</a>',
                 '4.2.b': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '4-2-ab">4.2.b</a>',
                 '5.1.b': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '5-1-bc">5.1.b</a>',
                 '5.1.c': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '5-1-bc">5.1.c</a>',
                 '6.2.a': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '6-2-ab">6.2.a</a>',
                 '6.2.b': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '6-2-ab">6.2.b</a>',
                 '7.1.a': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '7-1-ab">7.1.a</a>',
                 '7.1.b': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '7-1-ab">7.1.b</a>',
                 '8.2.a': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '8-2-ab">8.2.a</a>',
                 '8.2.b': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '8-2-ab">8.2.b</a>',
                 '8.5.a': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '8-5-ab">8.5.a</a>',
                 '8.5.b': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '8-5-ab">8.5.b</a>',
                 '12.1.ba': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '12-1-b">12.1.ba</a>',
                 '12.1.bb': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '12-1-b">12.1.bb</a>',
                 '12.1.bc': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '12-1-b">12.1.bc</a>',
                 '12.3.a' : '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '12-3-ab">12.3.a</a>',
                 '12.3.b' : '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '12-3-ab">12.3.b</a>',
                 '14.1.aa': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '14-1-a">14.1.aa</a>',
                 '14.1.ab': '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '14-1-a">14.1.ab</a>',
                 '15.3.a' : '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '15-3-ab">15.3.a</a>',
                 '15.3.b' : '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '15-3-ab">15.3.b</a>',
                 '16.3.a' : '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '16-1-ab">16.3.a</a>',
                 '16.3.b' : '<a href="' + pageLinkDic[toggle]['De'].replace('status','') + '16-1-ab">16.3.b</a>'}


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
                    re += '\n      backgroundColor: transparent'
                    re += '\n      color: transparent'
                    re += '\n    preset: target_line'
                    re += '\n    backgroundColor: transparent'

    if len(re) > 0:
        re = 'graph_annotations:' + re
    return re

def getContentFct (index, lang):
    firstPart = meta.loc[page, 'Inhalt' + lang + '1']
    secondPart = meta.loc[page, 'Inhalt' + lang + '2']
    if firstPart[-100:] == secondPart[-100:]:
        return firstPart
    else:
        matchingPart = ''
        for i in range(len(secondPart)):
            #print(firstPart[-i:], secondPart [:i])
            if firstPart[-i:] != secondPart [:i]:
                matchingPart += secondPart[i]
                #print(matchingPart)
            else:
                break
        return firstPart.replace(matchingPart, secondPart)
    

def getFilename(index):
    filename = index.lstrip('0').replace('.','-').replace(',','')                    # filename = 7-2-ab
    #if filename[-1].isnumeric():
    #    filename += '-a'
    return filename

def getFootnotes(index, lang):
    footnote = meta.loc[index, 'Fußnote ' + lang]
    re, specList = '', []
    
    if pd.isnull(meta.loc[index, 'Fußnote 1 De']):
        if not pd.isnull(footnote):
            footnote = footnote.replace('\n','<br>')
            if '<br>' in footnote:
                return 'data_footnotes: ' + txtFct('false', 'true', footnote.replace('<br>', '<br>• '), lang)
            else:
                return 'data_footnote: ' + txtFct('false', 'true', footnote, lang)
        else:
            return re       
    else:
        re += 'footer_fields:'
        for i in range(1,3):
            case = 'Sing '
            if not pd.isnull(meta.loc[index, 'Fußnote ' + str(i) + ' ' + lang]):
                spec = meta.loc[index, 'Fußnote ' + str(i) + ' Spezifikation']
                specList.append(spec)
                value = meta.loc[index, 'Fußnote ' + str(i) + ' ' + lang]
                if not pd.isnull(footnote):
                    value = footnote + '<br>' + value
                if '<br>' in value:
                    case = 'Plur '
                    value = '<br>' + value
                
                if not pd.isnull(spec):
                    if spec[0:2] == 'E_':
                        re += '\n  - unit: ' + units.loc[spec, 'Bezeichnung En'].lower() + '\n    '
                        list(set(data[data.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].Einheit))
                    elif spec[0:2] == 'A_':
                        re += '\n  - series: ' + expressions.loc[spec, 'Ausprägung En'].lower() + '\n    '
                    elif spec[0] == 'Z':
                        re += '\n  - series: ' + indicators.loc[spec, 'Bezeichnung für Plattform En'].lower() + '\n    '
                        possSpec = list(set(data[data.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].INr))
                    else:
                        print("Error: Wrong key at footer field specificaion.", index)
                else:
                        re += '\n  - '
                re += 'label: ' + txtFct('false', 'true', dicFootnoteLabels[case + lang], lang)
                re += '\n    value: ' + txtFct('false', 'true', value.replace('<br>', '<br>• '), lang) 
        # case general footnote plus specified footnote --> generel part needs to be added as specified for the rest
        if not pd.isnull(footnote) and len(specList) < len(possSpec): 
            for spec in list(set(possSpec) - set(specList)):
                re += '\n  - series: ' + indicators.loc[spec, 'Bezeichnung für Plattform En'].lower()
                re += '\n    label: ' + txtFct('false', 'true', dicFootnoteLabels[case + lang], lang)
                re += '\n    value: ' + txtFct('false', 'true', footnote.replace('<br>', '<br>• '), lang) 
    return re

def getHeader(index, lang):
    re = ''
    wth = ''
    for iNr in indicators[indicators.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].index:
        if not pd.isnull(indicators.loc[iNr, 'Ziel kurz ' + lang]):
            re += '\n<div>'
            re += '\n  <div class="my-header">'
            re += '\n    <label class="default">' + txtFct('false', 'true', indicators.loc[iNr, 'Indikator kurz ' + lang], lang) + ': ' 
            re += txtFct('false', 'true', indicators.loc[iNr, 'Ziel kurz ' + lang], lang)
            if not pd.isnull(weather.loc[iNr, 'Ws t-0']):
                wth = weather.loc[iNr, 'Ws t-0']
            elif not pd.isnull(weather.loc[iNr, 'Etappenziel 1 Ws t-0']):
                wth = weather.loc[iNr, 'Etappenziel 1 Ws t-0']
            elif not pd.isnull(weather.loc[iNr, 'Etappenziel 2 Ws t-0']):
                wth = weather.loc[iNr, 'Etappenziel 2 Ws t-0']
            if wth != '':
                lastWeatherYear = str(int(weather.loc[iNr, 'Jahr t-0']))
                re += '\n      <a href="' + pageLinkDic[toggle][lang] + '"><img src="https://g205sdgs.github.io/sdg-indicators/public/Wettersymbole/' + wth + '.png" title="' + getWeatherTitel(lastWeatherYear, {'De':' (Datenstand 31.10.2022)','En':' (Data as of Oct. 31 2022)'}, weather.loc[iNr, 'Zieltyp'], wth[0], lang) + '" alt="' + getAltWeather(wth, lang) + '"/>'
                re += '\n      </a>'
            re += '\n    </label>'
            re += '\n  </div>'   
            re += '\n</div>'
    re += '\n<div class="my-header-note">'
    re += '\n  <label class="default">'
    re += '\n    Die Bewertung des Indikators beruht auf den Daten des Berichtsjahres 2020 zum Stand 31.10.2022.'
    re += '\n</label>'
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
        return '\n\n' + key + ': '+ value
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
        re += '\nsource_organisation_' + str(c) + "_short: '" + '<a href="' + orgas.loc[orgaId, 'Homepage ' +lang] + '" target="_blank">' +  orgas.loc[orgaId, 'Bezeichnung ' + lang] +"</a>'" #'Bezeichnung lang ' + lang] +"</a>'"
        re += '\nsource_organisation_logo_' + str(c) + ': ' + "'" + '<a href="' + getLanguageDependingContent(orgas, orgaId, 'Homepage ', lang) + '" target="_blank"><img src="' + pageLinkDic[toggle][lang].replace('/en/','/').replace('status','public/OrgImg' + lang + '/') + orgas.loc[orgaId, 'imgId'] + '.png" alt="' + orgas.loc[orgaId, 'Bezeichnung ' + lang] + '" title=" ' + getTitle('linkToSrcOrga', orgas.loc[orgaId, 'Bezeichnung ' + lang], lang) + '" style="height:60px; width:148px; border: transparent"/></a>' + "'"
        
        for linkId in srcDic[orgaId]:
            d += 1
            re += '\nsource_url_' + str(c) + appendix[d] + ": '" + getLanguageDependingContent(links, linkId, 'Link ', lang) + "'"
            re += '\nsource_url_text_' + str(c) + appendix[d] + ': ' + txtFct('false', 'true', links.loc[linkId, 'Text ' + lang], lang)
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
                    re += '\n    title: ' + txtFct('false', 'false', meta.loc[index, key + ' 1' + lang], lang[1:3]) 
                elif i[0:2] == 'A_':
                    re += '\n  - series: ' + expressions.loc[i, 'Ausprägung En'].lower()
                    re += '\n    title: ' + txtFct('false', 'false', meta.loc[index, key + ' 1' + lang], lang[1:3])              
            
        else:
            re += keyDict[key].replace('titles','title') + txtFct('false', 'false', meta.loc[index, key + ' 1' + lang], lang[1:3])
            
        
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
            return txtFct('false', 'false', breakYear, lang[1:3])
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
        for INr in sorted(list(set(allStartDatasets.INr))):
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

def getWeatherFct2(index, lang):
    IbNr = meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']
    df = weatherWithIndicatorInfos[(weatherWithIndicatorInfos.IbNr == IbNr)]
    counter = 0
    re, reTp, reTpComplete, reTLComplete, reTL, re3, reHeader, targetYearsH  = '', '', '', '', '', '', '', []
    
    #determine years
    yearsOnYAxis = []
    for y in data[data.IbNr == IbNr].dropna(axis='columns', how='all').columns:
        try: 
            if float(y.replace(',','.')):
                if not meta.loc[index, y]:
                    yearsOnYAxis.append(y)
        except ValueError:
            continue 
    #add empty years
    if len(yearsOnYAxis) > 3:
        if float(yearsOnYAxis[-1].replace(',','.')) % 1 == 0.5:
            lastVal = str(int(float(yearsOnYAxis[-1].replace(',','.')) - 0.5))
        else:
            lastVal = str(yearsOnYAxis[-1])
        [yearsOnYAxis.append(str(y)) for y in range(int(yearsOnYAxis[0]),int(lastVal)) if not str(y) in yearsOnYAxis]
    #add target years
    [yearsOnYAxis.append(str(int(y))) for y in df.Zieljahr if not pd.isnull(y) and str(int(y)) not in yearsOnYAxis]
    yearsOnYAxis.sort()  

    if len(df) > 0:
        for INr in df['INr'].unique():
            years = [str(x) for x in range(2010, 2026)]
            dfI = df[df.INr == INr].dropna(axis='columns', how='all') #df with one indicator only and no columns with nan only
            if len(dfI) > 0:
                #readd some columns
                for column in ['VorherigesZieljahr', 'Gültig bis', 'Gültig seit', 'Spezifikation', 'Zieljahr', 'AnzeigenAb', 'AnzeigenBis']:
                    if not column in dfI.columns:
                        l = [np.nan for x in range(len(dfI))]
                        dfI[column] = l
                        
                counter += 1
                if lang == 'De':
                    re += '\n\nweather_active_' + str(counter) + ': true' 
                re += '\nweather_indicator_' + str(counter) + ': ' + indicators.loc[INr, 'Indikator'] + ' ' + txtFct('false', 'false', indicators.loc[INr, 'Bezeichnung für Plattform ' + lang], lang)
                
                # Years
                years = [str(x) for x in range(2010, 2026)]
                yearCounter = 0
                for year in list(reversed(years)):
                    if year in dfI.columns: 
                        re += '\nweather_indicator_' + str(counter) + '_year_' + string.ascii_lowercase[yearCounter] +": " + year + ""
                        yearCounter += 1
                
                # Actual target
                re += '\n\nweather_indicator_' + str(counter) + '_target: ' + txtFct('false', 'true', indicators.loc[INr, 'Ziel ' + lang], lang)
                
                #-------------------------------------------------------------------------------------    
                # header from here
                if INr != 'Z06_B02_P01_Ib01_I03':
                    targetYearH = ''
                    reHeader += '\n<div>'
                    reHeader += '\n  <div class="my-header">'
                    reHeader += '\n    <label class="default">' + txtFct('false', 'true', indicators.loc[INr, 'Indikator kurz ' + lang], lang) + ': ' 
                    reHeader += txtFct('false', 'true', indicators.loc[INr, 'Ziel kurz ' + lang], lang)
                
                # Loop through all available targets
                targetCounter = 0
                for target in dfI.index:
                    if not pd.isnull(dfI.loc[target, 'Zieljahr']):
                        targetYear = yearsOnYAxis.index(str(int(dfI.loc[target, 'Zieljahr'])))
                        
                    #first lets find the series for which the target is for
                    seriesKey = INr
                    series = indicators.loc[seriesKey, 'Bezeichnung für Plattform En'].lower()
                    if not pd.isnull(dfI.loc[target, 'Spezifikation']):
                        seriesKey = dfI.loc[target, 'Spezifikation']
                        series = expressions.loc[seriesKey, 'Ausprägung En'].lower()
                        
                    
                    targetCounter +=1
                    re += '\n\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + ': '
                    if 'ZielÜbersichtDe' in dfI.columns:
                        re += txtFct('false', 'true', dfI.loc[target, 'ZielÜbersicht' + lang], lang)
                    else:
                        re += txtFct('false', 'true', indicators.loc[INr, 'Ziel ' + lang], lang)
                    
                    # type of target
                    targetType = 'normal'
                   
                    if not pd.isnull(dfI.loc[target, 'Gültig seit']):
                        targetType = 'new'                
                    if not pd.isnull(dfI.loc[target, 'Gültig bis']):
                        targetType = 'old'
                    re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_category: '
                    if target == 'W_1301a_2020' or target == 'W_1301b_2020' or target == 'W_0702b_2020' or target == 'W_0402b_2020':
                        re += 'normal'
                    else: 
                        re += targetType
                        
                    if not pd.isnull(dfI.loc[target, 'Zieljahr']):
                         re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_targetYear: ' + str(int(dfI.loc[target, 'Zieljahr']))
                            
                    if targetType == 'new':
                        re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_validFrom: ' + str(int(dfI.loc[target, 'Gültig seit']))
                    if targetType == 'old':
                        re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_validUntil: ' + str(int(dfI.loc[target, 'Gültig bis']))
                    
                    re += '\n'
                    
                    # items
                    yearCounter = 0
                    for year in list(reversed(years)):
                        if year in dfI.columns:               
                            title = getWeatherTitel(year,{'De':'','En':''}, dfI.loc[target, 'Zieltyp'], dfI.loc[target, year], lang)
                            re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_item_' + string.ascii_lowercase[yearCounter] + ': ' + nanFct(dfI.loc[target, year])
                            re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_item_' + string.ascii_lowercase[yearCounter] + '_title: ' + title
                            re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_item_' + string.ascii_lowercase[yearCounter] + '_valid: ' + getValidFct(year, dfI.loc[target, 'Zieljahr'], dfI.loc[target, 'VorherigesZieljahr'], dfI.loc[target, 'Gültig bis'], dfI.loc[target, 'AktuellGültig?'])
                            yearCounter += 1     
                    if yearCounter == 0:
                        re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_item_a:' 
                    if 'Anmerkung' + lang in dfI.columns:
                        if not pd.isnull(dfI.loc[target, 'Anmerkung' + lang]):
                            re += '\nweather_indicator_' + str(counter) + '_target_' + str(targetCounter) + '_note: ' + txtFct('false', 'true', dfI.loc[target, 'Anmerkung' + lang], lang)
                    
                    # graph_target_points from here
                    if dfI.loc[target, 'InGrafikAnzeigen?']:
                        #if pd.isnull(dfI.loc[target, 'Gültig bis']):
                        # find graph type
                        if pd.isnull(meta.loc[index, 'Grafiktyp 1 Spezifikation']):
                            graphType = meta.loc[index, 'Grafiktyp 1']
                        else:
                            for i in ['1', '2']:
                                if meta.loc[index, 'Grafiktyp ' + i + ' Spezifikation'] == dfI.loc[target, 'Spezifikation']:
                                    graphType = meta.loc[index, 'Grafiktyp ' + i]
                        # start writing
                        reTp += '\n  - '
                        reTL += '\n  - '
                        # series depending?
                        if meta.loc[index, 'Umschalten zwischen Zeitreihen?']:
                            if 'K_SERIES' in list(data[data.INr == INr].xs('Disaggregation 1 Kategorie', axis=1)):
                                reTp += 'series: ' + expressions.loc[dfI.loc[target, 'Spezifikation'], 'Ausprägung En'].lower() + '\n    '
                                reTL += 'series: ' + expressions.loc[dfI.loc[target, 'Spezifikation'], 'Ausprägung En'].lower() + '\n    '
                            else:
                                reTp += 'series: ' + indicators.loc[INr, 'Bezeichnung für Plattform En'].lower() + '\n    '
                                reTL += 'series: ' + indicators.loc[INr, 'Bezeichnung für Plattform En'].lower() + '\n    '
                        
                        #check if there are targets of two indicators in same chart
                        if (len(df['INr'].unique()) > 1 or ('K_SERIES' in list(data[data.INr == INr].xs('Disaggregation 1 Kategorie', axis=1)) and not np.nan in list(data[data.INr == INr].xs('Disaggregation 1 Kategorie', axis=1)))) and not meta.loc[index, 'Umschalten zwischen Zeitreihen?']:
                            color = sdgColors[meta.loc[index, 'Ziel']-1][int(INr[-1])] #- int(INr[-1]) - 6]
                        elif graphType == 'bar' and dfI.loc[target,'Zieltyp'] == 'J':
                            color = '423d3d'
                        else:
                            color = sdgColors[meta.loc[index, 'Ziel']-1][0]
                            
                        if graphType == 'bar' and dfI.loc[target,'Zieltyp'] != 'J':
                            reTp += 'type: box'
                            reTp += '\n    xMin: ' + str(targetYear - (0.3 + len(yearsOnYAxis) * 0.0015))
                            reTp += '\n    xMax: ' + str(targetYear + (0.3 + len(yearsOnYAxis) * 0.0015))
                            reTL += 'type: label'
                            if 'LabelPositionX' in dfI.columns:
                                if not pd.isnull(dfI.loc[target, 'LabelPositionX']):
                                    reTL += '\n    xValue: ' + str(dfI.loc[target, 'LabelPositionX']).replace(',','.')
                                else: reTL += '\n    xValue: ' + str(targetYear).replace(',','.')
                            else:
                                reTL += '\n    xValue: ' + str(targetYear) 
                        elif dfI.loc[target,'Zieltyp'] != 'J':
                            reTL += 'type: label'
                            reTp += 'xValue: ' + str(targetYear)
                            # if dfI.loc[target,'Zieltyp'] == 'J':
                            #     reTp += 'x'
                            #     if 'LabelPositionX' in dfI.columns:
                            #         if not pd.isnull(dfI.loc[target, 'LabelPositionX']):
                            #             reTL += '\n    xValue: ' + str(dfI.loc[target, 'LabelPositionX']).replace(',','.')
                            #else:
                            #    reTp += str(targetYear)
                            
                                #if targetYear == len(yearsOnYAxis)-1:
                                    #reTp += '\n    xAdjust: -7'
                                 #   reTL += '\n    xValue: ' + str(targetYear).replace(',','.')
                                #else: reTL += '\n    xValue: ' + str(targetYear).replace(',','.')
                            if 'LabelPositionX' in dfI.columns:
                                if not pd.isnull(dfI.loc[target, 'LabelPositionX']):
                                    reTL += '\n    xValue: ' + str(dfI.loc[target, 'LabelPositionX']).replace(',','.')
                                else: reTL += '\n    xValue: ' + str(targetYear).replace(',','.')
                            else: reTL += '\n    xValue: ' + str(targetYear).replace(',','.')
                        else:
                            reTL += 'type: label'
                            if 'LabelPositionX' in dfI.columns:
                                if not pd.isnull(dfI.loc[target, 'LabelPositionX']):
                                    reTL += '\n    xValue: ' + str(dfI.loc[target, 'LabelPositionX']).replace(',','.')
                            reTp += "type: 'line'"
                            reTp += '\n    xMin: '
                            if pd.isnull(dfI.loc[target, 'AnzeigenAb']):
                                reTp += '0'
                            else:
                                reTp += str(int(dfI.loc[target, 'AnzeigenAb']) - int(yearsOnYAxis[0]) + 0.5)
                            reTp += '\n    xMax: '
                            if pd.isnull(dfI.loc[target, 'AnzeigenBis']):
                                reTp += str(len(yearsOnYAxis))
                            else:
                                reTp += str(int(dfI.loc[target, 'AnzeigenBis']) - int(yearsOnYAxis[0]))
                            reTp += '\n    yMin: '  + str(dfI.loc[target, 'Zielwert']).replace(',','.')
                            reTp += '\n    yMax: '  + str(dfI.loc[target, 'Zielwert']).replace(',','.')
                            reTp += '\n    borderDash:  [4, 4]'
                         
                            
                         
                            
                        #if 'LabelPositionX' in dfI.columns:
                            #if not pd.isnull(dfI.loc[target, 'LabelPositionX']):
                               # reTL += '\n    xValue: ' + str(dfI.loc[target, 'LabelPositionX']).replace(',','.')
                                
                        
                        if graphType == 'bar' and dfI.loc[target,'Zieltyp'] != 'J':
                            reTp += '\n    yMin: 0'
                            reTp += '\n    yMax: ' + str(dfI.loc[target, 'Zielwert']).replace(',','.') 
                        elif dfI.loc[target,'Zieltyp'] != 'J':
                            reTp += '\n    yValue: ' + str(dfI.loc[target, 'Zielwert']).replace(',','.')                        
                            reTp += '\n    pointStyle: triangle'
                            if dfI.loc[target, 'Zielrichtung'] == 'sinken':
                                reTp += '\n    rotation: 180'
                        
                         
                            
                            
                        if "LabelPositionY" in dfI.columns:
                            if not pd.isnull(dfI.loc[target, 'LabelPositionY']):
                                reTL += '\n    yValue: ' + str(dfI.loc[target, 'LabelPositionY']).replace(',','.')
                        
                        
                         
                        if graphType == 'bar' and dfI.loc[target,'Zieltyp'] != 'J':    
                            reTp += '\n    borderColor: "#' + color + '"'
                            reTp += '\n    backgroundColor: transparent'
                            reTp += '\n    borderDash: [1, 0]'
                            reTp += '\n    borderWidth: 2'
                        else:
                            reTp += '\n    borderColor: "#' + color + '"'
                        reTp += '\n    preset: target_points'
                        reTL += '\n    backgroundColor: transparent'
                        
                        if 'Label' + lang in dfI.columns:
                            if not pd.isnull(dfI.loc[target, 'Label'+lang]):
                                reTL += "\n    content: ['" + dfI.loc[target, 'Label'+lang].replace('\n', "','") + "']"
                            else:
                                if dfI.loc[target,'Zieltyp'] == 'J':
                                    reTL += "\n    content: ['Jährliches Ziel: " + str(dfI.loc[target, 'Zielwert']) + "']"
                                else:
                                    reTL += "\n    content: ['Ziel:','" + str(dfI.loc[target, 'Zielwert']) + "']"
                        else:
                            if dfI.loc[target,'Zieltyp'] == 'J':
                                reTL += "\n    content: ['Jährliches Ziel: " + str(dfI.loc[target, 'Zielwert']) + "']"
                            else:
                                reTL += "\n    content: ['Ziel:','" + str(dfI.loc[target, 'Zielwert']) + "']"
                        reTL += "\n    font: {"
                        reTL += "\n      size: 14"
                        reTL += "\n      }"
                        reTL += "\n    borderColor: transparent"
                        
                        #repeat for J targets
                        # if dfI.loc[target,'Zieltyp'] == 'J':
                        #     save = reTp
                        #     reTp = ''
                        #     for jj in range(len(yearsOnYAxis)):
                        #         ok = False
                        #         if 'AnzeigenAb' in dfI.columns:
                        #             if int(yearsOnYAxis[jj]) >= int(dfI.loc[target, 'AnzeigenAb']):
                        #                 ok = True                     
                        #         elif 'AnzeigenBis' in dfI.columns:
                        #             if int(yearsOnYAxis[jj]) <= int(dfI.loc[target, 'AnzeigenBis']):
                        #                 ok = True 
                        #         else:
                        #             ok = True        
                        #         if ok:    
                        #             reTp += save.replace('xValue: x', 'xValue: ' + str(jj))                                  
                        #            # if jj == len(yearsOnYAxis) - 1:
                        #              #   reTp += '\n    xAdjust: -7' 
                            
                        #-------------------------------------------------------------------------------------    
                        # graph_annotations from here
                        re3 += '\n  - '
                        if meta.loc[index, 'Umschalten zwischen Zeitreihen?']:
                            re3 += 'series: ' + series + '\n    '
                        re3 += 'value: ' + str(dfI.loc[target, 'Zielwert']).replace(',','.')
                        re3 += '\n    label:'
                        #check if there are targets of two indicators in same chart
                        if len(df['INr'].unique()) > 1 and not meta.loc[index, 'Umschalten zwischen Zeitreihen?']:
                            additionalLabel = ' - ' + indicators.loc[INr, 'Indikator kurz ' + lang]
                        else:
                            additionalLabel = ''
                            
                        if 'Zieljahr' in dfI.columns and not pd.isnull(dfI.loc[target, 'Zieljahr']):
                            re3 += '\n      content: ' + transl[lang] + ' ' + str(int(dfI.loc[target, 'Zieljahr'])) + additionalLabel
                        elif 'Label' + lang in dfI.columns:
                            if not pd.isnull(dfI.loc[target, 'Label' + lang]):
                                re3 += '\n      content: ' + dfI.loc[target, 'Label' + lang][:dfI.loc[target, 'Label' + lang].find(':')]
                        else: 
                            re3 += '\n      content: ' + transl[lang + 'EveryYear']
                        re3 += '\n      position: left'
                        re3 += '\n      backgroundColor: transparent'
                        re3 += '\n      color: transparent'
                        re3 += '\n    preset: target_line'
                        re3 += '\n    borderColor: transparent'
                        
                    # header from here
                    if dfI.loc[target, 'AufIndikatorseiteAnzeigen?']:
                        weather, targetType, targetYearH= '', '', ''
                        for year in yearsOnYAxis:
                            if year in dfI.columns and not pd.isnull(dfI.loc[target, year]):
                                weather = weatherLong[dfI.loc[target, year]]
                                targetType = dfI.loc[target, 'Zieltyp']
                                targetYearH = year
                        if not targetYearH in targetYearsH:
                            targetYearsH.append(targetYearH)
                        if weather != '':
                            reHeader += '\n      <a href="' + pageLinkDic[toggle][lang] + '"><img src="https://g205sdgs.github.io/sdg-indicators/public/Wettersymbole/' + weather + '.png" title="' + getWeatherTitel(targetYearH, {'De':'','En':''}, targetType, weather[0], lang) + '" alt="' + getAltWeather(weather, lang) + '"/>'
                            reHeader += '\n      </a>' 
                                                     
                    
                    #use only labels that should be used
                    if dfI.loc[target, 'LabelAnzeigen?']:
                        reTLComplete += reTL
                        reTL = ''
                            
                if INr != 'Z06_B02_P01_Ib01_I03':                
                    reHeader += '\n    </label>'
                    reHeader += '\n  </div>'   
                    reHeader += '\n</div>'
                
                reTpComplete += reTp
                reTp = ''

                     
        if len(targetYearsH) > 1:
                targetYearH = '/'.join(sorted(targetYearsH))    
        reHeader += '\n<div class="my-header-note">' 
        reHeader += '\n  <label class="default"><b>'
        reHeader += headerNoteDic[reHeader.count("/sdg-indicators/public/Wettersymbole/")][lang].replace('XXX', targetYearH)
        reHeader += '\n  </b></label>'
        reHeader += '\n</div>'
                
    for w in weatherLong:
        re = re.replace(': ' + w + '\n', ': ' + weatherLong[w] + '\n')
    if len(reTpComplete) > 0:
        if lang == 'En':
            reTLComplete = reTLComplete.replace('Jährliches Ziel', 'Annual target').replace('Ziel', 'Target')
        reTp = '\ngraph_target_points:' + reTpComplete + reTLComplete
    if len(re3) > 0:
        re3 = '\ngraph_annotations:' + re3
    return re, reTp, re3, reHeader

weatherLong = {'S': 'Sonne', 'W': 'Wolke','L':'Leicht bewölkt','B': 'Blitz'}
headerNoteDic = {0:{'De':'(Keine Bewertung möglich)','En':'(No evaluation possible)'},
                 1:{'De':'(Bewertung aus dem Indikatorenbericht 2022, bezogen auf das Berichtsjahr XXX)','En':'(Evaluation of the indicator report 2022 relating to the reporting year XXX)'},
                 2:{'De':'(Bewertungen aus dem Indikatorenbericht 2022, bezogen auf das Berichtsjahr XXX)','En':'(Evaluations of the indicator report 2022 relating to the reporting year XXX)'},
                 3:{'De':'(Bewertungen aus dem Indikatorenbericht 2022, bezogen auf das Berichtsjahr XXX)','En':'(Evaluations of the indicator report 2022 relating to the reporting year XXX)'}}

def getValidFct (year, targetYear, prevTgtYear, validTill, notValid):
    if not notValid:
        return 'false'
    elif not pd.isnull(prevTgtYear):
        if prevTgtYear >= int(year):
            return 'false'
        else:
            return"true"
    elif not pd.isnull(year) and not pd.isnull(targetYear):
        if int(year) > int(targetYear):
            return 'false'
        else:
            return 'true'
    else:
        return 'true'
    
def getWeatherFct(index, lang):
    c = 0
    re = ''
    for iNr in indicators[indicators.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].index:
        if iNr in weather.index and not pd.isnull(indicators.loc[iNr, 'Bezeichnung für Plattform ' + lang]):
            c += 1
            appendix = ['a','b','c','d','e','f','g','h']
            if lang == 'De':
                re += '\n\nweather_active_' + str(c) + ': true'
            re += '\nweather_indicator_' + str(c) + ': ' + indicators.loc[iNr, 'Indikator'] + ' ' + txtFct('false', 'true', indicators.loc[iNr, 'Bezeichnung für Plattform ' + lang], lang)
            if lang == 'De':
                # -- years -- 
                for t in range(7):
                    if not pd.isnull(weather.loc[iNr, 'Jahr t-' + str(t)]):
                        re += '\nweather_indicator_' + str(c) + '_year_' + appendix[t] + ": " + str(int(weather.loc[iNr, 'Jahr t-' + str(t)])) + ""
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
                    re += '\nweather_indicator_' + str(c) + '_target_old: ' + txtFct('false', 'true', weather.loc[iNr, 'Altes Ziel ' + lang], lang) + '\n'
                    if lang == 'De':
                        re += '\nweather_indicator_' + str(c) + "_target_old_date: '" + str(int(weather.loc[iNr, 'Altes Ziel gültig bis'])) + "'\n"
                    # -- weather --
                    for t in range(7):
                        if t == 0:
                            titleType = 'current'
                        elif not pd.isnull(weather.loc[iNr, 'Jahr t-' + str(t)]):
                            titleType = str(int(weather.loc[iNr, 'Jahr t-' + str(t)]))
                        value = weather.loc[iNr, 'Ws altes Ziel t-' + str(t)]                       
                        if not pd.isnull(value):
                            title = getWeatherTitel(titleType, {'De':'','En':''}, weather.loc[iNr, 'Zieltyp'], value[0] ,lang)
                            if lang == 'De':
                                re += '\nweather_indicator_' + str(c) + '_old_item_' + appendix[t] + ': ' + value
                            re += '\nweather_indicator_' + str(c) + '_old_item_' + appendix[t] + '_title: ' + title                         
                        elif t == 0:
                            re += '\nweather_indicator_' + str(c) + "_old_item_a: '-'"
                re += '\nweather_indicator_' + str(c) + '_target' + new + ': ' + txtFct('false', 'true', indicators.loc[iNr, 'Ziel ' + lang], lang) + '\n'
                
                # -- weather --
                for t in range(7):
                    value = weather.loc[iNr, 'Ws t-' + str(t)]
                    if t == 0:
                            titleType = 'current'
                    elif not pd.isnull(weather.loc[iNr, 'Jahr t-' + str(t)]):
                        titleType = str(int(weather.loc[iNr, 'Jahr t-' + str(t)]))
                    if not pd.isnull(value):
                        title = getWeatherTitel(titleType,{'De':'','En':''}, weather.loc[iNr, 'Zieltyp'], value[0], lang)
                        if lang == 'De':
                            re += '\nweather_indicator_' + str(c) + new + '_item_' + appendix[t] + ': ' + value
                        re += '\nweather_indicator_' + str(c) + new + '_item_' + appendix[t] + '_title: ' + title
                    elif t == 0:
                        re += '\nweather_indicator_' + str(c) + new + "_item_a: '-'"    
            else:                                                   # -- multi targets        
                re += '\nweather_indicator_' + str(c) + '_target: ' + txtFct('false', 'true', indicators.loc[iNr, 'Ziel ' + lang], lang)
                for multiTarget in range(1,5):
                    re += '\n'
                    # -- old multi target? ---
                    new = ''
                    value = weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' ' + lang]
                    if not pd.isnull(value):
                        re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old: ' + txtFct('false', 'true', value, lang)
                        if lang == 'De':
                            re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + "_old_date: '" + str(int(weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' gültig bis'])) + "'"
                            if weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' Jahr'] != 0:
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + "_old_year: '" + str(int(weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' Jahr'])) + "'\n"
                        new = '_new'
                        
                        # -- weather --
                        for t in range(7):
                            value = weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' Ws t-' + str(t)]
                            if t == 0:
                                titleType = 'current'
                            elif not pd.isnull(weather.loc[iNr, 'Jahr t-' + str(t)]):
                                titleType = str(int(weather.loc[iNr, 'Jahr t-' + str(t)]))
                            if not pd.isnull(value):
                                title = getWeatherTitel(titleType, {'De':'','En':''}, weather.loc[iNr, 'Zieltyp'], value[0], lang)
                                if lang == 'De':
                                    re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old_item_' + appendix[t] + ': ' + value
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old_item_' + appendix[t] + '_title: ' + title
                            elif t == 0:
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + "_old_item_a: '-'"
                    if not pd.isnull(weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' ' + lang]):                       
                        re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + ': ' + txtFct('false', 'true', weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' ' + lang], lang)
                        if not pd.isnull(weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' Jahr']):
                            re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + "_year: '" + str(int(weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' Jahr'])) + "'\n"
                        # -- weather --
                        for t in range(7):
                            value = weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' Ws t-' + str(t)]
                            if t == 0:
                                titleType = 'current'
                            elif not pd.isnull(weather.loc[iNr, 'Jahr t-' + str(t)]):
                                titleType = str(int(weather.loc[iNr, 'Jahr t-' + str(t)]))
                            if not pd.isnull(value):
                                title = getWeatherTitel(titleType, {'De':'','En':''}, weather.loc[iNr, 'Zieltyp'], value[0], lang)
                                if lang == 'De':
                                    re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + '_item_' + appendix[t] + ': ' + value
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + '_item_' + appendix[t] + '_title: ' + title   
                            elif t == 0:
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + "_item_a: ''"    
    return re


# -- Text functions ---------
 
def nanFct(inpt):
    if pd.isnull(inpt):
        return ''
    else:
        return inpt

def quotationFct(inpt):
    if ':' in inpt and not ((inpt[0] == "'" and inpt[-1] =="'") or (inpt[0] == '"' and inpt[-1] == '"')):
        if '"' in inpt or '“' in inpt:                
            return "'" + inpt.replace("'",'"') + "'"
        else:
            return '"' + inpt.replace('"',"'") + '"'#.replace('“',"'").replace('„',"'") + '"'
    else:
        return inpt

def replaceFct(dic, inpt, lang):
    for i in dic[lang]:
        inpt = inpt.replace(i,'XXX' + dic[lang][i] + 'XXX')
    inpt = decmark_reg.sub('&nbsp;',inpt) # replace all whitespaces between numeric values
    return inpt.replace('XXX', '')
        
def txtFct (textInpt, withAbb, inpt, lang):
    re = replaceFct(replaceDic, wrappingFct(nanFct(inpt)), lang)
    if textInpt == 'true':
        re = replaceFct(replaceDicTextOnly, wrappingFct(nanFct(re)), lang)      
    if withAbb == 'true':
        re = replaceFct(abbDic, re, lang)
    else:
        re = re.replace('&nbsp;',' ')
    return quotationFct(re)

def undoAbbrFct (text, lang):
    for abb in abbDic[lang]:
        text = text.replace(abbDic[lang][abb], abb)
    return text
     
def wrappingFct(inpt):
    return (inpt)
    #return inpt.replace('\n','<br><br>')
    
def getSdgIndicators(index):
    re = ''
    if not pd.isnull(meta.loc[index, 'SDG1']):
        re += "sdg_indicator: " + meta.loc[index, 'SDG1']
    if not pd.isnull(meta.loc[index, 'SDG2']):            
        re += "\nsdg_indicator2: " + meta.loc[index, 'SDG2']
    return re

# Adding abbreviations to replaceDic
abbDic = {'De':{}, 'En':{}}
for abb in abbreviations.index:
    for lang in ['De', 'En']:
        if not pd.isnull(abbreviations.loc[abb, 'Klartext' + lang]):
            for context in [[' ',' '],
                            ['>',' '],
                            ['nbsp;','<'],
                            ['nbsp;',' '],
                            ['nbsp;','.'],
                            ['nbsp;',','],
                            ['nbsp;','-'],
                            ['nbsp;',')'],
                            [' ','&nbsp;'],
                            ['(',')'],
                            [' ','-'],
                            [' ','–'],
                            ['„','-'],
                            [' ','_'],
                            ['-',')'],
                            ['-',' '],
                            ['-',')'],
                            [' ','.'],
                            [' ','+'],
                            [' ',','],
                            ['(',' '],
                            [' ',')'],
                            ['(','-'],
                            [' ',"'"],
                            [' ',"’"]]:              
                abbDic[lang][context[0] + abb + context[1]] = context[0] + '<abbr title="' + abbreviations.loc[abb, 'Klartext' + lang] + '">' + abb + "</abbr>" + context[1]

# --------------------------------------
for page in meta.index:                                                             # page = 07.1.a,b
    
    print(page)
    #if page[:2]=="07":
       # print(getWeatherFct2(page, 'De'))
    
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
    \nnational_indicator_available: " + txtFct('false', 'true', meta.loc[page, 'Tab_4a_Indikatorenblätter.BezDe'], 'De') + "\
    \n\ndns_indicator_definition: " + txtFct('true', 'true', meta.loc[page, 'DefinitionDe'], 'De') + "\
    \n\ndns_indicator_intention: "+ txtFct('true', 'true', meta.loc[page, 'IntentionDe'], 'De') +"\
    \n\ndata_state: " + dataState['De'] + "\
    \n\nindicator_name: " + txtFct('false', 'false', meta.loc[page, 'Tab_4a_Indikatorenblätter.BezDe'], 'De') + "\
    \nsection: " + txtFct('false', 'true', meta.loc[page, 'Tab_2a_Bereiche.BezDe'], 'De') + "\
    \npostulate: " + txtFct('false', 'true', meta.loc[page, 'Tab_3a_Postulate.BezDe'], 'De') + "\
    \ntarget_id: " + getTargetId(meta.loc[page, 'Tab_3a_Postulate.PNr']) + "\
    \nprevious: " + getFilename(getPreviousIndex(page, 'prev')) + "\
    \nnext: " + getFilename(getPreviousIndex(page, 'next')) + "\
    \n\n#content \
    \ncontent_and_progress: " + addLinkFct(txtFct('true', 'true', "<b>" + contentText['De'] + "</b><br>" + getContentFct(page, 'De'), 'De'), 'De').replace('<br>','<br><br>') + "\
    \n\n#Sources\
    \n" + getSourcesFct(page, 'De') + "\
    \n\n#Status\
    \n" + getWeatherFct2(page, 'De')[0] + "\
    \n" + getWeatherFct2(page, 'De')[1] + "\
    \n\ndata_show_map: " + str(meta.loc[page, 'Karte anzeigen?']).lower() + "\
    \ncopyright: '&copy; Statistisches Bundesamt (Destatis), " + year + "'\
    \n\n" + getFootnotes(page, 'De') + "\
    \n\n" + getSpecifiedStuff(page,'Grafiktitel', 5, 'title', '', ' De') + "\
    \n\n" + getSpecifiedStuff(page,'Untertitel', 5, 'title', '', ' De') + "\
    \n\n" + getWeatherFct2(page, 'De')[2] + "\
    \n\n" + getSpecifiedStuff(page, 'Dezimalstellen', 4, 'decimals', '', '') +"\
    \n\nspan_gaps: " + str(meta.loc[page, 'Lücken füllen?']).lower() + "\
    \nshow_line: " + str(meta.loc[page, 'Linie anzeigen?']).lower() + "\
    \n\n" +  getSpecifiedStuff(page, 'Grafiktyp', 3, 'type', '', '') + "\
    " + getStartValues(page) +"\
    \n\n" + getSpecifiedStuff(page, 'Achsenlimit', 4, 'minimum', 'maximum', '') + "\
    \n\n" + getSpecifiedStuff(page, 'Schrittweite y-Achse', 4, 'step', '', '') + "\
    \n\n" + getSpecifiedStuff(page, 'Zeitreihenbruch', 4, 'value', '', '') + "\
    " + getStackedDisagg(page) + "\
    " + getSomething('x_axis_label', meta.loc[page,'x-Achsenbezeichnung De']) + "\
    " + getSomething('national_geographical_coverage', meta.loc[page,'Geografische Abdeckung De']) + "\
    \n---\n\n" + getWeatherFct2(page, 'De')[3]) #getHeader(page, 'De'))
    # \n\n" + getAnnotations(page, 'De') + "\
    # \n\n" + getWeatherFct2(page, 'De')[2] + "\
    fileEn.write("---\n\nlanguage: en\
    \nnational_indicator_available: " + txtFct('false', 'true', meta.loc[page, 'Tab_4a_Indikatorenblätter.BezEn'], 'En') + "\
    \n\ndns_indicator_definition: " + txtFct('true', 'true', meta.loc[page, 'DefinitionEn'], 'En') + "\
    \n\ndns_indicator_intention: "+ txtFct('ture', 'true', meta.loc[page, 'IntentionEn'], 'En') +"\
    \n\ndata_state: " + dataState['En'] + "\
    \n\nindicator_name: " + txtFct('false', 'false', meta.loc[page, 'Tab_4a_Indikatorenblätter.BezEn'], 'En') + "\
    \nsection: " + txtFct('false', 'true', meta.loc[page, 'Tab_2a_Bereiche.BezEn'], 'En') + "\
    \npostulate: " + txtFct('false', 'true', meta.loc[page, 'Tab_3a_Postulate.BezEn'], 'En') + "\
    \n\n#content \
    \ncontent_and_progress: " + txtFct('true', 'true', "<b>" + contentText['En'] + "</b><br>" + getContentFct(page, 'En'), 'En').replace('<br>','<br><br>') + "\
    \n\n#Sources\
    \n" + getSourcesFct(page, 'En') + "\
    \ncopyright: '&copy; Federal Statistical Office (Destatis), " + year + "'\
    \n\n" + getFootnotes(page, 'En') + "\
    \n\n" + getSpecifiedStuff(page,'Grafiktitel', 5, 'title', '', ' En') + "\
    \n\n" + getSpecifiedStuff(page,'Untertitel', 5, 'title', '', ' En') + "\
    \n\n" + getWeatherFct2(page, 'En')[2] + "\
    " + getSomething('x_axis_label', meta.loc[page,'x-Achsenbezeichnung En']) + "\
    " + getSomething('national_geographical_coverage', meta.loc[page,'Geografische Abdeckung En']) + "\
    \n" + getWeatherFct2(page, 'En')[0] +"\
    \n" + getWeatherFct2(page, 'En')[1] +"\
    \n---\n\n" + getWeatherFct2(page, 'En')[3])
    
    fileEn.close()
    file.close()