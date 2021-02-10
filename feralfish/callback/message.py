from feralfish.decorators import club, channel
from feralfish.utils import Music
from config import channel_id, dev_user_id, music_phone, music_pwd
from telegram import InputMediaAudio

music = Music()
music.login(music_phone, music_pwd)
music.check_login()

@club
def send_to_channel(update, context):
    message = update.effective_message
    if message.from_user.id == 777000:
        return
    audio_messages = download_music(update, context)
    if audio_messages:
        for message in audio_messages:
            message.forward(chat_id=f'@{channel_id}')
        return
    message.forward(chat_id=f'@{channel_id}')


def delete_state(update, context):
    update.message.delete()


@channel
def parse_music(update, context):
    download_music(update, context)

def download_music(update, context):
    message = update.effective_message
    entities = message.parse_entities()
    audios = []
    flag = 0
    for entity, text in entities.items():
        if entity.type == 'url':  # 163
            flag += 1
            music_id = Music.extract_id(text)
            if not music_id:
                continue
            music_url = music.get_url(music_id)
            title, performer, pic = music.get_detail(music_id)
            path = music.download(music_url, title)
            audio = InputMediaAudio(
                media=open(path, 'rb'),
                title=title,
                parse_mode = None,
                performer=performer,
                thumb=open(pic, 'rb')
            )
            audios.append(audio)
    if audios:
        audio_messages = message.reply_media_group(media=audios, allow_sending_without_reply=True)
        return audio_messages

def get_chat_id(update, context):
    context.bot.send_message(dev_user_id, update.effective_chat.id)
