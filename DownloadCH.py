import os
import re

import requests
from bs4 import BeautifulSoup


class Cyanide:
    '''Create an instance of this class to download ALL comics with the date published as the file name.

    Attributes:
        save_dir: The path to an empty directory where the comics should be downloaded.
        use_date: Boolean value indicating whether to save comics with the date published as their file names.
    Methods:
        downloadcomic()
    '''
    url = "http://www.explosm.net/comics/archive/"

    def __init__(self, download_all=1, use_date=1, save_dir=""):
        '''Sets up attributes.

        Parameters:
             download_all: Boolean value specifying whether to download all the comics or not.
             use_date: Sets value for use_date attribute.
             save_dir: Sets value for save_dir attribute.'''
        self.save_dir = save_dir if save_dir else (os.getcwd() + "\\")
        self.use_date = use_date
        if download_all:
            r = requests.get(self.url).content
            main_soup = BeautifulSoup(r, "html.parser")
            links = list(set(["http://www.explosm.net" + link["href"]
                              for link in
                              main_soup.find_all("a", {"href": re.compile(r"/comics/archive/\d{4}/\d{2}$")})]))

            for link in links:
                r = requests.get(link).content
                soup = BeautifulSoup(r, "html.parser")
                comic_links = [link["href"]
                               for link in
                               soup.find_all("a", {"href": re.compile(r"http://explosm.net/comics/\d+/$")})]

                for comic in comic_links:
                    self.downloadcomic(comic)
        else:
            print("Initialization complete. You can now provide individual comic URL's to the downloadcomic() method")
        return

    def downloadcomic(self, url):
        '''Downloads the comic for the provided URL.

        Parameters:
            url: Link to a single comic's page'''
        r = requests.get(url).content
        comic_soup = BeautifulSoup(r, "html.parser")
        date = comic_soup.find_all("a", {}, True, re.compile(r"\d{4}\.\d{2}\.\d{2}"))[0].text

        try:
            link = [(("http:" if "http" not in link["src"] else "") + link["src"])
                    for link in comic_soup.find_all("img", {"id": "main-comic"})][0]
        except IndexError:
            link = [file["src"] for file in comic_soup.find_all("embed")][0]

        response = requests.get(link)

        if response.status_code == 200:
            print("Downloading", link)

            local_dest = (self.save_dir + re.search(r"[^\/]+\.(png|gif|jpg|swf)", link, re.IGNORECASE).group()) \
                if not self.use_date else (
                self.save_dir + date + re.search(r"\.(png|gif|jpg|swf)", link, re.IGNORECASE).group())

            with open(local_dest, "wb") as f:
                for chunk in response.iter_content(4096):
                    f.write(chunk)

        else:
            print("Unable to download; Response code:", response.status_code)
        return


if __name__ == "__main__":
    obj = Cyanide()
