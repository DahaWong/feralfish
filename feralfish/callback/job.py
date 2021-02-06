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
        question='早上好！今天的心情如何？',
        options=[
            '非常好',
            '还不错',
            '一般般',
            '糟透了'
        ],
        allows_multiple_answers=False,
        is_anonymous=False
    )

    msg.pin()
    poll_id = msg.poll.id
    context.bot_data.update({'score': 0, 'count': 0, 'msg': msg, 'poll': poll_id})
