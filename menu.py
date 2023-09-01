from aiogram import types

#головне меню
home_menu = types.InlineKeyboardMarkup()
home_menu.row(types.InlineKeyboardButton(text='Каталог товарів', callback_data='open_catalog'))