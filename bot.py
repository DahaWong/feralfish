import configparser
import sys
import traceback
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Defaults
from functools import wraps

# Config

config = configparser.ConfigParser()
config.read('config.ini')
bot_token = config['BOT']['TOKEN']
proxies = config['PROXIES']
defaults = Defaults(
    parse_mode="MARKDOWN",
    disable_notification=True
)
dev_user_id = int(config['DEV']['ID'])  # daha
channel_owner = int(config['CHANNEL']['OWNER'])  # bob
channel_id = config['CHANNEL']['ID']
update_info = {
    'token': bot_token,
    'use_context': True,
    'defaults': defaults
}


class manifest:
    name = "野鱼"
    channel_name = "野鱼日报"
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


def club(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        message = update.message
        admins = message.chat.get_administrators()
        if admins and (channel_owner not in map(lambda x: x.user.id, admins)):
            message.reply_text('当前群聊还不是一个业余公司！')
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def dev(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if update.message.from_user.id not in [dev_user_id, channel_owner]:
            update.message.reply_text(f'您没有{manifest.name}专线的获取权 :)')
            return
        return func(update, context, *args, **kwargs)
    return wrapped

# Commands:


def start(update, context):
    update.message.reply_text(
        f"你好，我是{manifest.name}！[{manifest.channel_name}](https://t.me/{channel_id})的管理员。")


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


@dev
def show_proxy(update, context):
    update.message.pin()
    buttons = [InlineKeyboardButton(
        text=f'{manifest.name}专线 {i}', url=proxy) for i, proxy in enumerate(proxies.values())]
    update.message.reply_text(
        text='点击按钮以乘坐专线通往互联网彼岸',
        reply_markup=InlineKeyboardMarkup.from_column(buttons)
    )


@club
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


@club
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

@club
def send_to_channel(update, context):
    message = update.message
    if not (message and message.from_user.id == 777000):
        return
    message.forward(chat_id=f'@{channel_id}')


# Handle Error
def handle_error(update, context):
    if not update:
        return
    if update.effective_message:
        text = f"刚刚的操作触发了一个错误，报告已抄送给[开发者](tg://user?id={dev_user_id})。"
        update.effective_message.reply_text(text)
    payload = ""
    if update.effective_user:
        payload += f"有[用户](tg://user?id={update.effective_user.id})"
    if update.effective_chat.title:
        payload += f"在{update.effective_chat.title}"
        if update.effective_chat.username:
            payload += f'(@{update.effective_chat.username})'
    if update.poll:
        payload += f'在发起投票 {update.poll.id} 时'
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    text = f"{payload}触发了一个错误：`{context.error}`。\n\n"
    text += f"错误路径如下:\n`{trace}`" if trace else ''
    context.bot.send_message(dev_user_id, text)


# Handlers
dispatcher.add_error_handler(handle_error, run_async=True)

command_handlers = [
    CommandHandler('start', start),
    CommandHandler('about', about),
    CommandHandler('help', help),
    CommandHandler('share', share),
    CommandHandler('yeyu', yeyu),
    CommandHandler('proxy', show_proxy)
]
message_handlers = [MessageHandler(
    Filters.regex(r'#(?:上电视|野鱼屏幕|分享发现)'), send_to_channel)]
handlers = command_handlers.extend(message_handlers)

for handler in command_handlers:
    dispatcher.add_handler(handler)

# Polling:
updater.start_polling()
updater.idle()
