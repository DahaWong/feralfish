from feralfish.decorators import club, channel
from feralfish.utils import Music
from config import channel_id, dev_user_id, music_phone, music_pwd

music = Music()
music.login(music_phone, music_pwd)


@club
def send_to_channel(update, context):
    message = update.effective_message
    if message.from_user.id != 777000:
        message.forward(chat_id=f'@{channel_id}')


def delete_state(update, context):
    update.message.delete()


@channel
def download_music(update, context):
    message = update.effective_message
    entities = message.parse_entities()
    for entity, text in entities.items():
        if entity.type == 'url':  # 163
            music_url = music.get_url(music_id=Music.extract_id(text))
            message.reply_audio(
                audio=music_url,
                caption=message.text,
                allow_sending_without_reply=True
            )
    message.delete()


def get_chat_id(update, context):
    context.bot.send_message(dev_user_id, update.effective_chat.id)
