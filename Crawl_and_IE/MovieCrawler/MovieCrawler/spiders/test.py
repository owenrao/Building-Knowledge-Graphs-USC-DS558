'''from json import loads

directors = []
with open('C:/Users/ruiji/Documents/USC/Fall2022/DS558/Homework/01_Crawl_and_IE/Script/Ruijie_Rao_hw01_movie.jsonl','r', encoding='utf-8') as file:
    for line in file:
        dict = loads(line)
        directors += dict["directors"]
directors = set(directors)
#print(len(directors))

directors_= []
with open('C:/Users/ruiji/Documents/USC/Fall2022/DS558/Homework/01_Crawl_and_IE/Script/Ruijie_Rao_hw01_director.jsonl','r', encoding='utf-8') as file:
    for line in file:
        dict = loads(line)
        directors_.append(dict["name"])
directors_ = set(directors_)
#print(len(directors_))

print([i for i in directors if i not in directors_])
'''

import requests
r = requests.get("https://www.imdb.com/name/nm0001008/bio?ref_=nm_ov_bio_sm")

from bs4 import BeautifulSoup

with open('C:/Users/ruiji/Documents/USC/Fall2022/DS558/Homework/01_Crawl_and_IE/Script/MovieCrawler/MovieCrawler/spiders/test.html','r', encoding='utf-8') as file:
    content = file.read()
base_url = "https://www.imdb.com"
soup = BeautifulSoup(content, 'lxml')
temp = [h4 for h4 in soup.find_all("h4") if "Mini Bio" in h4.get_text()]
if len(temp)>0:
    mini_bio = temp[0]
    biography = mini_bio.find_next_sibling().get_text(strip=True)
print(biography)
