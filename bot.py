from telegram.ext import Updater
from config import update_info
from feralfish.handlers import register_handlers
from datetime import time
from feralfish.callback import job

updater = Updater(**update_info)
register_handlers(updater.dispatcher)

#Job
updater.job_queue.run_once(callback=job.send_poll, when=1)
updater.job_queue.run_daily(job.send_poll, time=time(23,00))

# Polling
updater.start_polling()
updater.idle()
