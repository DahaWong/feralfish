from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from manifest import manifest
from config import dev_user_id, channel_id

def start(update, context):
    update.message.reply_text(f"你好，我是野鱼！[野鱼日志](https://t.me/{channel_id})的管理员。")

def about(update, context):
    keyboard = [[InlineKeyboardButton("源     代     码", url = manifest.repo),
                InlineKeyboardButton("工     作     室", url = manifest.author_url)]]
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text=(
            f"*{manifest.name}*  "
            f"`{manifest.version}`"
            f"\n_by_ [{manifest.author}](https://t.me/{manifest.author_id})\n"
        ), 
        reply_markup = markup
    )


# def search(update, context):
#     keyboard = [[InlineKeyboardButton('搜   索   播   客', switch_inline_query_current_chat = 'search ')]]

#     message = update.message.reply_text(
#         '🔎️',
#         reply_markup = InlineKeyboardMarkup(keyboard)
#     )

#     Tips(from_command = 'search',
#         text = (f"⦿ 点击「搜索播客」按钮启动搜索模式。"
#             f"\n⦿ 前往 Telegram `设置 → 外观 → 大表情 Emoji` 获得更好的显示效果"
#             f"\n⦿ 推荐通过在对话框中输入 `@` 来唤出行内搜索模式"
#         )
#     ).send(update, context)

# def manage(update, context):
#     user = context.user_data['user']
#     podcast_names = user.subscription.keys()
#     page = ManagePage(podcast_names)
#     reply_message = update.message.reply_text(
#         text = page.text,
#         reply_markup = ReplyKeyboardMarkup(page.keyboard(), resize_keyboard = True, one_time_keyboard=True)
#     )
#     update.message.delete()

def help(update, context):
    command_message_id = update.message.message_id

    keyboard = [[
        InlineKeyboardButton("阅  读  完  毕", 
        callback_data = f'delete_command_context_{command_message_id}')
    ]]

    update.message.reply_text(
        f"*{manifest.name} 使用说明*",# import constants
        reply_markup = InlineKeyboardMarkup(keyboard)
    )