from config import channel_id, channel_owner_id
from telegram import ParseMode

def send_to_channel(update, _):
    # print(update.message)
    message = update.message
    if not message:
        return

    admins = message.chat.get_administrators()
    if admins and (int(channel_owner_id) not in map(lambda x: x.user.id, admins)):
        message.reply_text('当前群聊还不是一个业余公司！')
        return

    if not message.from_user.id == 777000:
        message.forward(chat_id=f'@{channel_id}')
