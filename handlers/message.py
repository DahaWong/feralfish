from telegram.ext import MessageHandler, Filters
import callbacks.message as callback

links_handler = MessageHandler(Filters.entity("url") & Filters.regex(r'#yeyu'), callback.send_to_channel)
tv_handler = MessageHandler(Filters.regex(r'#上电视'), callback.send_to_channel)

handlers=[links_handler]