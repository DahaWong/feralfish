from config import channel_id, group_id


async def send_to_channel(update, context):
    message = update.effective_message
    if message.from_user.id == 777000:
        return
    await message.forward(chat_id=f'@{channel_id}')


async def send_to_group(update, context):
    await update.effective_message.copy(chat_id=group_id)


async def delete_state(update, context):
    await update.effective_message.delete()


async def handle_legacy(update, context):
    await update.effective_message.delete()
