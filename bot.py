import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import menu
from config import token
from model import *

API_TOKEN = token

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Обробка команди "старт".
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Збереження чатайді, прізвища, імені і юзернейму в базу даних
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    print(chat_id, user_id, username, first_name, last_name)
    db = SessionLocal()
    # Перевірка, чи існує користувач з таким чатайді в базі даних
    existing_user = db.query(Users).filter_by(chat_id=chat_id).first()
    if not existing_user:
        print('create user')
        new_user = Users(chat_id=chat_id, user_name=username, user_first_name=first_name, user_last_name=last_name)
        db.add(new_user)
        db.commit()

    welcome_message = 'Привіт!'
    await message.answer(welcome_message, reply_markup=menu.home_menu)




#region CallbackMenu
# Обробник натискання кнопки "Каталог товарів"
@dp.callback_query_handler(lambda query: query.data == 'open_catalog')
async def open_catalog(query: types.CallbackQuery):
    product_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
    # Отримання списку товарів з бази даних
    db = SessionLocal()
    products = db.query(Product).first()

    #Створення кнопок меню
    product_keyboard.row(
        types.InlineKeyboardButton(text='Додати в корзину', callback_data=f'add_basket_{products.id}')
    )
    product_keyboard.row(
        types.InlineKeyboardButton(text='<< Попередній', callback_data=f'prev_{products.id}'),
        types.InlineKeyboardButton(text='Наступний >>', callback_data=f'next_{products.id}')
    )

    chat_id = query.from_user.id
    product_desc = f'*{products.product_name}* \nЦіна: {products.product_price}'
    with open(products.product_img, 'rb') as product_image:
        await bot.send_photo(chat_id, photo=product_image, caption=product_desc, parse_mode='Markdown',
                             reply_markup=product_keyboard)



#endregion


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)