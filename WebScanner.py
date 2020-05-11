# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from time import sleep
import unidecode
import datetime
import urllib.parse
import urllib.error
import urllib.request
import requests
import json
import os


def soupGet(url):
    html = requests.request("GET", url, headers={},
                            data={}).text.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    return soup


urlPack = ["https://vostfree.com/animes-vostfr/"]
for i in range(2, 21):
    urlPack.append(f"https://vostfree.com/animes-vostfr/page/{i}/")

Poster = {}
step = []

for i in urlPack:
    html = soupGet(i)
    step += html.find_all("div", class_="movie-poster")
    print(len(step), end=" ")

print("\n")
tour = 0
for i in step:
    tour += 1
    print(tour, end=" ")
    if tour % 20 == 0:
        print("")
    link = i.find_all("a", class_="link")[0]['href']
    image_url = "https://vostfree.com" + i.find_all("img")[0]['src']
    synopsis = i.find_all("div", class_="desc")[
        0].string.rstrip().lstrip()
    saison = i.find_all("div", class_="kp")[0].find_all("b")[0].string
    AnimeName = i.find_all("div", class_="title")[0].string.replace("VOSTFR",
                                                                    "Saison "+saison)
    synopsis = unidecode.unidecode(synopsis)
    Poster[AnimeName] = {"link": link,
                         "image_url": image_url,
                         "synopsis": synopsis}


with open("data1.json", "w", encoding="utf8") as fp:
    date = datetime.datetime.now()
    NewDico = {'date': (date.year, date.month, date.day,
                        date.hour, date.minute, date.second)}
    NewDico["Anime"] = Poster
    json.dump(NewDico, fp)
