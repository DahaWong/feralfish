from config import channel_id, group_id
from feralfish.utils import notion
from telegram.ext import ConversationHandler


async def send_to_channel(update, context):
    message = update.effective_message
    if message.from_user.id == 777000:
        return
    await message.forward(chat_id=f'@{channel_id}')


async def send_to_group(update, context):
    await update.effective_message.copy(chat_id=group_id)


async def count_questions(update, context):
    message = update.effective_message
    if message.is_automatic_forward and message.forward_signature == '一位灵感买家':
        context.bot_data['questions_count'] = context.bot_data.get(
            'questions_count', 0) + 1
    elif message.reply_to_message and message.reply_to_message.is_automatic_forward:
        context.bot_data['questions_feedback_count'] = context.bot_data.get(
            'questions_feedback_count', 0) + 1


async def add_question_to_notion(update, context):
    question = update.message.text
    await notion.create_page(title=question)
    await update.message.reply_markdown(f"问题收到啦，感谢分享！")
    return ConversationHandler.END


async def delete_state(update, context):
    await update.effective_message.delete()


async def handle_legacy(update, context):
    await update.effective_message.delete()
