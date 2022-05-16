import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import insta
import qr_decode, info
import keys as nav
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
import aiohttp
import requests

INFO_POST = 'http://127.0.0.1:8000/voice/'
API_TOKEN = ''
CHANNEL_ID = '@testchannelforcoolbot'

# Configure logging for

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

markdown = """
    *bold text*
    _italic text_
    [text](URL"""

class Form(StatesGroup):
    Get_contact = State() #Задаем состояние
    Cash_back = State()
    QR_catch = State()


def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, 'Добро пожаловать!  Этот бот для получения кешбека от суммы накладной.'
                                                 ' Отправьте свой номер боту для регистрации',
                           reply_markup=nav.markup_requests)
    await Form.Get_contact.set()


@dp.message_handler(content_types=['contact'], state=Form.Get_contact)
async def contact(message):
    if message.contact is not None:
        keyboard2 = types.ReplyKeyboardRemove()
        await bot.send_message(message.chat.id, 'Вы успешно отправили свой номер, cпасибо вы зарегистрированы',
                               reply_markup=keyboard2)
        await bot.send_message(message.from_user.id, 'Для получения кешбека нажмите на кнопку',
                               reply_markup=nav.cashBack)
        global phone_number
        phone_number = message.contact.phone_number
        user_id = int(message.contact.user_id)
        # print(phone_number, user_id)
        cash = int(12124)
        # requests.post('http://127.0.0.1:8000/user', data={'tgUserId': user_id, 'phone': phone_number})
        print(phone_number)
    await Form.next()


async def info_post():
    async with aiohttp.ClientSession as session:
        async with session.post(INFO_POST) as response:

            return await response.json()


@dp.callback_query_handler(text='cashbackdone', state=Form.Cash_back)
async def cashbackdone(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        await bot.delete_message(message.from_user.id, message.message.message_id)
        await bot.send_message(message.from_user.id, 'Отправьте фотографию QR кода из накладной')
        await Form.next()
    else:
        await bot.send_message(message.from_user.id, 'Подпишитесь на наш телеграм канал', reply_markup=nav.checkSubMenu)
        # await bot.send_message(message.from_user.id, 'моладец что подписался, теперь подпишись на инсту',
        #                        reply_markup=nav.checkInstMenu)
        # await Form.peremennaya.set()
        # print(message.text)
# @dp.message_handler()
# async def get_nick(message: types.Message):
#     denser = insta.insta(message.text)
#     if denser :
#      markup = types.ReplyKeyboardRemove()
    # else:
        # await bot.send_message(message.from_user.id, 'моладец что подписался, теперь подпишись на инсту',
        #                        reply_markup=nav.checkInstMenu)


@dp.callback_query_handler(text='subchanneldone', state=Form.Cash_back)
async def subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)


@dp.message_handler(content_types=['photo'], state=Form.QR_catch)
async def handle_docs_photo(message: types.Message):
    await message.photo[-1].download('qr/test.jpg')
    payload = qr_decode.decoder()
    print(payload)

    if len(payload) < 15:
        parss = {'inVoiceId': int(payload)}
        # await bot.send_message(message.from_user.id, qr_decode.decoder())
        r = requests.get('http://127.0.0.1:8000/invoice', params=parss)
        if len(r.text) > 10:
            await bot.send_message(message.from_user.id, 'За этот накладной кэшбэк получен, отправь другой накладной', parse_mode="Markdown")
        else:
            url = f'https://express.eastline.uz/api/bot/get-cashback-info/{payload}'
            r = requests.get(url, params=payload)
            user_id = int(message.from_user.id)
            json = r.json()
            requests.post('http://127.0.0.1:8000/user/myapp/', data={'phone': json['sender_phone'],
                                                                    'tgUserId' : user_id,
                                                                    'inVoiceId': payload,
                                                                    'price': json['cost_of_service_with_vat'],
                                                                    'name': json['sender_name'],
                                                                    'cashBack': json['cashback']})
            await bot.send_message(message.from_user.id, f'Кешбек получен успешно. Ваш кешбек:{ str(json["cashback"]) } UZS { str(json["sender_phone"]) } { str(json["cost_of_service_with_vat"]) }, { str(json["sender_name"]) }')
    else:
        await bot.send_message(message.from_user.id, payload, parse_mode="Markdown")

    # print(r.text)
    # print(r.url)
    # await bot.send_message(message.from_user.id, r.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
