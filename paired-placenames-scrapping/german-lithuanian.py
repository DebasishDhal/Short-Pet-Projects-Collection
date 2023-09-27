import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import os

link = "https://de.wikipedia.org/wiki/Liste_deutscher_Bezeichnungen_litauischer_Orte" #This page has the most comprehensive list of german exonyms for lithuanian places.


source = requests.get(link).text
soup = BeautifulSoup(source, 'lxml')
divs = soup.find_all('div', class_='mw-parser-output')

german_name_list = []
lithuanian_name_list = []

div = divs[0]
uls = div.find_all('ul')

count = 0

escape_chars = list(string.digits) + list(string.punctuation)
escape_chars.remove("-")
switch = False

for ul in uls:

    if not ul:
        continue

    lis = ul.find_all('li')
    for li in lis:
        if "Kreis" not in li.text and "Stadtkreis" not in li.text:
            switch = True
        else:
            switch = False

        if ":" not in li.text:
            continue
        
        if switch:
            german_name = li.text.split(":")[1].strip()
            lithuanian_name = li.text.split(":")[0].strip()

        else:
            german_name = li.text.split(":")[0].strip()
            lithuanian_name = li.text.split(":")[1].strip()

        german_name = german_name.split("Kreis")[0].strip()
        german_name = german_name.split("Stadtkreis")[0].strip()

        if "/" in german_name:
            german_name = german_name.split("/")[0].strip()

        if "," in german_name:
            german_name = german_name.split(",")[0].strip()

        if "(" in german_name:
            continue


        
        
        if "," in lithuanian_name:
            lithuanian_name = lithuanian_name.split(",")[0].strip()

        if "/" in lithuanian_name:
            lithuanian_name = lithuanian_name.split("/")[0].strip()

        if "(" in lithuanian_name:
            continue

        # print(german_name +" : "+ lithuanian_name)

        german_name_list.append(german_name)
        lithuanian_name_list.append(lithuanian_name)
        count += 1
        
print(count)

df = pd.DataFrame({"german": german_name_list, "lithuanian": lithuanian_name_list})

for i in df.columns:
    df[i] = df[i].str.replace(r'\(.*\)', '', regex=True).str.strip()

for i in range(len(df)):
    for j in df.columns:
        if any(char in escape_chars for char in df.loc[i, j]):
            # print(df.loc[i, j])
            df.drop(i, inplace=True)
            break

print(len(df))

print(df.isnull().sum()) # Check for null values

with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(df)

saving_adress = r"\Users\HP\OneDrive\Desktop\Python\Pet_Projects\web_scrapping_wiki\datasets"
df.to_csv(os.path.join(saving_adress, "german_lithuanian.csv"), index=False)
print("Done")
