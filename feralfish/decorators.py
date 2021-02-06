from functools import wraps
from config import channel_owner, dev_user_id, manifest
__all__ = ['club', 'dev']


def club(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        message = update.message or update.edited_message
        if not message:
            return
        admins = message.chat.get_administrators()
        if admins and (channel_owner not in map(lambda x: x.user.id, admins)):
            message.reply_text('当前群聊还不是一个业余公司！')
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def dev(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if update.message.from_user.id not in [dev_user_id, channel_owner]:
            update.message.reply_text(f'您没有{manifest.name}专线的获取权 :)')
            return
        return func(update, context, *args, **kwargs)
    return wrapped
