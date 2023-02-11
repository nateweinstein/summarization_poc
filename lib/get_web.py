from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
import re

from tinydb import TinyDB, Query
db = TinyDB('db/parsed_db.json')

sleep_len = 10

# Grab a url and write its contents to a local file; 
#url = url,  contents = file name, path = folder to write to
def crawlURL(url,contents,path):
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()

    with open(path+'/'+contents+'.html', 'wb') as f:
        f.write(webpage)
    time.sleep(sleep_len)
    return

# Parse a local HTML file and grab specific content from it
# EDIT ME BASED ON ARTICLES
def parseContent(file):
    soup = BeautifulSoup(file, "html.parser")
    search_string = 'transcript'
    try:
        transcript = soup.find(string=lambda text: text and search_string.lower() in text.lower())
        authors = soup.find("meta", {"name":"author"})['content']
        title = soup.find("meta", {"property":"og:title"})['content']
        description = soup.find("meta", {"property":"og:description"})['content']
    except:
        return None
        
    if None not in (transcript, authors):        
        # try to parse the 
        element = soup.body.find("div", {"class": "wp-content"})
        
        print("TRANSCRIPT found")
        print("AUTHORS", str(authors))
        i=0
        for aut in authors.split(', '):
            a = aut.split(' ')[0]+':'
            r = re.compile(a+'(.*?)<\/p\s*>')
            cleaned = r.findall(str(element))
            for c in cleaned:
                entry = {
                    'index':i,
                    'author':aut,
                    'title':title,
                    'description':description,
                    'content':strip_tags(c)
                }
                db.insert(entry)
                i = i + 1

    return
        # print("Element found!")
    #     return {'contents':''.join(map(str, element.contents)), 'authors':authors}
    # else:
    #     # print("Element not found.")
    #     return None



# Copied from here https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def search_word_in_string(word, string, size):
    index = string.find(word)
    if index == -1:
        return "Word not found in the string."
    start = max(0, index - size // 2)
    end = min(len(string), start + size)
    return string[start:end]