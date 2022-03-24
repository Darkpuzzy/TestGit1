from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import aiohttp
import websockets
import requests

FUA = UserAgent().chrome


async def price_game(oldprice, price, discount, site_url):
    price_list = []
    if oldprice and discount == []:
        future = [asyncio.ensure_future(find(obj=price[-1], to_append=price_list))]
        await asyncio.wait(future)
        return f"Old price: -, Discount: -%, Price: {price_list[0]}\n{site_url}"
    elif price == []:
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


class Game:

    def __init__(self, text):
        self.text = text

    async def is_valid(self):
        if isinstance(await validator(text=self.text), str):
            try:
                zaka = 'https://zaka-zaka.com/game/{}'.format(await validator(text=self.text))
                code_txt = await test(text=await validator(text=self.text))
                soup = BeautifulSoup(code_txt, 'lxml')
                old_price = soup.find_all('div', class_='old-price')
                price_now = soup.find_all('div', class_='price')
                discount = soup.find_all('div', class_='discount')
                tasks = asyncio.create_task(price_game(oldprice=old_price, price=price_now, discount=discount, site_url=zaka))
                res = await asyncio.gather(tasks)
                return res[0] # В данном случае получаем фильтрованные данные
            except IndexError:
                return """ 
                    Enter the name of the game like this:\n
                    Elden Ring, Fallout New Vegas, Rising Storm 2 Vietnam
                            """
        else:
            return print('Sorry')


async def test(text):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://zaka-zaka.com/game/{}'.format(await validator(text))) as response:
            html = await response.text()
            return html


async def main(text):
    gm = Game(text=text)
    return await gm.is_valid()


if __name__ == '__main__':
    txt_input = input()
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