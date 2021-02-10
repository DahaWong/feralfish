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
    if message.from_user.id != 777000:
        message.forward(chat_id=f'@{channel_id}')


def delete_state(update, context):
    update.message.delete()


@channel
def download_music(update, context):
    print('in')
    message = update.effective_message
    entities = message.parse_entities()
    for entity, text in entities.items():
        if entity.type == 'url':  # 163
            music_id = Music.extract_id(text)
            if not music_id:
                continue
            music_url = music.get_url(music_id)
            title, performer, pic = music.get_detail(music_id)
            path = music.download(music_url, title)
            caption = None if update.effective_chat.type == 'private' else message.text
            message.reply_audio(
                audio=open(path, 'rb'),
                title=title,
                performer=performer,
                thumb=pic,
                caption=caption,
                allow_sending_without_reply=True,
            )
    message.delete()


def get_chat_id(update, context):
    context.bot.send_message(dev_user_id, update.effective_chat.id)
