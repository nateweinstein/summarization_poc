from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time

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

    try:
        element = soup.body.find("div", {"class": "wp-content"})
        authors = soup.find("meta", {"name":"author"})['content']
    except:
        return None
        
    if None not in (element, authors):
        # print("Element found!")
        return {'contents':''.join(map(str, element.contents)), 'authors':authors}
    else:
        # print("Element not found.")
        return None


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