from feralfish.decorators import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import manifest, channel_id, proxies


def start(update, context):
    update.message.reply_text(
        f"你好，我是{manifest.name}！[{manifest.group_name}](https://t.me/{channel_id})的管家。")


def about(update, context):
    keyboard = [[InlineKeyboardButton("源代码", url=manifest.repo),
                 InlineKeyboardButton("工作室", url=manifest.author_url)]]
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
        text=f'{manifest.name}专线 {i+1}', url=proxy) for i, proxy in enumerate(proxies.values())]
    update.message.reply_text(
        text='点击按钮以乘坐专线通往互联网彼岸',
        reply_markup=InlineKeyboardMarkup.from_column(buttons)
    )


@club
def share(update, context, share_type='分享发现'):
    message = update.message
    replied_message = message.reply_to_message
    if not replied_message:
        message.reply_text(
            (
                '嗨，想要使用指令，需要先*回复*一条想要分享的群组消息，并在回复的对话框中填入命令；被回复的消息会同步到野鱼日报。\n\n'
                '有疑问可以找 @bob_fu 或 @dahawong :)'
            )
        )
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
