import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# import insta
import keys
import qr_decode
import keys as nav
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
import asyncRequests
from aiogram.dispatcher import FSMContext

API_TOKEN = '5342616434:AAH6urtpWE53qFi657huUlesapo62o2aTvQ'
CHANNEL_ID = '@Eastline_express_uzb'
# Configure logging for

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    Get_contact = State()
    Menu = State()
    # Cash_back = State()
    # Balance_check = State()
    # History_check = State()
    QR_catch = State()


def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message):
    pk = message.chat.id
    user_num = await asyncRequests.user_chat_id(pk)
    print(len(user_num))
    if len(user_num) > 0:
        await bot.send_message(message.from_user.id, '🤔 С чего начнём?',
                               reply_markup=nav.cashBack)
        await Form.Menu.set()
    else:
        await bot.send_message(message.from_user.id, 'Добро пожаловать в Eastline Express Bot! 🤗 '
                                                     'Этот бот создан для получения кэшбэка от суммы накладной.'
                                                     'Отправьте свой контакт боту для регистрации 📲',
                               reply_markup=nav.markup_requests)
        await Form.Get_contact.set()


@dp.message_handler(content_types=['contact'], state=Form.Get_contact)
async def contact(message):
    if message.contact is not None:
        keyboard2 = types.ReplyKeyboardRemove()
        pk = message.chat.id
        if len(message.contact.phone_number) == 12:
            phone_number = '+' + message.contact.phone_number
            print(len(phone_number))
            await asyncRequests.contact_create(chat_id=pk, number=phone_number)
            await bot.send_message(message.chat.id, 'Вы успешно отправили свой контакт! Спасибо за регистрацию 🤩',
                                   reply_markup=keyboard2)
            await bot.send_message(message.from_user.id, '🤔 С чего начнём?',
                                   reply_markup=nav.cashBack)

            await Form.next()

    # if len(resp) < 4:
    #     await bot.send_message(message.from_user.id, 'вы ещё не получали кешбек', reply_markup=keys.balanceBack)
    # else:
    #     await bot.send_message(message.from_user.id, f"{resp['name']}"
    #                                                  f" {resp['phone']}"
    #                                                  f" {resp['cashback']}", reply_markup=keys.balanceBack)


# @dp.message_handler()
# async def get_nick(message: types.Message):
#     denser = insta.insta(message.text)
#     if denser :
#      markup = types.ReplyKeyboardRemove()
# else:
# await bot.send_message(message.from_user.id, 'моладец что подписался, теперь подпишись на инсту',
#                        reply_markup=nav.checkInstMenu)


@dp.message_handler(content_types=['photo'], state=Form.QR_catch)
async def handle_docs_photo(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    await message.photo[-1].download(f'test/{chat_id}.jpg')
    payload = qr_decode.decoder(chat_id)
    print(payload)
    name = message.from_user.first_name
    if len(payload) < 15:
        parss = {'inVoiceId': int(payload)}
        r = await asyncRequests.check_invoice(invoice_id=parss)
        print(len(r))

        if len(r) == 1:
            await bot.send_message(message.from_user.id, '😔 Кэшбэк за эту накладную уже получен.'
                                                         ' Отправьте другой QR-код',
                                   reply_markup=keys.back)
        else:
            pk = message.chat.id
            user_num = await asyncRequests.user_chat_id(pk)
            us = user_num[0]['phone']

            resp = await asyncRequests.get_cashback(order_id=payload, chat_id=pk, name=name, phone=us)
            ress = await asyncRequests.invoice_create(chat_id=resp['telegram_chat_id'], number=resp['order_id'])
            print(resp)
            await bot.send_message(message.from_user.id, f'🥳 Поздравляем! Кэшбэк получен успешно!.\n'
                                                         f'📦 Номер заказа: {resp["order_id"]} \n'
                                                         f'👤 Имя заказчика: {resp["sender_name"]} \n'
                                                         f'📲 Номер заказчик: {resp["sender_phone"]} \n'
                                                         f'💵 Стоимость заказа: {resp["cost_of_service_with_vat"]} UZS\n'
                                                         f'💸 Начисленная сумма: {resp["cashback"]} UZS \n'
                                                         f'🤩 Процент кэшбэка: {resp["percent"]}',
                                   reply_markup=keys.back)


            #await bot.send_message(message.from_user.id,
            #                        'За этот накладной кэшбэк получен, отправь другой накладной',
            #                        parse_mode="Markdown")
    else:
        await bot.send_message(message.from_user.id, payload, parse_mode="Markdown")

    # print(r.text)
    # print(r.url)
    # await bot.send_message(message.from_user.id, r.text)


#                                                 OBRABOTKA KNOPOK


@dp.message_handler(lambda message: message.text == "💸 Получить кэшбэк", state=Form.Menu)
async def cashbackdone(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        # await bot.delete_message(message.from_user.id, message.message.message_id)
        await bot.send_message(message.from_user.id, 'Отправьте фото QR-кода вашей накладной 📷',
                               reply_markup=keys.back)
        await Form.QR_catch.set()
    else:
        await bot.send_message(message.from_user.id, '😉 Для начала подпишитесь на наш Telegram-канал',
                               reply_markup=nav.checkSubMenu)


@dp.message_handler(lambda message: message.text == "👤 Профиль", state=Form.Menu)
async def balancedone(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        pk = message.from_user.id
        resp = await asyncRequests.get_balance(pk)
        if len(resp) < 4:
            await bot.send_message(message.from_user.id, '🥲 Вы ещё не получили кэшбэк.', reply_markup=keys.back)
        else:
            await bot.send_message(message.from_user.id, f"👤 Имя: {resp['name']} \n"
                                                         f"📲 Номер: {resp['phone']} \n"
                                                         f"💰 Баланс: {resp['cashback']} UZS", reply_markup=keys.back)
    else:
        await bot.send_message(message.from_user.id, '😉 Для начала подпишитесь на наш Telegram-канал', reply_markup=nav.checkSubMenu)


@dp.message_handler(lambda message: message.text == "📄 История транзакций", state=Form.Menu)
async def historydone(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        pk = message.from_user.id
        try:
            resp = await asyncRequests.get_history(pk)
            data = resp['data']
            ans = ''
            for i in data:
                word = i['created_at']
                remove_last = word[:-17]
                answer = f"📦Номер заказа: {i['order_id']},  \n" \
                         f"💸Кэшбэк: {i['cashback']} UZS,  \n" \
                         f"🕑Время: {remove_last}"
                ans = str(answer) + '.\n\n' + ans
                # await bot.send_message(message.from_user.id, answer)
            await bot.send_message(message.from_user.id, text=ans, reply_markup=keys.back)
            print(ans)
        except:
            await bot.send_message(message.from_user.id, '🥲 Вы ещё не получили кэшбэк.', reply_markup=keys.back)
    else:
        await bot.send_message(message.from_user.id, '😉 Для начала подпишитесь на наш Telegram-канал', reply_markup=nav.checkSubMenu)


@dp.message_handler(lambda message: message.text == '🔙 Назад', state='*')
async def back_done(message: types.Message):
    await bot.send_message(message.from_user.id, '🤔 С чего начнём?', reply_markup=keys.cashBack)
    await Form.Menu.set()


@dp.callback_query_handler(text='subchanneldone', state='*')
async def subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
