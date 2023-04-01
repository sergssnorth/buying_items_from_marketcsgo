from bs4 import BeautifulSoup
from decimal import Decimal
from urllib.parse import unquote
import json
import re
import requests


def scraping_tradeback_comprassion(html):
    item_list = list()
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find(id="table-body")
    items = table.find_all('tr')
    for item in items:
        try:
            name = str(item.find('td', class_='copy-name').string)
        except Exception as Ex:
            print(ex)
            name = "No name"

        # Info Steam
        info_steam = item.find(attrs={"data-link-key": "steamcommunity"})
        try:
            steam_last_sales_container = info_steam.find('div', class_='last-sales-container')
            steam_last_sales = steam_last_sales_container.find('div', class_='last-sales-list')

            steam_finish_sales = [element.get_text() for element in
                                  steam_last_sales.find('div', class_='last-sales-row prices title').find_all('div')]
            steam_last_sales_avg = (steam_finish_sales[3].split('$'))[0]
            steam_last_sales_avg = Decimal(''.join(steam_last_sales_avg))
            steam_last_sales_max = (steam_finish_sales[5].split('$'))[0]
            steam_last_sales_max = Decimal(''.join(steam_last_sales_max))
        except AttributeError as ex:
            steam_last_sales_avg = Decimal('0')
            steam_last_sales_max = Decimal('0')

        # Info Tm
        try:
            info_tm = item.find(attrs={"data-link-key": "tm"})
            tm_link = (info_tm.find('a'))['href']
            tm_link_decode = unquote(tm_link)
        except Exception as ex:
            tm_link_decode = 'no link'
        try:
            game = 'no game'
            if 'csgo' in tm_link_decode:
                game = 'csgo'
            elif 'dota2' in tm_link_decode:
                game = 'dota2'
            elif 'tf2' in tm_link_decode:
                game = 'tf2'
            elif tm_link_decode == 'no link':
                game = 'rust'
        except Exception as ex:
            game = 'no game'

        # Info First_Service
        info_first_service = item.find(attrs={"data-column": "first"})
        first_service_price = info_first_service.find('div', class_='first-line')
        first_service_price_rub = first_service_price.find('span', class_='price rub').get_text()
        first_service_price_usd = first_service_price.find('span', class_='price-converted').get_text()
        first_service_price_rub = Decimal(str(first_service_price_rub))
        first_service_price_usd = Decimal(str(first_service_price_usd))

        # Info Second_Service
        info_second_service = item.find(attrs={"data-column": "second"})
        second_service_price = info_second_service.find('div', class_='first-line')
        second_service_price_usd = second_service_price.find('span').get_text()
        second_service_price_usd = Decimal(str(second_service_price_usd))

        #Procent First to Second
        procent_first_service = item.find(attrs={"data-column": "first","class": "field-profit" }).get_text()
        procent_first_service = Decimal(procent_first_service)

        item_list.append(
            {'name': name, 'game': game,
             'steam_info': {'steam_last_sales_avg': steam_last_sales_avg,
                            'steam_last_sales_max': steam_last_sales_max},
             'info_first_service' : {'first_service_price_rub':first_service_price_rub,
                                     'first_service_price_usd': first_service_price_usd},
             'info_second_service': {'second_service_price_usd':second_service_price_usd},
             'procent_first_service' : procent_first_service
             })
    return item_list


# def history_sale(item_url:str):
#     try:
#         rs = requests.get(item_url)
#         m = re.search(r'var line1=(.+);', rs.text)
#         data_str = m.group(1)
#         data = json.loads(data_str)
#         return data
#     except Exception as ex:
#         return None


def filter_out_items(items:list,course:Decimal,procent:int):
    filtred_items = list()
    procent = Decimal(procent/100)

    for item in items:
        name = item['name']
        if "Artificer's Hammer" in name:
            continue
        if "Artificer's Chisel" in name:
            continue
        if "Master Artificer's Hammer" in name:
            continue

        game = item['game']
        if game == 'rust':
            continue
        if game == 'tf2':
            continue

        price_steam_avg = item['steam_info']['steam_last_sales_avg']
        price_steam_max = item['steam_info']['steam_last_sales_max']
        price_tm_rub = item['info_first_service']['first_service_price_rub']
        price_tm_usd = item['info_first_service']['first_service_price_usd']
        price_steam = item['info_second_service']['second_service_price_usd']

        price_sell_item_in_steam_with_comission = (price_steam - (price_steam * Decimal("0.13")))
        finish_procent = price_sell_item_in_steam_with_comission/price_tm_usd - Decimal("1")

        price_steam_avg_with_comission = price_steam_avg - (Decimal("0.13") * price_steam_avg) + (price_steam_avg * Decimal("0.03"))
        price_tm_with_condition = price_tm_usd + (price_tm_usd * procent)

        if(price_steam_avg_with_comission >= price_tm_with_condition and finish_procent >= procent
                and price_sell_item_in_steam_with_comission >= price_tm_with_condition
                and price_steam_max <= (price_steam_avg * Decimal(2))):
            if price_sell_item_in_steam_with_comission <= price_steam_avg_with_comission:
                new_price = (price_sell_item_in_steam_with_comission/ (procent + Decimal(1))) * course
                filtred_items.append({'name': name, 'game': game, 'new_price': new_price})
            elif price_steam_avg_with_comission < price_sell_item_in_steam_with_comission:
                new_price = (price_steam_avg_with_comission / (procent + Decimal(1))) * course
                filtred_items.append({'name': name, 'game': game, 'new_price': new_price})
        else:
            pass
    return filtred_items


def get_price_item_from_marketcsgo(html):
    instances_of_items_list = list()
    soup = BeautifulSoup(html, 'lxml')
    body_items = soup.find(id="applications")
    all_instances_of_items = body_items.select('#applications>.item')
    for instance_of_item in all_instances_of_items:
        item_link = instance_of_item['href']
        item_link = unquote(item_link)

        item_price_rub = instance_of_item.select_one('#applications>.item .price').get_text()
        item_price_rub= item_price_rub.split('\xa0')
        item_price_rub = item_price_rub[0]
        if ' ' in item_price_rub:
            item_price_rub = item_price_rub.split(' ')
            item_price_rub = ''.join(item_price_rub)
        item_price_rub = Decimal(item_price_rub)

        item_name = instance_of_item.select_one('#applications>.item>.name').get_text()
        item_name = item_name.split('\n')
        item_name = item_name[1]
        instances_of_items_list.append({'item_name': item_name, 'item_price_rub':item_price_rub,'item_link': item_link})

    return instances_of_items_list


def get_price_item_from_marketcsgo_second(html):
    instances_of_items_list = list()
    soup = BeautifulSoup(html, 'lxml')
    body_item = soup.select_one('.item-page-left')
    item_price_rub = body_item.select_one('.item-page-left>.ip-price>.ip-bestprice').get_text().strip()
    if ' ' in item_price_rub:
        item_price_rub = item_price_rub.split(' ')
        item_price_rub = ''.join(item_price_rub)
    item_price_rub = float(item_price_rub)

    return item_price_rub