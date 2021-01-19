from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, ChatAction, ParseMode
from config import channel_id
from manifest import manifest

def exit_reply_keyboard(update, context):
    if not check_login(update, context): return
    message = update.message
    message.reply_text(
        '好', 
        reply_markup = ReplyKeyboardRemove()
    ).delete()
    message.delete()