from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from utils.persistence import persistence
from base64 import urlsafe_b64decode as decode
from manifest import manifest
from models import User, Feed
from components import ManagePage, PodcastPage
import re, os
from config import dev_user_id

def start(update, context):
    message = update.message
    user_id = message['from_user']['id']
    first_name = message['from_user']['first_name']

    if 'user' not in context.user_data.keys():
        user = User(first_name, user_id)
        context.user_data.update({
            'user': user,
            'tips':['search', 'help', 'logout','alert'],
        })

    user = context.user_data['user']
    if (not context.args) or (context.args[0] == "login"):
        welcome_text = (
            f'欢迎使用 {manifest.name}！                                            '
            f'\n\n您可以发送 OPML 文件或 RSS 链接以*导入播客订阅*。\n'
        )

        keyboard = [[
            InlineKeyboardButton('搜   索   播   客', switch_inline_query_current_chat = "search "),
            InlineKeyboardButton('订   阅   列   表', switch_inline_query_current_chat = "")
        ]]

        welcome_message = message.reply_text(
            welcome_text,
            reply_markup = InlineKeyboardMarkup(keyboard)
        )
        
        welcome_message.pin(disable_notification=True)
    else: 
        podcast_name = decode(context.args[0]).decode('utf-8')
        podcast = context.bot_data['podcasts'][podcast_name]
        subscribing_note = update.message.reply_text("订阅中…")
        # 完全一样的订阅逻辑，简化之：
        user.subscription.update({podcast_name: Feed(podcast)})
        podcast.subscribers.add(user_id)
        page = PodcastPage(podcast)
        subscribing_note.edit_text(
            text = page.text(),
            reply_markup = InlineKeyboardMarkup(page.keyboard())
        )

def about(update, context):
    if not check_login(update, context): return
    keyboard = [[InlineKeyboardButton("源     代     码", url = manifest.repo),
                InlineKeyboardButton("工     作     室", url = manifest.author_url)]]
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text=(
            f"*{manifest.name}*  "
            f"`{manifest.version}`"
            f"\n_by_ [{manifest.author}](https://t.me/{manifest.author_id})\n"
        ), 
        reply_markup=markup
    )
    jobs = context.job_queue.jobs()
    s = '\n'.join([job.name for job in jobs])
    if s: context.bot.send_message(dev_user_id, s)

def search(update, context):
    if not check_login(update, context): return
    keyboard = [[InlineKeyboardButton('搜   索   播   客', switch_inline_query_current_chat = 'search ')]]

    message = update.message.reply_text(
        '🔎️',
        reply_markup = InlineKeyboardMarkup(keyboard)
    )

    Tips(from_command = 'search',
        text = (f"⦿ 点击「搜索播客」按钮启动搜索模式。"
            f"\n⦿ 前往 Telegram `设置 → 外观 → 大表情 Emoji` 获得更好的显示效果"
            f"\n⦿ 推荐通过在对话框中输入 `@` 来唤出行内搜索模式"
        )
    ).send(update, context)

def manage(update, context):
    if not check_login(update, context): return
    user = context.user_data['user']
    podcast_names = user.subscription.keys()
    page = ManagePage(podcast_names)
    reply_message = update.message.reply_text(
        text = page.text,
        reply_markup = ReplyKeyboardMarkup(page.keyboard(), resize_keyboard = True, one_time_keyboard=True)
    )
    update.message.delete()

def help(update, context):
    if not check_login(update, context): return
    command_message_id = update.message.message_id

    keyboard = [[
        InlineKeyboardButton("阅  读  完  毕", 
        callback_data = f'delete_command_context_{command_message_id}')
    ]]

    update.message.reply_text(
        f"*{manifest.name} 使用说明*",# import constants
        reply_markup = InlineKeyboardMarkup(keyboard)
    )

def export(update, context):
    if not check_login(update, context): return
    user = context.user_data['user']
    if not user.subscription:
        update.message.reply_text('您的订阅列表还是空的，请先订阅再导出～')
        return
    update.message.reply_document(
        filename = f"{user.name} 的 {manifest.name} 订阅.xml",
        document = user.update_opml(), 
        # thumb = ""
    )

def logout(update, context):
    if not check_login(update, context): return
    command_message_id = update.message.message_id
    keyboard = [[InlineKeyboardButton("返   回", callback_data = f"delete_command_context{command_message_id}"),
                 InlineKeyboardButton("注   销", callback_data = "logout")]]

    update.message.reply_text(
        "确认注销账号吗？\n",
        reply_markup = InlineKeyboardMarkup(keyboard)
    )

    Tips('logout', "⦿ 这将清除所有存储在后台的个人数据。").send(update, context)

class Tips(object):
    def __init__(self, from_command, text):
        self.command = from_command
        self.text = text
    def keyboard(self):
        return InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("✓", callback_data=f'close_tips_{self.command}')
        )
    def send(self, update, context):
        if self.command not in context.user_data.get('tips'): 
            return
        update.message.reply_text(
            text = self.text,
            reply_markup = self.keyboard()
        )

def check_login(update, context):
    user = context.user_data.get('user')
    if not user:
        update.message.reply_text("请先登录：/start")
        return False
    return True