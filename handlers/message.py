from telegram.ext import MessageHandler, Filters
import callbacks.message as callback

links_handler = MessageHandler(Filters.entity("url") & Filters.regex(r'#yeyu'), callback.send_to_channel)

handlers=[feed_handler, subscription_handler, exit_handler, episode_handler]