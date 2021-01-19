from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, ChatAction, ParseMode
from config import channel_id
from manifest import manifest

def send_to_channel(update, context):
    # print(update.message.from_user)
    if not update.message.from_user.id == 777000:
        context.bot.copy_message(
            chat_id = f'@{channel_id}',
            from_chat_id = update.message.chat_id,
            message_id = update.message.message_id
        )
