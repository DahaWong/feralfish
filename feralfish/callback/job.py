from config import group_id


# validate!
def send_poll(context):
    msg = context.bot_data.get('msg')
    if msg:
        msg.unpin()
        context.bot.stop_poll(chat_id=group_id, message_id=msg.message_id)
    context.bot_data.clear()

    msg = context.bot.send_poll(
        chat_id=group_id,
        question='嗨，今天的心情怎么样？',
        options=[
            '☀️',
            '🌥',
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
