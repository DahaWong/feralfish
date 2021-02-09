from telegram.ext import Updater
from config import update_info_test
from feralfish.handlers import register_handlers
from datetime import time
from feralfish.callback import job

updater = Updater(**update_info_test)
register_handlers(updater.dispatcher)

#Jobs
# updater.job_queue.run_once(callback=job.send_poll, when=1)

updater.start_polling()
updater.idle()
