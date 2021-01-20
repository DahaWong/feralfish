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
    message = update.message
    replied_message = message.reply_to_message
    if not replied_message:
        message.reply_text('推荐的内容不能为空 :)')
        return
    new_message = replied_message.copy(chat_id = f'@{channel_id}')
    bot = context.bot
    if replied_message.text:
        bot.edit_message_text(
            chat_id = f'@{channel_id}', 
            message_id = new_message.message_id,
            text = f'#{share_type} {replied_message.text_markdown_v2_urled}'
        )
    elif replied_message.caption:
        bot.edit_message_caption(
            chat_id = f'@{channel_id}', 
            message_id = new_message.message_id,
            caption = f'{replied_message.caption_markdown_v2_urled}\n\n#{share_type}'
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
