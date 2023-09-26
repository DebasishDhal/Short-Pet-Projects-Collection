import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

link = "https://en.wikipedia.org/wiki/List_of_German_exonyms_for_places_in_Estonia" #The names are present in table format. Easy to scrap.

page = requests.get(link)
soup = BeautifulSoup(page.content, 'lxml')

table = soup.find_all('table')[0]

df = pd.read_html(str(table))[0]
df.columns = ['estonian', 'german', 'notes']

del df['notes']

#Swap columns
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

print(df.head())

saving_adress = r"\Users\HP\OneDrive\Desktop\Python\Pet_Projects\web_scrapping_wiki\datasets"
df.to_csv(os.path.join(saving_adress, "german_estonian.csv"), index=False)
