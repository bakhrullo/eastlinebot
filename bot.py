import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import insta
import qr_decode
import keys as nav
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '5342616434:AAH6urtpWE53qFi657huUlesapo62o2aTvQ'
CHANNEL_ID = '@testchannelforcoolbot'

# Configure logging

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


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
        phone_number = str(message.contact.phone_number)
        user_id = str(message.contact.user_id)
        print(phone_number, user_id)
    await Form.next()


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
    await bot.send_message(message.from_user.id, qr_decode.decoder())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
