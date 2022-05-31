import pprint
from telegram import BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats, BotCommandScopeChat, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler, CallbackContext
from config import manifest, channel_id, dev_user_id, private_commands, group_commands, dev_commands
from feralfish.utils import notion

async def get_bot_data(update: Update, context: CallbackContext):
    bot_data = pprint.pformat(context.bot_data)
    await update.message.reply_markdown(f"`{bot_data}`")

async def init(update: Update, context: CallbackContext):
    await context.bot.set_my_commands(commands=private_commands,
                                      scope=BotCommandScopeAllPrivateChats())
    await context.bot.set_my_commands(commands=group_commands,
                                      scope=BotCommandScopeAllGroupChats())
    await context.bot.set_my_commands(commands=dev_commands,
                                    scope=BotCommandScopeChat(dev_user_id))
    await context.bot.send_message(dev_user_id, '指令初始化完成')
    # context.bot_data['questions_count'] = 6
    # context.bot_data['questions_feedback_count'] = 32
    context.bot_data['recent_questions'] = [
        { 'content': "什么时候开店，开家什么样的店？", 'message_id': 54 },
        { 'content': "到底是康德的时代还是伍德斯托克的时代更适合我？", 'message_id': 55 },
        { 'content': "如何做好一个有价值的 online co-working/event space + 一个 productivity AI 来帮助跨领域阅读，以及（类似 Vsauce、Last Week Tonight with John Oliver）explainatory 性质的视频/vlog 的 post-production 编辑", 'message_id': 56 },
    ]
    context.bot_data['recent_feedbacks'] = 7

async def question(update: Update, context: CallbackContext):
    await update.message.reply_text(
        text='请输入你的问题：',
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                '取消', callback_data='cancel_adding_question')
        )
    )
    return 0


async def start(update: Update, context: CallbackContext):
    command_arg = context.args[0] if context.args else None
    if command_arg == 'add_a_question':
        return await question(update, context)
    else:
        await update.message.reply_markdown(
            f"你好，我是{manifest.name}！[{manifest.group_name}](https://t.me/{channel_id})的管家。")
        return ConversationHandler.END


async def about(update: Update, context: CallbackContext):
    keyboard = [InlineKeyboardButton("源代码", url=manifest.repo),
                InlineKeyboardButton("工作室", url=manifest.author_url)]
    await update.effective_message.reply_markdown(
        text=(
            f"*{manifest.name}*  "
            f"`{manifest.version}`\n\n"
            f"负责处理[灵感买家俱乐部](https://club.q24.io)旗下项目（如 [Uselessideas](https://t.me/uselessideas)、[Project 25](https://t.me/qna25)，还有[野鱼日报](https://t.me/ideabuyersclub)）的大小事。\n\n"
            f"\n[{manifest.author}](https://t.me/{manifest.author_id}) 制作"
        ),
        reply_markup=InlineKeyboardMarkup.from_row(keyboard)
    )


async def share(update: Update, context: CallbackContext):
    replied_message = update.effective_message.reply_to_message
    new_message = await replied_message.copy(chat_id=f'@{channel_id}')
    back_slash = '\\'
    if replied_message.text:
        await context.bot.edit_message_text(
            chat_id=f'@{channel_id}',
            message_id=new_message.message_id,
            text=f"#分享发现 {replied_message.text_markdown_v2_urled.replace(back_slash,'')}"
        )
    else:
        await context.bot.edit_message_caption(
            chat_id=f'@{channel_id}',
            message_id=new_message.message_id,
            caption=f"#分享发现 {replied_message.caption if replied_message.caption else ''}"
        )


async def tv(update: Update, context: CallbackContext):
    replied_message = update.effective_message.reply_to_message
    new_message = await replied_message.copy(chat_id=f'@{channel_id}')
    back_slash = '\\'
    if replied_message.text:
        await context.bot.edit_message_text(
            chat_id=f'@{channel_id}',
            message_id=new_message.message_id,
            text=f"#上电视 {replied_message.text_markdown_v2_urled.replace(back_slash,'')}"
        )
    else:
        await context.bot.edit_message_caption(
            chat_id=f'@{channel_id}',
            message_id=new_message.message_id,
            caption=f"#上电视 {replied_message.caption if replied_message.caption else ''}"
        )


async def news(update: Update, context: CallbackContext):
    replied_message = update.effective_message.reply_to_message
    new_message = await replied_message.copy(chat_id=f'@{channel_id}')
    back_slash = '\\'
    if replied_message.text:
        await context.bot.edit_message_text(
            chat_id=f'@{channel_id}',
            message_id=new_message.message_id,
            text=f"#小事 {replied_message.text_markdown_v2_urled.replace(back_slash,'')}"
        )
    else:
        await context.bot.edit_message_caption(
            chat_id=f'@{channel_id}',
            message_id=new_message.message_id,
            caption=f"#小事 {replied_message.caption if replied_message.caption else ''}"
        )


async def get_chat_id(update: Update, context: CallbackContext):
    await context.bot.send_message(dev_user_id, update.effective_chat.id)


async def get_question_analysis(update: Update, context: CallbackContext):
    questions_count = context.bot_data.get('questions_count', 0)
    feedback_count = context.bot_data.get('questions_feedback_count', 0)
    text = (
        f"晚上好，我们本周共发出 {questions_count} 个灵感买家的问题，并收到了 {feedback_count} 条反馈。\n\n"
        "这一周你都在思考些什么呢？欢迎填表分享你的问题，帮助更新我们的灵感买家问题库。"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text="分享你的问题",
                url=manifest.url+'?start=add_a_question'
            )
        )
    )
    # context.bot_data['questions_count'] = 0
    # context.bot_data['questions_feedback_count'] = 0


async def get_notion_database(update: Update, context: CallbackContext):
    database_id = await notion.get_database()
    await update.effective_message.reply_markdown(f"数据库 ID：`{database_id}`")


async def command_in_group_without_reply(update: Update, context: CallbackContext):
    await update.effective_message.reply_text(
        text=(
            '嗨，你可以这样使用 bot：\n\n'
            '1. 如果想要新发一条内容：在内容旁添加 #分享发现 或 #上电视 的标签，这样就能让本条内容同步到《野鱼日报》频道。\n'
            '2. 如果已经发了一条内容：先 reply 这条消息，然后输入 /，选择相应的命令如「分享发现」或「上电视」，同样能实现消息同步。'
        )
    )


async def test_recent_analysis(update: Update, context: CallbackContext):
    questions = context.bot_data.get('recent_questions')
    feedback_count = context.bot_data.get('recent_feedbacks')
    content = ''
    for question in questions:
        content += f"{question['content']}\nhttps://t.me/qna25/{question['message_id']}\n\n"
    text = (
        f"各位晚上好，今天我们发出了 3 条来自灵感买家的问题，并收到 {feedback_count} 条反馈，点击链接看看大家是如何回答的吧！\n\n"
        f"{content}"
    )
    await update.message.reply_text(text, disable_web_page_preview=True)