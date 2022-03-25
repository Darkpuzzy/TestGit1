from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import aiohttp
# import websockets
import requests
from lxml import etree
from urllib.request import urlopen

FUA = UserAgent().chrome
HTMLPARCE = etree.HTMLParser()


class Game:

    def __init__(self, text):
        self.text = text

    ''' parsing steam store '''

    async def steam_find(self):
        try:
            steam = 'https://store.steampowered.com/search/?term={}'.format(await validlink(name=self.text))
            req_link = requests.get(steam, headers={'User-Agent': FUA})
            codetxt = req_link.text
            with open('SteamHTML', 'w', encoding='utf-8') as f:
                f.write(codetxt)
            local = 'file:///C:/Users/user/AioAsync/SteamHTML'
            respones = urlopen(local)
            treex = etree.parse(respones, HTMLPARCE)
            task = asyncio.create_task(linkers(id=await spliter(await links(name=self.text, tree=treex), game_name=self.text), list_game=await links(name=self.text, tree=treex)))
            res1 = await asyncio.gather(task)
            return res1[0]
        except IndexError:
            return 'The game is not found, check if you entered the name correctly, or is missing from the store'

    ''' parsing zaka-zaka store '''

    async def zaka_find(self):
        if isinstance(await validator(text=self.text), str):
            try:
                zaka = 'https://zaka-zaka.com/game/{}'.format(await validator(text=self.text))
                code_txt = await test(text=await validator(text=self.text))
                soup = BeautifulSoup(code_txt, 'lxml')
                old_price = soup.find_all('div', class_='old-price')
                price_now = soup.find_all('div', class_='price')
                discount = soup.find_all('div', class_='discount')
                tasks = asyncio.create_task(price_game(oldprice=old_price, price=price_now, discount=discount, site_url=zaka))
                res2 = await asyncio.gather(tasks)
                return res2[0] # В данном случае получаем фильтрованные данные
            except IndexError:
                return """
Enter the name of the game like this:\nElden Ring, Fallout New Vegas, Rising Storm 2 Vietnam 
                """
        else:
            return print('Sorry')

    async def finally_stand(self, res1, res2):
        pass


async def price_game(oldprice, price, discount, site_url):
    price_list = []
    if oldprice and discount == []:
        future = [asyncio.ensure_future(find(obj=price[-1], to_append=price_list))]
        await asyncio.wait(future)
        return f"Old price: -, Discount: -%, Price: {price_list[0]}\n{site_url}"
    elif price is []:
        return """
This game is not in the store,
It will go on sale soon
Or enter the name of the game like this: 
Elden Ring, Fallout New Vegas, Rising Storm 2 Vietnam
                """
    else:
        futures = [
            asyncio.ensure_future(find(obj=oldprice[-1], to_append=price_list)),
            asyncio.ensure_future(find(obj=price[-1], to_append=price_list)),
            asyncio.ensure_future(find(obj=discount[-1], to_append=price_list))
        ]
        await asyncio.wait(futures)
        return f"Old price: {price_list[0]}, Discount: {price_list[2]}%, Price: {price_list[1]}\n{site_url}"


# def finall(list,site_url):
#     if len(list) == 1:
#         return f"Old price: -, Discount: -%, Price: {list[0]}\n{site_url}"
#     elif list == []:
#         return """
# This game is not in the store,
# It will go on sale soon
# Or enter the name of the game like this:
# Elden Ring, Fallout New Vegas, Rising Storm 2 Vietnam
#                 """
#     else:
#         None
#
#
# async def testws():
#     print('Your WS')
#     url = "wss://zaka-zaka.com/game/rising-storm-2-vietnam"
#     url_1 = 'wss://'
#     async with websockets.connect(url_1) as client:
#         print(await client.recv())

async def links(name, tree):

    list_links = []

    for n in range(1, 20):
        j = tree.xpath(f"//div[@id='search_resultsRows']/a[{n}]")
        advacii = j[-1].attrib
        if name in advacii['href']:
            list_links.append(advacii['href'])
        elif name.capitalize() in advacii['href']:
            list_links.append(advacii['href'])
        elif name.upper() in advacii['href']:
            list_links.append(advacii['href'])

    if not list_links:
        interim_list = []
        j1 = tree.xpath(f"//div[@id='search_resultsRows']/a[1]")
        advac = j1[-1].attrib
        interim_list.append(advac['href'])
        tasks = asyncio.create_task(spliter(list_cheak=interim_list, game_name=None))
        game_name = await asyncio.gather(tasks)
        enter = game_name[0]
        return await links(name=enter, tree=tree)
    # print(list_links)
    return list_links


async def spliter(list_cheak, game_name):
    list_split = []
    n = 0
    game_n = await valid(name=game_name)
    while n < len(list_cheak):
        for i in list_cheak:
            j = i.split('/')
            list_split.extend(j)
            n += 1

    if game_n is not None:

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
            return j


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


async def find(obj, to_append):
    for i in obj:
        to_str = str(i)
        a = to_str.strip('-%')
        if a.isdigit:
            go_int = int(a)
            to_append.append(go_int)
            return go_int


async def validator(text):
    if isinstance(text, str):
        text_for_site = text.lower()
        list_split = text_for_site.split(" ")
        list_to_join = "-".join(list_split)
        list_to_str = list_to_join
        return list_to_str
    else:
        print('Name of game does exists')


async def test(text):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zaka-zaka.com/game/{}'.format(await validator(text))) as response:
            html = await response.text()
            return html


async def main(text):
    gm = Game(text=text)
    res1 = await gm.zaka_find()
    res2 = await gm.steam_find()
    return f'Zaka-Zaka Store:\n{res1}\nSteam Store:\n{res2}'

if __name__ == '__main__':
    txt_input = 'elden ring'
    loop = asyncio.get_event_loop()
    tasks = main(txt_input)
    print(loop.run_until_complete(tasks)) # Elden Ring, Rising Storm 2 Vietnam, Fallout 3, Fallout New Vegas
    loop.close()


"""

html = html.split('<table class="ws-table-all notranslate">')[1]

future =  [asyncio.ensure_future(price_game(oldprice=old_price, price=price_now, discount=discount, site_url=zaka))]
return await asyncio.wait(future) # - В таком случае мы получаем данные корутины, а не ее значения
({<Task finished name='Task-2' coro=<price_game() done, defined at C:/Users/user/AioAsync/test2.py:10> result='Old price: -...me/elden-ring'>}, set())

# req = requests.get(zaka, headers={'User-Agent': FUA})
# code_txt = req.text
# for key, value in req.request.headers.items():
#     print(key+':'+value)

"""