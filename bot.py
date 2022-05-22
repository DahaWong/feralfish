from telegram.ext import ApplicationBuilder
import config
from feralfish.handlers import register_handlers
from datetime import time
from feralfish.callback import job

application = ApplicationBuilder().token(
    config.bot_token).persistence(config.persistence).build()

register_handlers(application)

application.job_queue.run_daily(job.send_poll, time=time(23, 00))

application.run_polling()
