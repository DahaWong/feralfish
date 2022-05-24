from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import group_id, channel_id, question_channel_name, manifest
import random


async def send_poll(context):
    msg = context.bot_data.get('msg')
    if msg:
        await msg.unpin()
        await context.bot.stop_poll(chat_id=group_id, message_id=msg.message_id)
    context.bot_data.clear()

    hi = random.choice(['嗨', 'Hey', '早', '早上好', 'Yo', 'Hi'])
    how = random.choice(['心情怎么样', '心情如何'])

    msg = await context.bot.send_poll(
        chat_id=group_id,
        question=f'{hi}，今天的{how}？',
        options=[
            random.choice(['🏝', '🏞️', '🏖', '🌅']),
            '🌤',
            '🌦',
            '🌧',
            random.choice(['🌪', '❄️'])
        ],
        allows_multiple_answers=False,
        is_anonymous=False
    )

    poll_id = msg.poll.id
    await msg.pin()
    context.bot_data.update(
        {'score': 0, 'count': 0, 'msg': msg, 'poll_id': poll_id})


async def send_analysis(context):
    questions_count = context.bot_data.get('questions_count', 0)
    feedback_count = context.bot_data.get('questions_feedback_count', 0)
    if feedback_count:
        text = (
            f"晚上好，我们本周共发出 {questions_count} 个灵感买家的问题，并收到了 {feedback_count if feedback_count else 0} 条反馈。\n\n"
            "这一周你都在思考些什么呢？欢迎填表分享你的问题，帮助更新我们的灵感买家问题库。"
        )
    else:
        text = (
            f"晚上好，我们本周共发出 {questions_count} 个灵感买家的问题，不过还没收到大家的反馈。\n\n"
            "这一周你都在思考些什么呢？欢迎填表分享你的问题，帮助更新我们的灵感买家问题库。"
        )
    await context.bot.send_message(
        chat_id=f"@{channel_id}",
        text=text,
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text="分享你的问题",
                url=manifest.url+'?start=add_a_question'
            )
        )
    )
    await context.bot.send_message(
        chat_id=f"@{question_channel_name}",
        text=text,
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text="分享你的问题",
                url=manifest.url+'?start=add_a_question'
            )
        )
    )
    context.bot_data.pop('questions_feedback_count')
    context.bot_data.pop('questions_count')
