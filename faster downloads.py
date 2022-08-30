import os
import requests
import json
import concurrent.futures
from bs4 import BeautifulSoup
import wget


def thread_get_data(subject="physics"):
    
    def get_image_links(sub_page):
        r = requests.get(sub_page)
        soup = BeautifulSoup(r.text, "html.parser")
        
        tags = soup.select("script#__NEXT_DATA__")[0].text
        data = json.loads(tags)
        return [i["imageUrl"] for i in data['props']['pageProps']['initialState']['seo']['categoryPage']["contentModules"]]
    
    home_page = "https://www.vedantu.com/iit-jee/jee-main-{subject}-important-questions".format(subject=subject.lower())
    r = requests.get(home_page)
    soup = BeautifulSoup(r.text, "html.parser")
    href_tags = soup.select("a.PageListModulesmain_links__Cb2Md")
    page_links = [i['href'] for i in href_tags]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_image_links, page_link) for page_link in page_links]
        
    data = {}
    for atag, future in zip(href_tags, futures):
        data[atag['title']] = future.result()
    return data
    

def download(chapter, urls):
    TITLE = chapter
    PATH = "YOUR PATH HERE"
    DIRECTORY =  PATH + "\\{folder}".format(folder=TITLE)
    OUT_FILE = DIRECTORY + "\\image{index}.png"
    os.mkdir(DIRECTORY)

    for index, url in enumerate(urls, start=1):
        wget.download(url, OUT_FILE.format(index=index))
        

def main():
    print("Started scraping...")
    data = thread_get_data("maths")
    print("Got All Links.")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download, data.keys(), data.values())
        
        
if __name__ == "__main__":
    main()
   