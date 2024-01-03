#Goal -  Scrap the German exonyms for places in Slovenia from the website given below.

link = 'https://de.wikipedia.org/wiki/Liste_deutscher_Namen_f%C3%BCr_slowenische_Orte'

from bs4 import BeautifulSoup
import requests
import re

r = requests.get(link)
soup = BeautifulSoup(r.text, 'lxml')

div = soup.find('div', class_='mw-content-ltr mw-parser-output')
# print(div)
german_name_list = []
slovene_name_list = []

ul_list = div.find_all('ul')[3:-3]
count = 0
for ul in ul_list:
    li_list = ul.find_all('li')

    for li in li_list:
        if ':' not in li.text:
            continue

        name = li.text

        if 'auch:' in name: #This thing is such a pain.
            name = re.sub(r'\(auch:.*?\)', '', name) #if name = 'random (auch: more_random) bizzare', this will change it to 'random bizzare'. auch means 'also' in German. Basically more than one German name of a place, which I don't want
        
        slovene_name = name.split(':')[0].strip()
        try:
            german_name = name.split(':')[1].strip()
        except:
            continue


        if ',' in german_name:
            german_name = german_name.split(',')[0].strip()
        

        german_name = re.sub(r'\((.*?)\)', r'\1', german_name) #Sometimes the larger location (i.e. city/county) is given within ( and ) alongisde a smaller locality's name, I'm including it for more context.
        slovene_name = re.sub(r'\((.*?)\)', r'\1', slovene_name) 

        if ';' in german_name:
            german_name = german_name.split(';')[0].strip()

        if german_name.endswith('St'):
            continue

        count += 1
        if ' (' in german_name:
            german_name = german_name.split(' (')[0].strip()
        if ' (' in slovene_name:
            slovene_name = slovene_name.split(' (')[0].strip()

        german_name_list.append(german_name)
        slovene_name_list.append(slovene_name)

        print(slovene_name,':', german_name)

import pandas as pd

df = pd.DataFrame({'german': german_name_list,'slovene': slovene_name_list})

df.to_csv(r'C:\Users\HP\OneDrive\Desktop\Python\Pet_Projects\web_scrapping_wiki\datasets\german_slovene.csv', index=False)
