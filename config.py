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
    author_url = "https://dreamlong.design/"
    version = "1.2.0"
    discription = ""
    repo = "https://github.com/dahawong/feralfish"


private_commands = [
    BotCommand('about', '关于野鱼机器人'),
    BotCommand('question', '分享一则让你疑惑的问题'),
]

dev_commands = [
    BotCommand('about', '关于野鱼机器人'),
    BotCommand('question', '分享一则让你疑惑的问题'),
    BotCommand('init', '初始化命令范围'),
    BotCommand('get_bot_data', '获取机器人数据'),
    BotCommand('test_recent_analysis', '测试今日问题分析'),
]

group_commands = [
    BotCommand('tv', '上电视：分享你的新作品或作品新进展'),
    BotCommand('share', '分享发现：分享所见所闻，如：文章、音乐…'),
    BotCommand('news', '小事：分享你与俱乐部会员间发生的小事'),
]
