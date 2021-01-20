# from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, constants
# from manifest import manifest
# from uuid import uuid4
# import re

# def handle_inline_query(update, context):
#     query = update.inline_query
# # 认证会员身份
#     query_text = query.query
#     member_match = re.match('^membe\(.*)', query_text)
#     results, kwargs = [], {"auto_pagination": True, "cache_time": 150}
#     if not query_text:
#         results, kwargs = welcome(query, context)
#     elif member_match:
#         keyword = member_a\match[1].lstrip(                                                                )
#         results = search_ 
#         results = show_episodes(query, context)
#         kwargs.update({"cache_time": 600})
#     query.answer(
#         results,
#         **kwargs
#     )

# def welcome(query, context):
#     if not context.user_data.get('user'):
#         results = []
#         kwargs = {
#             "switch_pm_text": "登 录",
#             "switch_pm_parameter": "login",
#             "cache_time": 0
#         }
#     else:
#         results = show_subscription(query, context)
#         kwargs = {}
#     return results, kwargs

# def search_podcast(query, keyword, context):
#     searched_results = search(keyword)
#     listed_results = []
#     if not searched_results:
#         listed_results = [
#             InlineQueryResultArticle(
#                 id = '0',
#                 title = "没有与此相关的播客呢 :(",
#                 description = "换个关键词试试",
#                 input_message_content = InputTextMessageContent("🔍️"),
#                 reply_markup=InlineKeyboardMarkup.from_button(
#                     InlineKeyboardButton('返 回 搜 索', switch_inline_query_current_chat=f"search {keyword}")
#                 )
#             )
#         ]
#     else:
#         for result in searched_results:
#             name = re.sub(r'[_*`]', ' ', result['collectionName'])
#             host = re.sub(r'[_*`]', ' ', result['artistName'])
#             feed = result['feedUrl']
#             thumbnail_full = result['artworkUrl600']
#             thumbnail_small = result['artworkUrl60']

#             # 如果不在 机器人主页，则：
#             # [InlineKeyboardButton('前  往  B O T', url = f"https://t.me/{manifest.bot_id}")],

#             result_item = InlineQueryResultArticle(
#                 id = result['collectionId'], 
#                 title = name, 
#                 input_message_content = InputTextMessageContent(feed),
#                 description = host,
#                 thumb_url = thumbnail_small,
#                 thumb_height = 60,
#                 thumb_width = 60
#             )
#             listed_results.append(result_item)
#     return listed_results

# def show_episodes(query, context):
#     keyword = query.query
#     podcasts = context.bot_data['podcasts']
#     listed_results = []
#     podcast = podcasts.get(keyword)
#     # if not podcast: ..
#     episodes = podcast.episodes
#     episodes_count = len(episodes)
#     # if context.user_data['preference'].get('reverse_episodes'): episodes.reverse()
#     keyboard = [[
#             InlineKeyboardButton("订  阅  列  表", switch_inline_query_current_chat=""),
#             InlineKeyboardButton("单  集  列  表", switch_inline_query_current_chat = f"{podcast.name}")
#     ]]
#     listed_results = [InlineQueryResultArticle(
#         id = index,
#         title = episode.title,
#         input_message_content = InputTextMessageContent((
#             f"[🎙️]({podcast.logo_url}) *{podcast.name}* #{episodes_count - index}"
#         )),
#         reply_markup = InlineKeyboardMarkup(keyboard),
#         description = f"{episode.duration or podcast.name}\n{episode.subtitle}",
#         thumb_url = podcast.logo_url,
#         thumb_width = 60, 
#         thumb_height = 60
#     ) for index, episode in enumerate(episodes)]
#     return listed_results

# def show_subscription(query, context):
#     subscription = context.user_data['user'].subscription
#     results = [InlineQueryResultArticle(
#             id = index,
#             title = feed.podcast.name,
#             input_message_content = InputTextMessageContent(PodcastPage(feed.podcast).text()),
#             reply_markup = InlineKeyboardMarkup(PodcastPage(feed.podcast).keyboard()),
#             description = feed.podcast.host or feed.podcast.name,
#             thumb_url = feed.podcast.logo_url,
#             thumb_width = 60, 
#             thumb_height = 60 
#         ) for index, feed in enumerate(subscription.values())]
#     return results

# def show_trending(context):
#     user = context.user_data['user']
#     podcasts = context.bot_data['podcasts']
#     results = [InlineQueryResultArticle(
#         id = uuid4(),
#         title = podcast.name,
#         description = podcast.host or podcast.name,
#         input_message_content = InputTextMessageContent((
#             f"{podcast.feed_url}"
#         )),
#         # reply_markup = InlineKeyboardMarkup(),
#         thumb_url = podcast.logo_url,
#         thumb_width = 60,
#         thumb_height = 60
#     ) for podcast in podcasts.values() if not user.subscription.get(podcast.name)]
#     return results