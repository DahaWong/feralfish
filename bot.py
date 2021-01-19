from config import update_info
from telegram.ext import Updater
from handlers.register import register

updater = Updater(**update_info)
dispatcher = updater.dispatcher

# Use this method to logout your bot from telegram api cloud:
#updater.bot.log_out()

# Use these methods before you move your bot to another local server:
# updater.bot.delete_webhook() 
# updater.bot.close()

# if not dispatcher.bot_data:
#     updater.dispatcher.bot_data.update({"podcasts":{}})

register(updater.dispatcher)

# Polling:
updater.start_polling()
updater.idle()
