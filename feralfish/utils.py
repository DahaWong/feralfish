from os import listdir, rename
import subprocess
from os.path import isfile, join
import requests
# from time import time
from config import music_api
import pprint
import re
import os
import errno


class Music(object):
    root = music_api
    cookie = ''

    def login(self, phone, pwd):
        res = requests.get(
            url=f"{self.root}/login/cellphone?phone={phone}&password={pwd}")
        pprint.pprint(res.json())
        self.cookie = f"cookie={res.json().get('cookie')}"

    def get_user(self):
        res = requests.get(url=f"{self.root}/user/detail{self.cookie}")
        # pprint.pprint(res.json())
        return res.json()

    def check_login(self):
        res = requests.get(url=f"{self.root}/login/status?{self.cookie}")
        pprint.pprint(res.json())

    def search(self, keyword):
        res = requests.get(url=f"{self.root}/cloudsearch?keywords={keyword}")
        pprint.pprint(res.json())
        return res.json()

    def get_url(self, music_id):
        res = requests.get(
            url=f"{self.root}/song/url?id={music_id}&{self.cookie}")
        return res.json()['data'][0]['url']

    def get_detail(self, music_id):
        res = requests.get(url=f"{self.root}/song/detail?ids={music_id}")
        result = res.json()['songs'][0]
        pprint.pprint(result)
        title = result['name']
        album_id = result['al']['id']
        performer = result['ar'][0]['name']
        pic_url = result['al']['picUrl'] + \
            '?param=100y100'  # with size of 100*100
        pic = requests.get(pic_url).content
        pic_file = f"public/logo/{album_id}.jpg"
        with open(pic_file, 'wb') as f:
            f.write(pic)
        return title, performer, pic_file

    @staticmethod
    def download(url, title):
        path = f'public/audio/{title}.mp3'
        res = requests.get(url)
        if not res.ok:
            raise Exception(f'下载音频出错～ 状态码：{res.status_code}')
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(path, 'wb') as f:
            f.write(res.content)
        return path

    def check_available(self, music_id):
        res = requests.get(url=f"{self.root}/check/music?id={music_id}")
        pprint.pprint(res.json())
        return res.json()

    @staticmethod
    def extract_id(url):
        match = re.match('.*song\?id=([0-9]+).*',
                         url) or re.match('.*song/([0-9]+).*', url)
        if match:
            return match[1]


class Ebook(object):
    # return name of file to be kept after conversion.
    # we are just changing the extension. azw3 here.
    def get_final_filename(f):
        f = f.split(".")
        filename = ".".join(f[0:-1])
        processed_file_name = filename+".azw3"
        return processed_file_name

    # return file extension. pdf or epub or mobi

    def get_file_extension(f):
        return f.split(".")[-1]

    # list of extensions that needs to be ignored.
    ignored_extensions = ["pdf"]

    # here all the downloaded files are kept
    mypath = "/home/daha/downloads/ebooks/"

    # path where converted files are stored
    mypath_converted = "/home/daha/downloads/ebooks/kindle/"

    # path where processed files will be moved to, clearing the downloaded folder
    mypath_processed = "/home/daha/downloads/ebooks/processed/"

    raw_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    converted_files = [f for f in listdir(
        mypath_converted) if isfile(join(mypath_converted, f))]

    for f in raw_files:
        final_file_name = get_final_filename(f)
        extension = get_file_extension(f)
        if final_file_name not in converted_files and extension not in ignored_extensions:
            print("Converting : "+f)
            try:
                subprocess.call(["ebook-convert", mypath+f,
                                 mypath_converted+final_file_name])
                s = rename(mypath+f, mypath_processed+f)
                print(s)
            except Exception as e:
                print(e)
        else:
            print("Already exists : "+final_file_name)
