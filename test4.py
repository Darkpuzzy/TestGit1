from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import aiohttp
import websockets
import requests
from lxml import etree
from urllib.request import urlopen
import re


""" 
 Задача: 1. Валидатор для текста enter и сравнения game_name Rising_Storm_2
 """


async def valid(name):
    if isinstance(name, str):
        text_for_site = name
        list_split = text_for_site.split(" ")
        list_to_join = "_".join(list_split)
        list_to_str = list_to_join
        return list_to_str


async def validlink(name):
    if isinstance(name, str):
        text_for_site = name
        list_split = text_for_site.split(" ")
        list_to_join = "+".join(list_split)
        list_to_str = list_to_join
        return list_to_str

FUA = UserAgent().chrome

enter = 'Rising Storm 2 Vietnam'
steam = f'https://store.steampowered.com/search/?term=Rising+Storm+2' # Rising+Storm+2 #hitman+2 Disco_Elysium__The_Final_Cut Disco+Elysium+The+Final+Cut
HTMLPARCE = etree.HTMLParser()
req_link = requests.get(steam, headers={'User-Agent': FUA})
codetxt = req_link.text
with open('SteamHTML', 'w', encoding='utf-8') as f:
    f.write(codetxt)
local = 'file:///C:/Users/user/AioAsync/SteamHTML'
respones = urlopen(local)
tree = etree.parse(respones, HTMLPARCE)


async def links(arg: str):

    list_links = []

    for n in range(1, 20):
        j = tree.xpath(f"//div[@id='search_resultsRows']/a[{n}]")
        advacii = j[-1].attrib
        if arg in advacii['href']:
            list_links.append(advacii['href'])
        elif arg.capitalize() in advacii['href']:
            list_links.append(advacii['href'])
        elif arg.upper() in advacii['href']:
            list_links.append(advacii['href'])

    if not list_links:
        interim_list = []
        j1 = tree.xpath(f"//div[@id='search_resultsRows']/a[1]")
        advac = j1[-1].attrib
        interim_list.append(advac['href'])
        tasks = asyncio.create_task(spliter(list_cheak=interim_list, game_name=None))
        game_name = await asyncio.gather(tasks)
        enter = game_name[0]
        return await links(arg=enter)
    # print(list_links)
    return list_links


async def spliter(list_cheak, game_name):
    list_split = []
    n = 0
    game_n = await valid(game_name)
    while n < len(list_cheak):
        for i in list_cheak:
            j = i.split('/')
            list_split.extend(j)
            n += 1

    if game_n != None:

        async def find_game_id(list_cheaker, game):
            try:
                index_game = list_cheaker.index(game)
                game_id = list_cheaker[index_game - 1]
                return game_id
            except ValueError:
                ind = 0
                while True:
                    if game.lower() == list_cheaker[ind].lower():
                        game_id = list_cheaker[ind-1]
                        break
                    else:
                        ind += 1
                        continue
            return game_id
        return await find_game_id(list_cheaker=list_split, game=game_n)
    else:
        return list_split[5]


async def linkers(id, list_game):
    for j in list_game:
        if id in j:
            print(j)
            return j
""" <div class="discount_final_price">253 pуб.</div> <div class="discount_original_price">725 pуб.</div>  """

""" PARSE PRICE """


async def answer():
    task = asyncio.create_task(linkers(id=await spliter(await links(enter), game_name=enter), list_game=await links(enter)))
    res = await asyncio.gather(task)
    html_link = res[0]
    req = requests.get(html_link, headers={'User-Agent': FUA})
    code_txt = req.text
    soup = BeautifulSoup(code_txt, 'lxml')
    price = soup.find_all('script', type="text/javascript")
    old_price = soup.find_all('div', class_='game_purchase_price price')
    return html_link


async def parse():
    steam1 = f'{await answer()}'
    HTMLPARCE1 = etree.HTMLParser()
    req_link1 = requests.get(steam1, headers={'User-Agent': FUA})
    codetxt1 = req_link1.text
    with open('SteamHTMLparse', 'w', encoding='utf-8') as f1:
        f1.write(codetxt1)
    local1 = 'file:///C:/Users/user/AioAsync/SteamHTMLparse'
    respones1 = urlopen(local1)
    tree1 = etree.parse(respones1, HTMLPARCE1)
    j1 = tree1.xpath(f"//div[@class='game_area_purchase_game_wrapper']//div[@class='game_purchase_price price']")
    j2 = tree1.xpath(f"//div[@class='game_area_purchase_game_wrapper']//div[@class='discount_final_price']")
    j3 = tree1.xpath(f"//div[@class='game_area_purchase_game_wrapper']//div[@class='discount_original_price']")
    list_test = []
    if len(j3) > 0:
        for i in j2:
            priceascii = i.text
            p1 = re.search("\d[0-9]\d", str(priceascii))
            list_test.append(p1.group())
            print('J2')
    else:
        for i in j1:
            priceascii = i.text
            p1 = re.search("\d[0-9]\d", str(priceascii))
            list_test.append(p1.group())
            print('J1')
    return list_test



if __name__ == '__main__':
    txt_input = 'Rising Storm 2'
    loop = asyncio.get_event_loop()
    tasks = loop.create_task(parse())
    res = asyncio.gather(tasks)
    print(loop.run_until_complete(res)[0])
    # print(loop.run_until_complete(wait_tasks)) # Elden Ring, Rising Storm 2 Vietnam, Fallout 3, Fallout New Vegas
    loop.close()



#span[@class='title']
#for el in j:
    #print(el)
    #print(dir(el))
#GameName = i.findAll('a', class_ = 'search_result_row ds_collapse_flag')
# <meta itemprop="price" content="1199"> ||||||| price = priceascii.encode('utf-8')
""" data-price-final="33100">
<div class="discount_pct">-80%</div>
<div class="discount_prices">
<div class="discount_original_price">1659 pуб. """