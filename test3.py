import aiohttp
import asyncio
import websockets


async def main1():

    async with aiohttp.ClientSession() as session:
        async with session.get('https://zaka-zaka.com/game/rising-storm-2-vietnam') as response:
            html = await response.text()

loop = asyncio.get_event_loop()
loop.run_until_complete(main1())


async def main2():

    uri = f"wss://stream.binance.com:9443/stream?streams=btcusd@miniTicker"
    async with websockets.connect(uri) as client:
        while True:
            res = await client.recv()
            print(res)

loop1 = asyncio.get_event_loop()
loop1.run_until_complete(main2())