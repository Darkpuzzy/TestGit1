import asyncio
import requests
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
# from token import Token_bot
import time
import json
import datetime
from fake_useragent import UserAgent

# FUA = UserAgent().chrome
# headers = {'User-Agent': FUA}


def test():
    now = datetime.datetime.now()
    now_str = now.strftime('%H:%M:%S')
    return now_str


async def gt1():
    sec = 3
    print('I will started GT1 {} seconds : {}'.format(test(), sec))
    await asyncio.sleep(sec)
    print('Connections {} seconds : {}'.format(test(), sec))


async def gt2():
    sec = 5
    print(f'I will started GT2 {test()}/ second : {sec}')
    await asyncio.sleep(sec)
    print(f'Connections {test()} / second {sec}')


async def gt3():
    sec = 1
    print(f'GT3 Fun {test()}/ second : {sec}')
    await asyncio.sleep(1)
    print(f'Done GT3 {test()} / second : {sec}')

URL = 'https://api.ipify.org/'


def ip_cheaker(URL):
    cheak_ip = requests.get(URL+'?format=json')
    # for key, value in cheak_ip.request.headers.items():
    #     j = print(key+':'+value)
    return cheak_ip


async def jsoner(to_json):
    print('Accepted files to json format')
    await asyncio.sleep(5)
    json_finish = to_json.json()
    return print(f'Accepted json.files : {json_finish}')


async def asynchrone():
    await asyncio.sleep(2)
    print('Get ip cheaker')
    to_json = ip_cheaker(URL=URL)
    print(f'Connection look {to_json}/ time start to connect : {test()}')
    await asyncio.sleep(3)
    print('Go to TASK')
    tasks = [asyncio.ensure_future(jsoner(to_json=to_json))]
    await asyncio.wait(tasks)
    print(f'Ended connection {test()}')




def main():
    ioloop = asyncio.get_event_loop()
    task = [
        ioloop.create_task(asynchrone())
    ]
    wait_tasks = asyncio.wait(task)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
    return 'Finished main №1'




def main2():
    time.sleep(2)
    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(gt1()),
        ioloop.create_task(gt2()),
        ioloop.create_task(gt3()),
    ]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
    return 'Finished main №2'

print(main())