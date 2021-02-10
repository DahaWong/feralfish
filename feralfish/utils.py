import requests
# from time import time
from config import music_api
import pprint
import re
import os
import errno
from tqdm.contrib.telegram import tqdm
from config import bot_token


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
    def download(url, title, update, context):
        path = f'public/audio/{title}.mp3'
        res = requests.get(url, stream=True)
        if not res.ok:
            raise Exception(f'下载音频出错～ 状态码：{res.status_code}')
        block_size = 1024
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        total = int(res.headers.get('content-length', 0))
        chat_id = update.effective_chat.id
        progress_bar = tqdm(
            total=total,
            unit='iB',
            token=bot_token,
            chat_id=chat_id,
            bar_format='{percentage:3.0f}% |{bar:8}|'
        )
        with open(path, 'wb') as f:
            for data in res.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
            message_id = progress_bar.tgio.message_id
        context.bot.delete_message(chat_id, message_id)
        progress_bar.close()
        if total != 0 and progress_bar.n != total:
            raise Exception("下载进度条出错！")
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
