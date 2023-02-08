from __future__ import unicode_literals
import yt_dlp as youtube_dl
import time


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    print(d['filename']+": "+d['_default_template'])
    if d['status'] == 'finished':
        print('Done downloading.... Now converting ...')


# URLS = a list of lists from a csv; the first value will be the title, the second will be the url
class getAudio:
    def __init__(self, urls,idx_to_start=0, batch_size=500):
        self.urls = urls
        self.idx = idx_to_start
        self.batch_size = batch_size


    #
    def download(self, url):
        song = url[0]+'-'+url[1][-11:]
        yt_url=url[1]

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'songs/'+song+'.',
            'keepvideo':False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
    
    def downloadAllURLs(self):
        i=0
        for url in self.urls:
            if i>=self.idx:
                self.download(url)
            i= i+1
            print(i)
            time.sleep(1)
        print("Finished!")

# ga = getAudio('https://www.youtube.com/watch?v=BaW_jenozKc')
# ga.download()