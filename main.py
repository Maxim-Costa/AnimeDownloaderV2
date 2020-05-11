from bs4 import BeautifulSoup
import requests
import json
import os
import subprocess


def SibnetLink(url):
    html = requests.request("GET", url, headers={},
                            data={}).text.encode('utf8')

    soup = BeautifulSoup(html, "html.parser")
    step = soup.find_all("script")
    l = str(step[23])
    r = l.split("\"")
    return r[r.index("video/mp4")-2]


templateLink = {"Sibnet": "https://video.sibnet.ru/shell.php?videoid={id}",
                "Mytv": "https://www.myvi.tv/embed/{id}"}

url = "https://vostfree.com/384-tensei-shitara-slime-datta-ken-vostfr-ddl-streaming-1fichier-uptobox.html"
html = requests.request("GET", url, headers={},
                        data={}).text.encode('utf8')
soup = BeautifulSoup(html, "html.parser")

step = soup.find_all("div", class_="button_box")
step1 = soup.find_all("div", class_="player_box")

DicoId = dict()
DicoAll = dict()
Link = dict()

for i in step1:
    DicoId[i.get("id")] = i.string

nbEpisode = len(step)
g = 0
for i in step:
    g += 1
    for j in i.contents:
        #print(j.string, " : ", DicoId["content_"+j.get('id')])
        if not (j.string in DicoAll.keys()):
            DicoAll[j.string] = {}
        DicoAll[j.string][g] = DicoId["content_"+j.get('id')]

for k, v in DicoAll.items():
    print(f"{k} : {len(v.keys())}/{nbEpisode}")
    if len(v.keys()) == nbEpisode:
        for k1, v1 in DicoAll[k].items():
            Link[k1] = templateLink[k].replace("{id}", v1)
print("\n")
for k, v in Link.items():
    print(f"{k} : {v}")
    getVersion = subprocess.Popen(
        './cusi.sh '+v, shell=True, stdout=subprocess.PIPE).stdout
    version = getVersion.read()
    version = version.decode()
    print(version.rstrip())
