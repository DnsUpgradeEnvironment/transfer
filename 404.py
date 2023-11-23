# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 11:11:31 2023

@author: Dauerausleihe04
"""


import re
import urllib
import requests
import pandas as pd
from bs4 import BeautifulSoup


#sdg_or_dns = 'sdg'
sdg_or_dns = 'dns'

live_or_test = 'test'
#live_or_test = 'live'

de_or_en = ''
#de_or_en = 'en/'

base_paths = {
                'sdg':{
                    'test': 'https://sdgtestenvironment.github.io/sdg-indicators/',
                    'live': 'https://sdg-indikatoren.de/'},
                'dns':{
                    'test': 'https://dnstestenvironment.github.io/dns-indicators/',
                    'live': 'https://dns-indikatoren.de/'}}
pages = {'sdg': ['', 'reporting-status', 'platform', 'navigation', 'guidance', 'facts_agenda', 'facts_dns', 'publications', 'imprint'],
         'dns': ['', 'status_summary', 'status', 'about_platform', 'about_joint_action', 'about_guidance', 'publications_reports', 'publications_strategy', 'publications_strategy_laender', 'publications_other', 'imprint']}


# meta_path = {'sdg': 'C:\\Users\\Dauerausleihe04\\Documents\\SDG\\FilesFromDatabase\\transfer\\Exp_3-n_NRP_Meta.xlsx',
#              'dns': 'C:\\Users\\Dauerausleihe04\\Documents\\MoBosse\\DnsUpgradeEnvironment\\transfer\\Exp_meta.xlsx'}

if sdg_or_dns == 'sdg':
    meta = pd.read_excel('C:\\Users\\Dauerausleihe04\\Documents\\SDG\\FilesFromDatabase\\transfer\\Exp_3-n_NRP_Meta.xlsx', index_col=0)
    
    for indicator in meta.index:
        if meta.loc[indicator, 'additionalInformation']:
            pages[sdg_or_dns].append(meta.loc[indicator, 'Indikator'].replace('.','-'))
    
        
brokenLinks = {}
testedLinks = []
counter = 0
for page_to_check in pages[sdg_or_dns]:
    page = base_paths[sdg_or_dns][live_or_test] + de_or_en + page_to_check
    brokenLinks[page] = []

    html_page = urllib.request.urlopen(page)
    soup = BeautifulSoup(html_page, "html.parser")

    for linkToCheck in soup.findAll('a', attrs={'href': re.compile("^https://")}):
        counter += 1
        a = str(linkToCheck)
        b = a[a.find("href=")+6:a[a.find("href=")+6:].find('"')+a.find("href=")+6]

        if not b in testedLinks:
            print(counter, ' ', b)
            try:
                requestObj = requests.get(str(b));
                if(requestObj.status_code == 404):
                    print('Broken: ', b)
                    brokenLinks[page].append(str(b))
                    testedLinks.append(str(b))
                else:
                    
                    testedLinks.append(str(b))
            except Exception as e:
                print("ERROR: " + str(e))
        