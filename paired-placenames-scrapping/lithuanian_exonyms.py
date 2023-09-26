#Output - TABLE CONTAINING EXONYMS OF LITHUANIAN PLACES IN RUSSIAN, POLISH, GERMAN, YIDDISH AND LATVIAN. Len(Table) = 102

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

link = "https://en.wikipedia.org/wiki/Names_of_Lithuanian_places_in_other_languages"

r = requests.get(link)
soup = BeautifulSoup(r.content, "lxml")

table = soup.find_all("table")[0]

df = pd.read_html(str(table))[0] #Easy way to get the table into a dataframe
df.columns =    ["lithuanian", "polish", "russian", "bel_cyr", "bel_lat", "yiddish", "german", "latvian"]

def original_script_extractor(row):
    if type(row) != str:
        return row
    
    if "/" in row:
        try:
            return row.split('/')[0].strip()
        except:
            return row
    else:
        return row
    
def latin_script_extractor(row):
    if type(row) != str:
        return row
    
    if "/" in row:
        try:
            return row.split('/')[1].strip()
        except:
            return row
    else:
        return row


df['rus_cyr'] = df['russian'].apply(original_script_extractor)
df['yid_heb'] = df['yiddish'].apply(original_script_extractor)
df['rus_lat'] = df['russian'].apply(latin_script_extractor)
df['yid_lat'] = df['yiddish'].apply(latin_script_extractor)

del df['russian']
del df['yiddish']

for i in df.columns: #Some rows have more than one entries, with () being used to store the 2nd entry, this will delete whatever is there inside the ()
    df[i] = df[i].str.replace(r'\(.*\)', '', regex=True).str.strip()
        
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(df)

print(df.isnull().sum())

saving_adress = r"\Users\HP\OneDrive\Desktop\Python\Pet_Projects\web_scrapping_wiki\datasets"
df.to_csv(os.path.join(saving_adress, "lithuanian_place_exonyms.csv"), index=False)
