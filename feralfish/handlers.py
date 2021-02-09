from telegram.ext import CommandHandler, MessageHandler, Filters, PollAnswerHandler
from feralfish.callback import message, command, poll, error

command_handlers = [
    CommandHandler('start', command.start),
    CommandHandler('about', command.about),
    CommandHandler('help', command.help),
    CommandHandler('share', command.share),
    CommandHandler('yeyu', command.yeyu),
    CommandHandler('proxy', command.show_proxy)
]

message_handlers = [
    MessageHandler(
        Filters.chat_type.groups &
        Filters.update.messages &
        Filters.regex(r'#(?:上电视|野鱼屏幕|分享发现)'),
        message.send_to_channel
    ),
    MessageHandler(
        Filters.chat_type.groups & (
            Filters.status_update.pinned_message |
            Filters.status_update.left_chat_member |
            Filters.status_update.new_chat_members |
            Filters.status_update.new_chat_title
        ),
        message.delete_state
    ),
    MessageHandler(
        Filters.chat_type.channel &
        Filters.entity("url") & (
            # Filters.regex(r'youtube\.com') |
            Filters.regex(r'music\.163\.com')
        ), message.download_music),
    # MessageHandler(Filters.text, message.get_chat_id),
    PollAnswerHandler(poll.handle_poll_answer)
]

handlers = command_handlers.extend(message_handlers)


def register_handlers(dispatcher):
    for handler in command_handlers:
        dispatcher.add_handler(handler)
    # dispatcher.add_error_handler(error.handle)
