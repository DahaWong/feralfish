from config import group_id
import random
moods = [10, 7.5, 5, 2.5, 0]


async def handle_poll_answer(update, context):
    weather = ['🌪', random.choice(['⛈️', '❄️', '🌨']), '🌧', '☔️', '☂️', '🌦',
               '☁️',  '⛅️', '🌤', random.choice(['🏝', '🏞️', '🏖', '🌅', '💫', '☀️']), '🏝']
    if context.bot_data.get('poll_id') != update.poll_answer.poll_id:
        return

    context.bot_data['count'] += 1
    mood = moods[update.poll_answer.option_ids[0]]
    context.bot_data['score'] += mood
    weather_symbol = weather[round(
        context.bot_data['score']/context.bot_data['count'])]
    await context.bot.set_chat_title(group_id, f"{weather_symbol} 鮀浦镇｜灵感买家俱乐部")
