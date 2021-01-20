from telegram.ext import MessageHandler, Filters
import callbacks.message as callback

share_handler = MessageHandler(Filters.entity("url") & Filters.regex(r'#分享发现'), callback.send_to_channel)
yeyu_handler = MessageHandler(Filters.regex(r'#野鱼屏幕'), callback.send_to_channel)
tv_handler = MessageHandler(Filters.regex(r'#上电视'), callback.send_to_channel)

handlers=[share_handler, yeyu_handler, tv_handler]