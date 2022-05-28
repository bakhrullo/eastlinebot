import aiohttp


async def user_chat_id(chat_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url='http://127.0.0.1:8000/tgid', params={'tgUserId': chat_id}) as response:
            return await response.json()


async def contact_create(chat_id, number):
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://127.0.0.1:8000/user/myapp/', data={'tgUserId': chat_id, 'phone': number}) \
                as response:
            return await response.json()


async def get_balance(chat_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'https://express.eastline.uz/api/bot/get-cashback-account/{chat_id}') as response:
            return await response.json()


async def get_history(chat_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'https://express.eastline.uz/api/bot/get-cashback-list/{chat_id}') as response:
            return await response.json()


async def check_invoice(invoice_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url='http://127.0.0.1:8000/invoice', params=invoice_id) as response:
            return await response.json()


async def get_cashback(order_id, chat_id, name, phone):
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://express.eastline.uz/api/bot/get-cashback', data={'order_id': order_id,
                                                                                              'telegram_chat_id':
                                                                                                  chat_id,
                                                                                              'name': name,
                                                                                              'phone': phone}) \
                as response:
            return await response.json()


async def invoice_create(chat_id, number):
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://127.0.0.1:8000/user/coolapp/', data={'UserId': chat_id, 'invoiceId': number}) \
                as response:
            return await response.json()
