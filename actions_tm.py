import requests
import aiohttp
import asyncio
from decimal import *


async def buy_item(session, key, game, hash_name, price):
    if game == 'csgo':
        url = f'https://market-old.csgo.com/api/v2/buy?key={key}&hash_name={hash_name}&price={price}'
    elif game == 'dota2':
        url = f'https://market.dota2.net/api/v2/buy?key={key}&hash_name={hash_name}&price={price}'
    elif game == 'rust':
        url = f'https://rust.tm/api/v2/buy?key={key}&hash_name={hash_name}&price={price}'
    elif game == 'tf2':
        url = f'https://tf2.tm/api/v2/buy?key={key}&hash_name={hash_name}&price={price}'
    async with session.get(url) as resp:
        assert resp.status == 200
        resp = await resp.json()
        print(resp)


async def buy_all_filterd_items(api_key,filtred_items):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in filtred_items:
            game = item['game']
            name = item['name']
            price_tm_rub = item['new_price']

            quantize_price = price_tm_rub.quantize(Decimal('1.10'), rounding=ROUND_UP)
            finish_price = (str(quantize_price)).split('.')
            finish_price = ''.join(finish_price)

            task = asyncio.create_task(buy_item(session, api_key, game, name, finish_price))
            tasks.append(task)
        await asyncio.gather(*tasks)



