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
application.job_queue.run_daily(
    callback=job.send_poll, 
    time=time(7, 00, tzinfo=SHANGHAI)
)  # 早上七点

# 运营初期，每周二周五晚上发送一条总结消息到野鱼日报：
application.job_queue.run_daily(
    callback = job.send_recent_analysis, 
    days = (2,4),  # 周二周五
    time=time(21, 00, tzinfo=SHANGHAI) # 晚上九点
)  

# 每周日晚上发送一条总结消息与问题征集到野鱼日报和 qna25 频道：
application.job_queue.run_daily(
    callback=job.send_analysis,
    days=(6,),  # 周日
    time=time(21, 10, tzinfo=SHANGHAI)  # 晚上九点
)

application.run_polling()
