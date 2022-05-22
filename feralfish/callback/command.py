from telegram import BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats, InlineKeyboardButton, InlineKeyboardMarkup
from config import manifest, channel_id, dev_user_id, private_commands, group_commands


async def init(update, context):
    await context.bot.set_my_commands(commands=private_commands,
                                      scope=BotCommandScopeAllPrivateChats())
    await context.bot.set_my_commands(commands=group_commands,
                                      scope=BotCommandScopeAllGroupChats())
    await context.bot.send_message(dev_user_id, '指令初始化完成')


async def start(update, context):
    await update.effective_message.reply_markdown(
        f"你好，我是{manifest.name}！[{manifest.group_name}](https://t.me/{channel_id})的管家。")


async def about(update, context):
    keyboard = [[InlineKeyboardButton("源代码", url=manifest.repo),
                 InlineKeyboardButton("工作室", url=manifest.author_url)]]
    markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_markdown(
        text=(
            f"*{manifest.name}*  "
            f"`{manifest.version}`"
            f"\nby [{manifest.author}](https://t.me/{manifest.author_id})\n"
        ),
        reply_markup=markup
    )


async def share(update, context):
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


async def tv(update, context):
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


async def news(update, context):
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


async def get_chat_id(update, context):
    await context.bot.send_message(dev_user_id, update.effective_chat.id)


async def command_in_group_without_reply(update, context):
    await update.effective_message.reply_text(
        text=(
            '嗨，你可以这样使用 bot：\n\n'
            '1. 如果想要新发一条内容：在内容旁添加 #分享发现 或 #上电视 的标签，这样就能让本条内容同步到《野鱼日报》频道。\n'
            '2. 如果已经发了一条内容：先 reply 这条消息，然后输入 /，选择相应的命令如「分享发现」或「上电视」，同样能实现消息同步。'
        )
    )
