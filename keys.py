from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btnUrlChannel = InlineKeyboardButton(text='подписаться нахооой', url='https://t.me/testchannelforcoolbot')
btnDoneSub = InlineKeyboardButton(text='подписался нахоооой', callback_data='subchanneldone')
btnUrlInsta = InlineKeyboardButton(text='тепрь подписаться на инсту нахооой',
                                   url='https://www.instagram.com/fatkhullaev_b/')
btnCashBack = InlineKeyboardButton(text='получить кешбек', callback_data='cashbackdone',)

cashBack = InlineKeyboardMarkup(row_with=1)
checkSubMenu = InlineKeyboardMarkup(row_width=1)
checkInstMenu = InlineKeyboardMarkup(row_with=1)

checkSubMenu.insert(btnUrlChannel)
checkSubMenu.insert(btnDoneSub)
checkInstMenu.insert(btnUrlInsta)
cashBack.insert(btnCashBack)

markup_requests = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свой контакт',
                                                                               request_contact=True))
