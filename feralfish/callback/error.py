from telegram import Update
from telegram.ext import CallbackContext
from config import dev_user_id, manifest
import sys
import traceback


async def handle(update: Update, context: CallbackContext):
    if not update:
        return
    if update.effective_message:
        text = f"刚刚的操作触发了一个错误，报告已抄送给[开发者](https://t.me/{manifest.author_id})。"
        await update.effective_message.reply_markdown(text)
    payload = ""
    if update.effective_user:
        payload += f"有[用户](tg://user?id={update.effective_user.id})"
    if update.effective_chat and update.effective_chat.title:
        payload += f"在{update.effective_chat.title}"
        if update.effective_chat.username:
            payload += f'(@{update.effective_chat.username})'
    if update.poll:
        payload += f'在发起投票 {update.poll.id} 时'
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    text = f"{payload}触发了一个错误：`{context.error}`。\n\n"
    text += f"错误路径如下:\n`{trace}`" if trace else ''
    await context.bot.send_message(dev_user_id, text)
    raise context.error
