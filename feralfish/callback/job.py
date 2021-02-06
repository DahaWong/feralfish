from config import group_id
import random

# validate!
def send_poll(context):
    msg = context.bot_data.get('msg')
    if msg:
        msg.unpin()
        context.bot.stop_poll(chat_id=group_id, message_id=msg.message_id)
    context.bot_data.clear()

    hi = random.choice(['嗨','Hey','早','早上好','Yo','Hi'])
    how = random.choice(['心情怎么样','心情如何'])

    msg = context.bot.send_poll(
        chat_id=group_id,
        question=f'{hi}，今天的{how}？',
        options=[
            '🏝',
            '🌤',
            '🌦',
            '🌧',
            '🌪'
        ],
        allows_multiple_answers=False,
        is_anonymous=False
    )

    poll_id = msg.poll.id
    msg.pin()
    context.bot_data.update({'score': 0, 'count': 0, 'msg': msg, 'poll_id': poll_id})
