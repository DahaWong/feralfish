from telegram.ext import CommandHandler, MessageHandler, filters, PollAnswerHandler, ConversationHandler, CallbackQueryHandler
from feralfish.callback import message, command, poll, error, callback_query
import config

# Question-adding conversation handlers:
start_handler = CommandHandler('start', command.start)
question_command_handler = CommandHandler('question', command.question)

add_question_handler = MessageHandler(
    filters.UpdateType.MESSAGE & filters.TEXT & ~filters.COMMAND,
    message.add_question_to_notion
)

cancel_add_question_handler = CallbackQueryHandler(
    callback=callback_query.cancel_add_question,
    pattern=r'^cancel_adding_question'
)

questions_conversation_handler = ConversationHandler(
    entry_points=[start_handler, question_command_handler],
    states={
        0: [add_question_handler, cancel_add_question_handler],
    },
    fallbacks=[],
)

handlers = [
    CommandHandler('about', command.about),
    CommandHandler('share', command.share, filters.REPLY &
                   filters.Chat(config.group_id)),
    CommandHandler('tv', command.tv, filters.REPLY &
                   filters.Chat(config.group_id)),
    CommandHandler('news', command.news, filters.REPLY &
                   filters.Chat(config.group_id)),
    CommandHandler('id', command.get_chat_id),
    CommandHandler('q', command.get_question_analysis),
    CommandHandler('n', command.get_notion_database),
    CommandHandler('init', command.init, filters=filters.Chat(config.dev_user_id)),
    CommandHandler('get_bot_data', command.get_bot_data, filters=filters.Chat(config.dev_user_id)),
    CommandHandler('test_recent_analysis', command.test_recent_analysis, filters=filters.Chat(config.dev_user_id)),
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
        (filters.ChatType.GROUPS |
         filters.ChatType.CHANNEL) &
         (
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
    MessageHandler(
        filters.Chat(config.question_group_id) &
        ~filters.UpdateType.EDITED,
        message.count_questions
    ),
    PollAnswerHandler(poll.handle_poll_answer),
    questions_conversation_handler
]


def register_handlers(application):
    for handler in handlers:
        application.add_handler(handler)
    application.add_error_handler(error.handle)
