import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

link = "https://en.wikipedia.org/wiki/List_of_German_names_for_places_in_the_Czech_Republic" #The wiki has the names grouped by alphabets. 
source = requests.get(link).text
soup = BeautifulSoup(source, 'lxml')

divs = soup.find_all('div', class_='div-col')

german_name_list = []
czech_name_list = []

for div in divs[0:]:
    ul = div.find('ul')
    german_name = None
    czech_name = None

    if ul:
        li = ul.find_all('li')
        # count = 1
        for item in li[0:]:

            if ":" not in item.text:
                continue
            german_name = item.text.split(':')[0].strip()
            czech_name = item.text.split(':')[1].strip()

            if german_name[0] == "(" and german_name[-1] == ")":
                continue

            if "(" in german_name:
                if german_name[0] == "(" and german_name[-1] == ")":
                    german_name = german_name[1:-1]
                else:
                    german_name = german_name.split('(')[0].strip()

            if "," in czech_name:
                czech_name = czech_name.split(',')[0].strip()
            
            if "\n" in czech_name:
                czech_name = czech_name.split('\n')[0].strip()
                
            if "(" in czech_name:
                # pass
                czech_name = czech_name.split('(')[0].strip()
            if german_name != None and czech_name != None and german_name != "" and czech_name != "":
                german_name_list.append(german_name)
                czech_name_list.append(czech_name)
            print(german_name,":",czech_name)

        
            # print(item.text)
            # print("check, count:", count)
            # count += 1

df = pd.DataFrame({'german': german_name_list, 'czech': czech_name_list})
            # df.columns = ['german', 'czech']
df.dropna(inplace=True)
df = df.reset_index(drop=True)
# print(df)

saving_adress = r"\Users\HP\OneDrive\Desktop\Python\Pet_Projects\web_scrapping_wiki"

df.to_csv(os.path.join(saving_adress, "german_czech.csv"), index=False)
