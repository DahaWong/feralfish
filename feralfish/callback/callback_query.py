from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext


async def cancel_add_question(update: Update, context: CallbackContext):
    await update.callback_query.answer(text='已取消', show_alert=True)
    await update.effective_message.delete()
    return ConversationHandler.END
