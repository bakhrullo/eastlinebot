from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btnUrlChannel = InlineKeyboardButton(text='Подписаться', url='https://t.me/testchannelforcoolbot')
btnDoneSub = InlineKeyboardButton(text='Подписался', callback_data='subchanneldone')
btnUrlInsta = InlineKeyboardButton(text='Тепрь подписаться на инсту нахооой',
                                   url='https://www.instagram.com/fatkhullaev_b/')
btnCashBack = InlineKeyboardButton(text='Получить кешбек', callback_data='cashbackdone',)
btnBalance = InlineKeyboardButton(text='Профил', callback_data='balancedone',)
btnHistory = InlineKeyboardButton(text='История', callback_data='historydone',)
# btnBackBalance = InlineKeyboardButton(text='назад', callback_data='backdonebalance',)
# btnBackHistory = InlineKeyboardButton(text='назад', callback_data='backdonehistory',)
# btnBackCashback = InlineKeyboardButton(text='назад', callback_data='backdonecashback',)
btnBack = InlineKeyboardButton(text='Назад', callback_data='back',)

back = InlineKeyboardMarkup(row_width=1)
cashBack = InlineKeyboardMarkup(row_with=1)
checkSubMenu = InlineKeyboardMarkup(row_width=1)
checkInstMenu = InlineKeyboardMarkup(row_with=1)

checkSubMenu.insert(btnUrlChannel)
checkSubMenu.insert(btnDoneSub)
checkInstMenu.insert(btnUrlInsta)
cashBack.add(btnCashBack)
cashBack.add(btnBalance)
cashBack.add(btnHistory)
back.insert(btnBack)

markup_requests = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свой контакт',
                                                                               request_contact=True))
