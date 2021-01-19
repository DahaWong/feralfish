import configparser
from utils.persistence import persistence
from telegram.ext import Defaults

config = configparser.ConfigParser()
config.read('config.ini')


# Bot
bot_token = config['BOT']['TOKEN']
proxy = config['BOT']['PROXY']
defaults = Defaults(
    parse_mode="MARKDOWN", 
    disable_notification=True, 
    run_async=True
)

# Dev
dev_user_id = config['DEV']['ID']

# Channel
channel_id = config['CHANNEL']['ID']


# Build
update_info = {
   'token': bot_token,
   'use_context': True,
   'persistence': persistence,
   'base_url': bot_api,
   'defaults': defaults,
   'workers': 16
 }
