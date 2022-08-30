import os
import requests
import json
from bs4 import BeautifulSoup
import wget
from urllib.error import HTTPError


def get_data(subject="physics"):
    
    def get_image_links(sub_page):
        r = requests.get(sub_page)
        soup = BeautifulSoup(r.text, "html.parser")
        
        tags = soup.select("script#__NEXT_DATA__")[0].text
        data = json.loads(tags)
        return [i["imageUrl"] for i in data['props']['pageProps']['initialState']['seo']['categoryPage']["contentModules"]]

    home_page = "https://www.vedantu.com/iit-jee/jee-main-{subject}-important-questions".format(subject.lower())
    r = requests.get(home_page)
    soup = BeautifulSoup(r.text, "html.parser")
    a_tags = soup.select("a.PageListModulesmain_links__Cb2Md")
    
    data = {}
    for atag in a_tags:
        print("Getting links for {}".format(atag['title']))
        data[atag['title']] = get_image_links(atag['href'])
        print("Got links for {}".format(atag['title']))
    return data
    

def download(chapter, urls):
    TITLE = chapter
    PATH = "YOUR PATH HERE"
    DIRECTORY =  PATH + "\\{folder}".format(folder=TITLE)
    OUT_FILE = DIRECTORY + "\\image{index}.png"
    os.mkdir(DIRECTORY)

    print("downloading images for {TITLE}".format(chapter))
    i = 0
    while True:
        try:
            url = urls[i]
            wget.download(url, out=OUT_FILE.format(index=(i + 1)))
            i += 1
        except IndexError:
            print("\nAll Images have been Downloaded.")
            break
        

def main():
    print("Started scraping...")
    data = get_data("physics")
    print("Got All Links.")
    for chap in data:
        download(chap, data[chap])
        
        
if __name__ == "__main__":
    main()
   