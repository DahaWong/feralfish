from config import group_id
moods = [10, 7.5, 5, 2.5, 0]
weather = ['🌪', '⛈', '🌨', '🌧', '☔️', '☂️', '🌦',  '⛅️', '🌥', '🌤', '☀️']

def handle_poll_answer(update, context):
    if context.bot_data['poll_id'] != update.poll_answer.poll_id:
        return

    context.bot_data['count'] += 1
    mood = moods[update.poll_answer.option_ids[0]]
    context.bot_data['score'] += mood
    weather_symbol = weather[round(context.bot_data['score']/context.bot_data['count'])]
    context.bot.set_chat_title(group_id, f"{weather_symbol} 鮀浦镇｜灵感买家俱乐部")
    
    # context.bot.set_chat_description(update.effective_chat.id, (
    #     f"太阳能维修，夜总会发光。\n\n"
    #     f"鮀浦镇今日天气：{weather_symbol}"
    #     )
    # )
