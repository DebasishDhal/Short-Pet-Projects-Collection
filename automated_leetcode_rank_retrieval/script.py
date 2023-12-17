import requests
from bs4 import BeautifulSoup
import datetime
import os


url = "https://leetcode.com/dd99_dunder/"

def rank(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div', class_='flex flex-1 items-end space-x-[5px] text-base')
    div = divs[0]
    spans = div.find_all('span')
    rank = int(spans[1].text.replace(',',''))
    return rank

present_rank = rank(url)

#India date now
time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%d-%m-%Y") #There exists another way, it involves putting "Kolkata" somewhere


file_adress  = r"C:\Users\HP\OneDrive\Desktop\Python\Pet_Projects\leetcode_rank_retrieval"
file_name = "rank.txt"

with open(os.path.join(file_adress, file_name), 'r') as f:
    text_present = f.read()
    print(f.read())

if str(present_rank) not in text_present.split(): #I don't want to write the same rank twice
    with open(os.path.join(file_adress, file_name), 'w') as f:
        f.write(f"{text_present}{time} {rank(url)}\n")