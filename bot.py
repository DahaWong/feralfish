from telegram.ext import ApplicationBuilder
import config
from feralfish.handlers import register_handlers
from datetime import time
from dateutil import tz
from feralfish.callback import job

SHANGHAI = tz.gettz('Asia/Shanghai')

application = ApplicationBuilder().token(
    config.bot_token).persistence(config.persistence).build()
register_handlers(application)
application.job_queue.run_daily(job.send_poll, time=time(23, 00))  # 早上qi点
application.job_queue.run_daily(
    callback=job.send_analysis,
    days=(6,),  # 周日
    # days=(1,),  # 周二
    time=time(21, 00, tzinfo=SHANGHAI)  # 晚上九点
)

application.run_polling()
