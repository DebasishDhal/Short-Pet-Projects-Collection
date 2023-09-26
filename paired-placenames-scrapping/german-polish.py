import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import string

link = "https://de.wikipedia.org/wiki/Liste_deutscher_Bezeichnungen_polnischer_Orte" #This German page had the best collection. Almost 10,000 rows. The Polish page had ~ 3000 rows only.

page = requests.get(link)
soup = BeautifulSoup(page.content, 'lxml')

divs = soup.find_all('div', class_='mw-parser-output')
div = divs[0]

uls = div.find_all('ul')

count = 0
unwanted_chars = list(string.punctuation)+list(string.digits)+["und"]

german_name_list = []
polish_name_list = []
for ul in uls[0:]:
    lis = ul.find_all('li')
    for li in lis:

        polish_name = None
        german_name = None

        if ":" not in li.text or len(li.text) > 130 or len(re.findall(r':', li.text))!=1:
            continue
        
        german_name = li.text.split(":")[0].strip().split(",")[0]
        polish_name = li.text.split(":")[1].strip()
        
        if "(" in german_name:
            german_name = german_name.split("(")[0].strip()

        if "/" in german_name:
            german_name = german_name.split("/")[0].strip()     

        if "(" in polish_name:
            polish_name = polish_name.split("(")[0].strip()

        if ")" in polish_name:
            polish_name = polish_name.split(")")[1].strip()
        
        if "/" in polish_name:
            polish_name = polish_name.split("/")[0].strip()

        if "," in polish_name:
            polish_name = polish_name.split(",")[0].strip()

#Ensure that no punctuation or digits are in either the german name or in the polish name
        reject = False
        for char in unwanted_chars:
            if (char in german_name) or (char in polish_name):
                reject = True
                break
        
        if reject:
            continue
        
        count += 1
        german_name_list.append(german_name)
        polish_name_list.append(polish_name)

        print(german_name,":",polish_name)
print(count)

df = pd.DataFrame({'german': german_name_list, 'polish': polish_name_list})
print(len(df))
df.head()
df.isnull().sum()

df.dropna(inplace=True)

saving_adress = r"\Users\HP\OneDrive\Desktop\Python\Pet_Projects\web_scrapping_wiki\datasets"

df.to_csv(os.path.join(saving_adress, "german_polish.csv"), index=False)
