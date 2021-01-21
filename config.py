import configparser
# from utils.persistence import persistence
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
channel_owner_id = config['CHANNEL']['OWNER_ID']

# Build
update_info = {
    'token': bot_token,
    'use_context': True,
    #    'base_url': bot_api,
    'request_kwargs': {
        'proxy_url': proxy
    },
    'defaults': defaults,
    'workers': 16
}
