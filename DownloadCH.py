import os
import re

import requests
from bs4 import BeautifulSoup

savedir = os.getcwd() + "\\"  # Path to an existing empty directory
url = "http://www.explosm.net/comics/archive/"
r = requests.get(url).content
mainsoup = BeautifulSoup(r, "html.parser")
links = list(set(["http://www.explosm.net" + link["href"]
                  for link in mainsoup.find_all("a", {"href": re.compile(r"/comics/archive/\d{4}/\d{2}$")})]))

for url in links:
    r = requests.get(url).content
    soup = BeautifulSoup(r, "html.parser")
    comic_link_and_date = [(link["href"], link.text)
                           for link in soup.find_all("a", {"href": re.compile(r"http://explosm.net/comics/\d+/$")})]

    for l in comic_link_and_date:
        date = l[1]
        r = requests.get(l[0]).content
        tempsoup = BeautifulSoup(r, "html.parser")

        try:
            link = [(("http:" if "http" not in link["src"] else "") + link["src"])
                    for link in tempsoup.find_all("img", {"id": "main-comic"})][0]
        except IndexError:
            link = [file["src"] for file in tempsoup.find_all("embed")]

        response = requests.get(link)
        if response.status_code == 200:
            print("Downloading", link)
            # localdest = savedir + \
            # re.search(r"[^\/]+\.(png|gif|jpg|swf)", link, re.IGNORECASE).group()     #Filename = comic name
            localdest = savedir + date + \
                        re.search(r"\.(png|gif|jpg|swf)", link, re.IGNORECASE).group()  # Filename = Date published
            with open(localdest, "wb") as f:
                for chunk in response.iter_content(4096):
                    f.write(chunk)
