from duckduckgo_search import ddg
from duckduckgo_search import ddg_videos
import csv
from tinydb import TinyDB, Query

def getVideos(keywords, csv_name):
    # Get the songs
    # Write the data row
    length =0
    # Open the file in append mode
    with open(csv_name+'.csv', 'a', newline='') as file:
        # Create a writer object
        writer = csv.writer(file)

        for keyword in keywords:
            songs = ddg_videos(keywords=keyword+" site:youtube.com", safesearch='Off', time=None, resolution=None, duration=None, license_videos=None, max_results=1000, output=None)
            length = len(songs)
            for s in songs:
                writer.writerow([s['title'], s['content']])
    print("finished writing this many songs: " + str(length))
    

# Search DDG for URLS based on keywords and the site restriction
def getLinks(keywords, site, db):
    length =0

    for keyword in keywords:            
        links = ddg(keywords=keyword+" site:"+site, time=None, max_results=1000)
        length = len(links)
        
        for s in links:
            db.insert({'podcast':s['title'], 'url':s['href'], 'contents':s['body'], 'crawled':False, 'body':''})
            # writer.writerow([s['title'], s['href'], s['body']])
        print("finished writing this many songs: " + str(length))
    return
    
