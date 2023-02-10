from lib.crawler import getLinks
from lib.get_web import crawlURL, parseContent, strip_tags
import os
from transformers import pipeline

from tinydb import TinyDB, Query
import json

# Set up a temp DB for easier writing
db = TinyDB('db/sysk.json')

search_terms = ['podcast']
site = 'a16z.com'

# Write crawled HTML to here
directory = 'sysk' 

# Generate a temp DB consisting of objects containing:
    # url, podcast name, DDG description, whether it's been crawled, contents of the article
def generateArticles():
    
    # # This will crawl DDG for relevant urls w/ content and dump them into a temp DB
    # getLinks(search_terms, site, db)

    # # Write all of the articles to a local folder as html
    # docs = db.all()
    # for d in docs:
    #     crawlURL(d['url'], d['podcast'], directory)
    
    # Parse the local html files --> you need to tweak this fucnt
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file):
            with open(file,'r',encoding = "ISO-8859-1") as f:
                #print(f.read())
                #con = parseContent(f.read())
                con = json.loads(f.read())


                if con is not None:
                    db.insert({"body":con['text'],"author":'sysk', "guid":con['id'], "url": con['audio_url']})#, Query().podcast=='sysk')
                    print(filename+ " updated!")    # 


# Uncomment to generate locally
#generateArticles()


# Create Summarizer object

def testSummarizer():
    print("compiling summarizer...")
    summarizer = pipeline("summarization", model="my_awesome_billsum_model")
    print("done")

    articles = db.all()
    size = len(articles)

    i=1
    while i>0 and i<size+1:
        print("\nPick an article between 1 and "+str(size))
        i = int(input())
        a = articles[int(i)-1]
        print('\nYou selected: '+a['guid'])
        #print("DDG summary: "+a['contents'])
        print("URL: "+a['url'])
        print('\nAttempting to summarize\n\n')
        #print("Authors"+ str(a['body']['authors']))
        #contents = strip_tags(a['body']['contents'])
        contents = a['body']
        #contents = contents[:3500]
        summary = summarizer(contents)
        print(summary)
        print('\n\nGo again?')

testSummarizer()
