import configparser
from telegram.ext import Defaults, PicklePersistence

config = configparser.ConfigParser()
config.read('config.ini')
bot_token = config['BOT']['TOKEN']
bot_token_test = config['BOT']['TOKEN_TEST']
proxies = config['PROXIES']
proxy = config['BOT']['PROXY']
defaults = Defaults(
    parse_mode="MARKDOWN",
    disable_notification=True,
    run_async=True
)

dev_user_id = int(config['DEV']['ID'])  # daha
channel_owner = int(config['CHANNEL']['OWNER'])  # bob
channel_id = config['CHANNEL']['ID']
group_id = int(config['GROUP']['ID'])
persistence = PicklePersistence(filename='persistence', store_chat_data=False, store_user_data=False)

music_phone = config['MUSIC']['PHONE']
music_pwd = config['MUSIC']['PWD']
music_api = config['MUSIC']['API']
# Build
update_info = {
    'token': bot_token,
    'use_context': True,
    'defaults': defaults,
    'persistence': persistence
}

# Test
update_info_test = {
    'token': bot_token_test,
    'use_context': True,
    'defaults': defaults,
    'request_kwargs': {
        'proxy_url': proxy
    },
    'persistence': persistence
}


class manifest:
    name = "野鱼"
    group_name = "鮀浦日报"
    bot_id = "FeralFishBot"
    author = "Daha"
    author_id = 'dahawong'
    author_url = "https://office.daha.me/"
    version = "0.1.0"
    discription = ""
    repo = "https://github.com/dahawong/feralfish"
