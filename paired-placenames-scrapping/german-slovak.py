link = "https://de.wikipedia.org/wiki/Liste_deutscher_Bezeichnungen_slowakischer_Orte"

from bs4 import BeautifulSoup
import requests
import re

r = requests.get(link)
source = requests.get(link).text
soup = BeautifulSoup(source, 'lxml')
# print(soup.prettify())

div = soup.find('div', class_='mw-content-ltr mw-parser-output')
# print(div.prettify())

ul = div.find_all('ul')
print(len(ul))
ul = ul[1:-3] #First ul is useless, so are the last three ul's which are some footnotes.
# print(ul)
# print(ul.prettify())

li = ul[-3].find_all('li')
# print(li)

count = 0
german_name_list = []
slovak_name_list = []

for li in ul:
    for item in li:
        text = item.text.strip()
        if ':' not in text:
            continue
        count += 1
        german_name = text.split(':')[0].strip()
        slovak_name = text.split(':')[1].strip()
        if '?' in slovak_name:
            continue
        if ',' in slovak_name:
            slovak_name = slovak_name.split(',')[0].strip()
        if '(' in slovak_name:
            slovak_name = slovak_name.split('(')[0].strip()
        if '\n' in slovak_name:
            slovak_name = slovak_name.split('\n')[0].strip()
        if ' - ' in slovak_name:
            slovak_name = slovak_name.split(' - ')[0].strip()

        german_name = re.sub(r'\[(.*?)\]', r'\1', german_name) #Blasensteinsanktnik[o]la[u]s => Blasensteinsanktnikolaus
        german_name = re.sub(r'^-','',german_name)  # -Kahlenberg => Kahlenberg

        german_name_list.append(german_name)
        slovak_name_list.append(slovak_name)  

        # print(german_name,':',slovak_name)

import pandas as pd

df = pd.DataFrame({'german':german_name_list, 'slovak':slovak_name_list})
df.to_csv(r'C:\Users\HP\OneDrive\Desktop\Python\Pet_Projects\web_scrapping_wiki\datasets\german_slovak.csv', index=False)

print(count)
df
