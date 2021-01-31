import configparser
import sys
import traceback
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Defaults

# Config

config = configparser.ConfigParser()
config.read('config.ini')
bot_token = config['BOT']['TOKEN']
proxy = config['BOT']['PROXY']
defaults = Defaults(
    parse_mode="MARKDOWN",
    disable_notification=True
)
dev_user_id = config['DEV']['ID']
channel_id = config['CHANNEL']['ID']
channel_owner_id = config['CHANNEL']['OWNER_ID']
update_info = {
    'token': bot_token,
    'use_context': True,
    'defaults': defaults
}


class manifest:
    name = "野鱼"
    bot_id = "FeralFishBot"
    author = "Daha"
    author_id = 'dahawong'
    author_url = "https://office.daha.me/"
    version = "0.0.2"
    discription = ""
    repo = "https://github.com/dahawong/feralfish"


updater = Updater(**update_info)
dispatcher = updater.dispatcher


# Use this method to logout your bot from telegram api cloud:
# updater.bot.log_out()

# Polling:
updater.start_polling()
updater.idle()

# Commands:


def start(update, context):
    update.message.reply_text(
        f"你好，我是野鱼！[野鱼日报](https://t.me/{channel_id})的管理员。")


def about(update, context):
    keyboard = [[InlineKeyboardButton("源     代     码", url=manifest.repo),
                 InlineKeyboardButton("工     作     室", url=manifest.author_url)]]
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text=(
            f"*{manifest.name}*  "
            f"`{manifest.version}`"
            f"\nby [{manifest.author}](https://t.me/{manifest.author_id})\n"
        ),
        reply_markup=markup
    )


def share(update, context, share_type='分享发现'):
    message = update.message
    replied_message = message.reply_to_message
    if not replied_message:
        message.reply_text('推荐的内容不能为空 :)')
        return
    new_message = replied_message.copy(chat_id=f'@{channel_id}')
    bot = context.bot
    back_slash = '\\'
    if replied_message.text:
        bot.edit_message_text(
            chat_id=f'@{channel_id}',
            message_id=new_message.message_id,
            text=f"#{share_type} {replied_message.text_markdown_v2_urled.replace(back_slash,'')}"
        )
    elif replied_message.caption:
        bot.edit_message_caption(
            chat_id=f'@{channel_id}',
            message_id=new_message.message_id,
            caption=f"{replied_message.caption_markdown_v2_urled.replace(back_slash,'')}\n\n#{share_type}"
        )


def yeyu(update, context):
    share(update, context, share_type='野鱼屏幕')


def help(update, context):
    update.message.reply_text(
        text=(
            f"*{manifest.name}使用说明书*\n\n"
            "/about: 关于本机器人\n"
        )
    )


# Handle Message


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


# Handle Error


def handle_error(update, context):
    if not update:
        return
    if update.effective_message:
        text = f"刚刚的操作触发了一个错误，报告已抄送给[开发者](https://t.me/{manifest.author_id})。"
        update.effective_message.reply_text(text)
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    payload = ""
    if update.effective_user:
        payload += f"<a href='tg://user?id={update.effective_user.id}'>有人</a>在使用中"
    if update.effective_chat.title:
        payload += f'<i>{update.effective_chat.title}</i>'
        if update.effective_chat.username:
            payload += f'(@{update.effective_chat.username})'
    if update.poll:
        payload += f'投票 {update.poll.id}'
    text = f"{payload}触发了一个错误：<code>{context.error}</code>。\n\n错误路径如下:\n\n<code>{trace}" \
           f"</code>"
    context.bot.send_message(dev_user_id, text, parse_mode=ParseMode.HTML)


# Handlers
dispatcher.add_error_handler(handle_error, run_async=True)

command_handlers = [
    CommandHandler('start', start),
    CommandHandler('about', about),
    CommandHandler('help', help),
    CommandHandler('share', share),
    CommandHandler('yeyu', yeyu),
]
message_handlers = [MessageHandler(
    Filters.regex(r'#(?:上电视|野鱼屏幕|分享发现)'), send_to_channel)]
handlers = command_handlers.extend(message_handlers)

for handler in command_handlers:
    dispatcher.add_handler(handler)
