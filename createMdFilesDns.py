# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:40:46 2022

@author: Dauerausleihe04
"""

import pandas as pd
import codecs
import os

path = os.getcwd()

toggle = 'Prüf'
#toggle = 'Staging'

if toggle == 'Staging':
    targetPath = path.replace('\\transfer', '\dns-data\meta')
else:   
    targetPath = path.replace('\\transfer','\dns-data\meta')
    

meta = pd.read_excel(path + '\\Exp_meta.xlsx')
meta.set_index('Tab_4a_Indikatorenblätter.Indikatoren', inplace = True)

links = pd.read_excel(path + '\\Tab_9a_Links.xlsx',  index_col=0)
orgas = pd.read_excel(path + '\\Tab_8a_Quellen.xlsx',  index_col=0)
indicators = pd.read_excel(path + '\\Tab_5a_Indikatoren.xlsx',  index_col=0)
weather = pd.read_excel(path + '\\Tab_5b_Wetter.xlsx',  index_col=0)

# ----- Variables -----------

dataState = {'De': 'Der Indikatorenbericht 2021 hat den Datenstand 31.12.2020. Die Daten auf der DNS-Online Plattform werden regelmäßig aktualisiert, sodass online aktuellere Daten verfügbar sein können als im Indikatorenbericht 2021 veröffentlicht.',
             'En': 'The data published in the indicator report 2021 is as of 31.12.2020. The data shown on the DNS-Online-Platform is updated regularly, so that more current data may be available online than published in the indicator report 2021.'}

contentText = {'De': 'Text aus dem Indikatorenbericht 2021',
               'En': 'Text from the Indicator Report 2021'}

replaceDic = {' %': '&nbsp;%'}

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

# ----- Functions -----------

def getTitle(case, content, lang):
    return titleDic[case][lang]['pre'] + content + titleDic[case][lang]['post']


def getTargetId(BNr):
    re = list(BNr.replace('Z','').replace('_B','.').replace('_P','.'))
    for i in [6,3,0]:
        if re[i] == '0':
            re[i] = ''
    return "".join(re)

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

def replaceFct(inpt):
    for i in replaceDic:
        if i in inpt:
            inpt = inpt.replace(i, replaceDic[i])
    return inpt
        

def txtFct (inpt):
    return quotationFct(replaceFct(wrappingFct(nanFct(inpt))))
        

def wrappingFct(inpt):
    return inpt.replace('\n','<br><br>')
    

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
        
def getFilename(index):
    filename = index.lstrip('0').replace('.','-').replace(',','')                    # filename = 7-2-ab
    if filename[-1].isnumeric():
        filename += '-a'
    return filename

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
        print(orgaId)
        c += 1
        d = -1
        appendix = ['','b','c','d','e','f']
        re += '\nsource_active_' + str(c) + ': true'
        re += '\nsource_organisation_' + str(c) + ': ' + orgas.loc[orgaId, 'Bezeichnung lang ' + lang]
        re += '\nsource_organisation_' + str(c) + '_short: ' + orgas.loc[orgaId, 'Bezeichnung ' + lang]
        re += '\nsource_organisation_logo_' + str(c) + ': ' + "'" + '<a href="' + getLanguageDependingContent(orgas, orgaId, 'Homepage ', lang) + '"><img src="' + getImgSourcePath(lang) + orgas.loc[orgaId, 'imgId'] + '.png" alt="' + orgas.loc[orgaId, 'Bezeichnung ' + lang] + '" title=" ' + getTitle('linkToSrcOrga', orgas.loc[orgaId, 'Bezeichnung ' + lang], lang) + '" style="height:60px; width:148px; border: transparent"/></a>' + "'"
        for linkId in srcDic[orgaId]:
            d += 1
            re += '\nsource_url_' + str(c) + appendix[d] + ': ' + getLanguageDependingContent(links, linkId, 'Link ', lang)
            re += '\nsource_url_text_' + str(c) + appendix[d] + ': ' + links.loc[linkId, 'Text ' + lang]
        re += '\n'  
    return re




def getImgSourcePath(lang):
    if lang == 'De':
        return 'https://g205sdgs.github.io/sdg-indicators/public/logos/'
    else:
        return 'ttps://g205sdgs.github.io/sdg-indicators/public/logosEn/'

def getLanguageDependingContent(df, index, key, lang):
    if lang == 'De':
        otherLang = 'En'
    else: 
        otherLang = 'De'
    if not pd.isnull(df.loc[index, key + lang]):
        return df.loc[index, key + lang]
    elif not pd.isnul(df.loc[index, key + otherLang]):
        return df.loc[index, key + otherLang]
    else:
        return ''
    
def getWeatherFct(index, lang):
    c = 0
    re = ''
    for iNr in indicators[indicators.IbNr == meta.loc[index, 'Tab_4a_Indikatorenblätter.IbNr']].index:
        if iNr in weather.index:
            c += 1
            appendix = ['a','b','c','d','e','f','g','h']
            re += '\nweather_active_' + str(c) + ': true'
            re += '\nweather_indicator_' + str(c) + ': ' + indicators.loc[iNr, 'Indikator'] + ' ' + indicators.loc[iNr, 'Indikator ' + lang]
            
            # -- years -- 
            for t in range(7):
                if not pd.isnull(weather.loc[iNr, 'Jahr t-' + str(t)]):
                    re += '\nweather_indicator_' + str(c) + '_year_' + appendix[t] + ':  ' + str(weather.loc[iNr, 'Jahr t-' + str(t)])
            re += '\n'
            
            # -- multiple targets? ---
            if pd.isnull(weather.loc[iNr, 'Etappenziel 1 Jahr']):   # -- single target
                # -- old single target? ---
                new = ''
                value = weather.loc[iNr, 'Altes Ziel ' + lang]
                if not pd.isnull(value):
                    new = '_new'
                    re += '\nweather_indicator_' + str(c) + '_target_old: ' + indicators.loc[iNr, 'Altes Ziel ' + lang] + '\n'
                    re += '\nweather_indicator_' + str(c) + '_target_old_date: ' + indicators.loc[iNr, 'Altes Ziel gültig bis'] + '\n'
                    # -- weather --
                    for t in range(7):
                        value = weather.loc[iNr, 'Ws altes Ziel t-' + str(t)]
                        if not pd.isnull(value):
                            re += '\nweather_indicator_' + str(c) + '_old_item_' + appendix[t] + ':  ' + value
                    re += '\n'
                re += '\nweather_indicator_' + str(c) + '_target' + new + ': ' + indicators.loc[iNr, 'Ziel ' + lang] + '\n'
                # -- weather --
                for t in range(7):
                    value = weather.loc[iNr, 'Ws t-' + str(t)]
                    if not pd.isnull(value):
                        re += '\nweather_indicator_' + str(c) + new + '_item_' + appendix[t] + ':  ' + value
                re += '\n' 
            
            
            else:                                                   # -- multi targets
            
                re += '\nweather_indicator_' + str(c) + '_target: ' + indicators.loc[iNr, 'Ziel ' + lang]
                for multiTarget in range(1,4):
                    # -- old multi target? ---
                    new = ''
                    value = weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' ' + lang]
                    if not pd.isnull(value):
                        re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old: ' + value
                        re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old_date: ' + str(int(weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' gültig bis'])) + '\n'
                        re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old_year: ' + str(int(weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' Jahr'])) + '\n'
                        new = '_new'
                        # -- weather --
                        for t in range(7):
                            value = weather.loc[iNr, 'Altes Etappenziel ' + str(multiTarget) + ' Ws t-' + str(t)]
                            if not pd.isnull(value):
                                re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + '_old_item_' + appendix[t] + ':  ' + value
                        re += '\n'
                                           
                    re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + ': ' + weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' ' + lang]
                    re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + '_year: ' + str(int(weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' Jahr'])) + '\n'
                    # -- weather --
                    for t in range(7):
                        value = weather.loc[iNr, 'Etappenziel ' + str(multiTarget) + ' Ws t-' + str(t)]
                        if not pd.isnull(value):
                            re += '\nweather_indicator_' + str(c) + '_target_' + str(multiTarget) + new + '_item_' + appendix[t] + ':  ' + value
                    re += '\n'
    return re

# --------------------------------------
for page in meta.index:                                                             # page = 07.1.a,b
    
    print(page)
    
    file = codecs.open(targetPath + '\\'+ getFilename(page) + '.md', 'w', 'utf-8')
    fileEn = codecs.open(targetPath + '\\en\\' + getFilename(page) + '.md', 'w', 'utf-8')
    
    file.write("---\nlayout: indicator\
    \nindicator: '" + getFilename(page).replace('-','.') + "'\
    \nindicator_display: '" + page.lstrip('0').replace(',',', ') + "'\
    \nindicator_sort_order: '" + getFilename(page) + "'\
    \npermalink: /" + getFilename(page) + "/\
    \nsdg_indicator: " + nanFct(meta.loc[page, 'SDG1']) + "\
    \nsdg_indicator2: " + nanFct(meta.loc[page, 'SDG2']) + "\
    \n\n#\nreporting_status: complete\
    \npublished: true\
    \ndata_non_statistical: false\
    \n\n\n#Metadata\
    \nnational_indicator_available: " + txtFct(meta.loc[page, 'Tab_4a_Indikatorenblätter.BezDe']) + "\
    \n\ndns_indicator_definition: " + txtFct(meta.loc[page, 'DefinitionDe']) + "\
    \n\ndns_indicator_intention: "+ txtFct(meta.loc[page, 'IntentionDe']) +"\
    \n\ndata_state: " + dataState['De'] + "\
    \n\nindicator_name: " + txtFct(meta.loc[page, 'Tab_4a_Indikatorenblätter.BezDe']) + "\
    \nsection: " + txtFct(meta.loc[page, 'Tab_2a_Bereiche.BezDe']) + "\
    \npostulate: " + txtFct(meta.loc[page, 'Tab_3a_Postulate.BezDe']) + "\
    \ntarget_id: " + getTargetId(meta.loc[page, 'Tab_3a_Postulate.PNr']) + "\
    \nprevious: " + getFilename(getPreviousIndex(page, 'prev')) + "\
    \nnext: " + getFilename(getPreviousIndex(page, 'next')) + "\
    \n\n#content \
    \ncontent_and_progress: <i>" + contentText['De'] + "</i>" + txtFct(meta.loc[page, 'InhaltDe']) + "\
    \n\nSources\
    \n" + getSourcesFct(page, 'De') +"\
    \n\n#Status\
    \n" + getWeatherFct(page, 'De'))
    
    fileEn.close()
    file.close()