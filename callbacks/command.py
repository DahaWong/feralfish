from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from manifest import manifest
from config import channel_id


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
            f"\n_by_ [{manifest.author}](https://t.me/{manifest.author_id})\n"
        ),
        reply_markup=markup
    )


def share(update, context, share_type='分享发现'):
    replied_message = update.message.reply_to_message
    if not replied_message:
        return
    context.bot.send_message(
        chat_id=f'@{channel_id}',
        text=f"#{share_type} {replied_message}"
    )


def yeyu(update, context):
    share(update, context, share_type='野鱼屏幕')


def help(update, context):
    update.message.reply_text(
        text=(
            f"*{manifest.name}使用说明书*\n"
            "/about: 关于本机器人\n"
        )
    )
