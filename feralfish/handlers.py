from telegram.ext import CommandHandler, MessageHandler, filters, PollAnswerHandler
from feralfish.callback import message, command, poll, error
import config

handlers = [
    CommandHandler('start', command.start),
    CommandHandler('about', command.about),
    CommandHandler('share', command.share, filters.REPLY &
                   filters.Chat(config.group_id)),
    CommandHandler('tv', command.tv, filters.REPLY &
                   filters.Chat(config.group_id)),
    CommandHandler('news', command.news, filters.REPLY &
                   filters.Chat(config.group_id)),
    CommandHandler('id', command.get_chat_id),
    CommandHandler('init', command.init),
    MessageHandler(filters.Chat(config.group_id) &
                   filters.COMMAND &
                   ~filters.REPLY, command.command_in_group_without_reply),
    MessageHandler(
        filters.Chat(config.group_id) &
        filters.UpdateType.MESSAGE &
        (filters.Regex(r'#(?:上电视|分享发现|小事)') |
         filters.CaptionRegex(r'#(?:上电视|分享发现|小事)')),
        message.send_to_channel
    ),
    MessageHandler(
        filters.Chat(username=config.channel_id) &
        filters.UpdateType.CHANNEL_POST &
        filters.Regex(r'#新人'),
        message.send_to_group
    ),
    MessageHandler(
        filters.ChatType.GROUPS & (
            filters.StatusUpdate.PINNED_MESSAGE |
            filters.StatusUpdate.LEFT_CHAT_MEMBER |
            # filters.StatusUpdate.NEW_CHAT_MEMBERS |
            filters.StatusUpdate.NEW_CHAT_TITLE),
        message.delete_state
    ),
    MessageHandler(
        filters.Chat(username="castpodchat") & (
            filters.Regex(r'^╳$') | filters.Regex(
                r'^随机波动StochasticVolatility$')
        ), message.handle_legacy),
    PollAnswerHandler(poll.handle_poll_answer)
]


def register_handlers(application):
    for handler in handlers:
        application.add_handler(handler)
    application.add_error_handler(error.handle)