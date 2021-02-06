from feralfish.decorators import club
from config import channel_id


@club
def send_to_channel(update, context):
    message = update.message or update.edited_message
    if (not message) or message.from_user.id == 777000:
        return
    message.forward(chat_id=f'@{channel_id}')


def delete_state(update, context):
    update.message.delete()
