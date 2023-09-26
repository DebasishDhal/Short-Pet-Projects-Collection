import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

link = "https://de.wikipedia.org/wiki/Liste_deutscher_Bezeichnungen_lettischer_Orte" #This is the most detailed German-Latvian name page I found, it's in German.

page = requests.get(link)
soup = BeautifulSoup(page.content, 'lxml')

divs = soup.find_all('div', class_='mw-parser-output')

div = divs[0]

uls = div.find_all('ul')

# print(len(uls))

count = 0

german_name_list = []
latvian_name_list = []
for ul in uls[0:]:
    # print(ul.text)
    lis = ul.find_all('li')
    for li in lis:

        latvian_name = None
        german_name = None

        if ":" not in li.text or len(li.text) > 130:
            continue
        
        german_name = li.text.split(":")[0].strip().split(",")[0]
        latvian_name = li.text.split(":")[1].strip().split(",")[0]
        
        if "(" in german_name:
            german_name = german_name.split("(")[0].strip()

        if "/" in german_name:
            german_name = german_name.split("/")[0].strip()     #Wiebersholm / Wiebertsholm (ehem. Insel : Viberta sala

        if "(" in latvian_name:
            latvian_name = latvian_name.split("(")[0].strip()
        
        if "/" in latvian_name:
            latvian_name = latvian_name.split("/")[0].strip()
        count += 1

        german_name_list.append(german_name)
        latvian_name_list.append(latvian_name)
        print(german_name,":",latvian_name)

print(count)

df = pd.DataFrame({'german': german_name_list, 'latvian': latvian_name_list})
df.dropna(inplace=True)
df=df.reset_index(drop=True)

print(df.sample(10))

saving_adress = r"\Users\HP\OneDrive\Desktop\Python\Pet_Projects\web_scrapping_wiki"

df.to_csv(os.path.join(saving_adress, "german_latvian.csv"), index=False)
