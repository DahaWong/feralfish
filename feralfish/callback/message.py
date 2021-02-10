from feralfish.decorators import club, channel
from feralfish.utils import Music
from config import channel_id, dev_user_id, music_phone, music_pwd
from telegram import InputMediaAudio
from mutagen.mp3 import MP3

music = Music()
music.login(music_phone, music_pwd)
music.check_login()


@club
def send_to_channel(update, context):
    message = update.effective_message
    if message.from_user.id == 777000:
        return
    forwarded = message.forward(chat_id=f'@{channel_id}')
    audios = download_music(update, context)
    if audios:
        forwarded.reply_media_group(
            media=audios, allow_sending_without_reply=True)


def delete_state(update, context):
    update.message.delete()


@channel
def parse_music(update, context):
    download_music(update, context)


def download_music(update, context):
    message = update.effective_message
    entities = message.parse_entities()
    downloading_note = None
    uploading_note = None
    audios = []
    in_channel = update.effective_chat.type == 'channel'
    flag = 0
    for entity, text in entities.items():
        if entity.type == 'url':  # 163
            if not (flag or in_channel):
                downloading_note = message.reply_text("欢迎使用野鱼之声！")
            flag += 1
            if not in_channel:
                downloading_note = downloading_note.edit_text(
                    f'正在下载第 {flag} 首音乐…')
            music_id = Music.extract_id(text)
            if not music_id:
                continue
            music_url = music.get_url(music_id)
            title, performer, pic = music.get_detail(music_id)
            path = music.download(music_url, title)
            audio = InputMediaAudio(
                media=open(path, 'rb'),
                title=title,
                parse_mode=None,
                performer=performer,
                thumb=open(pic, 'rb'),
                duration=int(MP3(path).info.length)
            )
            audios.append(audio)
    if audios:
        if not in_channel:
            uploading_note = downloading_note.edit_text("上传中，请稍候…")
        message.reply_media_group(
            media=audios, allow_sending_without_reply=True)
        if not in_channel:
            uploading_note.delete()
        return audios


def get_chat_id(update, context):
    context.bot.send_message(dev_user_id, update.effective_chat.id)
