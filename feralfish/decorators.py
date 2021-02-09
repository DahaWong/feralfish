from functools import wraps
from config import channel_owner, dev_user_id, manifest, channel_id, group_id
__all__ = ['club', 'dev']


def club(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        message = update.effective_message
        if update.effective_chat.id != group_id:
            message.reply_text('我只为鮀浦镇服务！')
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def channel(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        message = update.effective_message
        if update.effective_chat.username != channel_id:
            message.reply_text('我只为野鱼日报服务！')
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def dev(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if update.message.from_user.id not in [dev_user_id, channel_owner]:
            update.message.reply_text(f'您没有获取{manifest.name}专线的权利 :)')
            return
        return func(update, context, *args, **kwargs)
    return wrapped
