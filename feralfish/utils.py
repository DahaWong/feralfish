import requests
from time import time
from config import music_phone, music_pwd, music_api
import pprint
import re


class Music(object):
    root = music_api
    def login(self, phone, pwd):
        timestamp = int(time())
        res = requests.get(url=f"{self.root}/login/cellphone?phone={phone}&password={pwd}&timestamp={timestamp}")
        pprint.pprint(res.json())
        return res.json()
    def get_user(self):
        res = requests.get(url=f"{self.root}/user/detail")
        pprint.pprint(res.json())
        return res.json()
    def check_login(self):
        res = requests.get(url=f"{self.root}/login/status")
        pprint.pprint(res.json())
        return res.json()
    def search(self, keyword):
        res = requests.get(url=f"{self.root}/cloudsearch?keywords={keyword}")
        pprint.pprint(res.json())
        return res.json()
    def get_url(self, music_id):
        res = requests.get(url=f"{self.root}/song/url?id={music_id}")
        return res.json()['data']['url']
    def check_available(self, music_id):
        res = requests.get(url=f"{self.root}/check/music?id={music_id}")
        pprint.pprint(res.json())
        return res.json()

    @staticmethod
    def extract_id(url):
        song_id = re.match('song\?id=([0-9]+)', url)[1]
        print(song_id)
        return song_id