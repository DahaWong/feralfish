from config import group_id
moods = [10, 7.5, 5, 0]
weather = ['🌪', '⛈', '🌨', '🌧', '☔️', '☂️', '🌦',  '⛅️', '🌥', '🌤', '☀️']

def handle_poll_answer(update, context):
    context.bot_data['count'] += 1
    mood = moods[update.poll_answer.option_ids[0]]
    context.bot_data['score'] += mood
    weather_symbol = weather[round(context.bot_data['score']/context.bot_data['count'])]
    # context.bot.set_chat_title(chat, weather_symbol)
    context.bot.set_chat_description(group_id, f"太阳能维修，夜总会发光。\n\n鮀浦镇今日天气：{weather_symbol}")
