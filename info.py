import aiohttp
INFO_POST = 'http://127.0.0.1:8000/voice/'


async def info_post():
    async with aiohttp.ClientSession as session:
        async with session.post(INFO_POST) as response:
            return await response.json()
