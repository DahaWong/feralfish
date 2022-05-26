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
question_group_id = int(config['QUESTIONS']['GROUP_ID'])
question_channel_name = config['QUESTIONS']['CHANNEL_NAME']
persistence = PicklePersistence('persistence')

notion_token = config['NOTION']['TOKEN']
notion_database_id = config['NOTION']['DATABASE_ID']


class manifest:
    name = "野鱼"
    group_name = "野鱼日报"
    bot_id = "FeralFishBot"
    url = "https://t.me/FeralFishBot"
    author = "Daha"
    author_id = 'dahawong'
    author_url = "https://daha.me/"
    version = "1.1.0"
    discription = ""
    repo = "https://github.com/dahawong/feralfish"


private_commands = [
    BotCommand('start', '开始'),
    BotCommand('about', '关于'),
    BotCommand('question', '分享最近困扰你的问题'),
]

group_commands = [
    BotCommand('tv', '上电视'),
    BotCommand('news', '小事'),
    BotCommand('share', '分享发现'),
]
