import configparser
from telegram import BotCommand
from telegram.ext import Defaults, PicklePersistence

config = configparser.ConfigParser()
config.read('config.ini')
bot_token = config['BOT']['TOKEN']
bot_token_test = config['BOT']['TOKEN_TEST']
defaults = Defaults(
    parse_mode="MARKDOWN",
    disable_notification=True,
    block=False
)

channel_id = config['CHANNEL']['ID']
group_id = int(config['GROUP']['ID'])
dev_user_id = int(config['DEV']['ID'])
persistence = PicklePersistence('persistence')


class manifest:
    name = "野鱼"
    group_name = "野鱼日报"
    bot_id = "FeralFishBot"
    author = "Daha"
    author_id = 'dahawong'
    author_url = "https://daha.me/"
    version = "1.1.0"
    discription = ""
    repo = "https://github.com/dahawong/feralfish"


private_commands = [
    BotCommand('start', '开始'),
    BotCommand('about', '关于')
]

group_commands = [
    BotCommand('tv', '上电视'),
    BotCommand('news', '小事'),
    BotCommand('share', '分享发现'),
]