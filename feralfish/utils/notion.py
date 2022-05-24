'''
Todo
1. 添加入场问题对话
2. Network Error handling
'''

from notion_client import AsyncClient
import config
from pprint import pprint

client = AsyncClient(auth=config.notion_token)


async def get_database():
    res = await client.search(
        **{
            'query': '二五仔',
            'filter': {
                'value': 'database',
                'property': 'object'
            }
        }
    )
    database_id = res.get('results')[0].get('id')
    return database_id


async def create_page(title):
    res = await client.pages.create(
        **{
            'parent': {'database_id': config.notion_database_id},
            'properties': {
                '问题': {
                    'title': [
                        {
                            'text': {
                                'content': title,
                            },
                        },
                    ],
                },
                '状态': {
                    'select': {
                        'name': '未处理',
                    },
                },
            }
        }
    )
    # pprint(res)
    return True
