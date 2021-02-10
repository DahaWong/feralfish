import requests
from time import time
from config import music_api
import pprint
import re


class Music(object):
    root = music_api

    def login(self, phone, pwd):
        res = requests.get(
            url=f"{self.root}/login/cellphone?phone={phone}&password={pwd}")
        pprint.pprint(res.json())
        return res.json()

    def get_user(self):
        res = requests.get(url=f"{self.root}/user/detail")
        # pprint.pprint(res.json())
        return res.json()

    def check_login(self):
        res = requests.get(url=f"{self.root}/login/status")
        pprint.pprint(res.json())

    def search(self, keyword):
        res = requests.get(url=f"{self.root}/cloudsearch?keywords={keyword}")
        pprint.pprint(res.json())
        return res.json()

    def get_url(self, music_id):
        res = requests.get(url=f"{self.root}/song/url?id={music_id}")
        return res.json()['data'][0]['url']

    def get_detail(self, music_id):
        res = requests.get(url=f"{self.root}/song/detail?ids={music_id}")
        result = res.json()['songs'][0]
        pprint.pprint(result)
        title = result['name']
        performer = result['ar'][0]['name']
        pic = result['al']['picUrl']+'?param=100y100'  # with size of 60*60
        print(pic)
        return title, performer, pic

    @staticmethod
    def download(url, title):
        path = f'public/audio/{title}.mp3'
        res = requests.get(url)
        with open(path, 'wb') as f:
            f.write(res.content)
        return path

    def check_available(self, music_id):
        res = requests.get(url=f"{self.root}/check/music?id={music_id}")
        pprint.pprint(res.json())
        return res.json()

    @staticmethod
    def extract_id(url):
        song_id = re.match('.*song\?id=([0-9]+).*', url)[1]
        return song_id
