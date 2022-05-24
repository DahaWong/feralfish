from telegram.ext import ConversationHandler


async def cancel_add_question(update, context):
    await update.callback_query.answer(text='已取消', show_alert=True)
    await update.effective_message.delete()
    return ConversationHandler.END
