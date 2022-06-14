from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btnUrlChannel = InlineKeyboardButton(text='Сейчас подпишусь 👌', url='https://t.me/Eastline_express_uzb')
btnDoneSub = InlineKeyboardButton(text='Уже подписан 😏', callback_data='subchanneldone')
btnUrlInsta = InlineKeyboardButton(text='Тепрь подписаться на инсту',
                                   url='https://www.instagram.com/fatkhullaev_b/')
btnCashBack = KeyboardButton(text='💸 Получить кэшбэк')
btnBalance = KeyboardButton(text='👤 Профиль')
btnHistory = KeyboardButton(text='📄 История транзакций')
# btnBackBalance = InlineKeyboardButton(text='назад', callback_data='backdonebalance',)
# btnBackHistory = InlineKeyboardButton(text='назад', callback_data='backdonehistory',)
# btnBackCashback = InlineKeyboardButton(text='назад', callback_data='backdonecashback',)
btnBack = KeyboardButton(text='🔙 Назад', callback_data='back',)

back = ReplyKeyboardMarkup(resize_keyboard=True)
cashBack = ReplyKeyboardMarkup(resize_keyboard=True)
checkSubMenu = InlineKeyboardMarkup(row_width=1)
checkInstMenu = InlineKeyboardMarkup(row_with=1)

checkSubMenu.insert(btnUrlChannel)
checkSubMenu.insert(btnDoneSub)
checkInstMenu.insert(btnUrlInsta)
cashBack.insert(btnCashBack)
cashBack.insert(btnBalance)
cashBack.insert(btnHistory)
back.add(btnBack)

markup_requests = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свой контакт',
                                                                               request_contact=True))
