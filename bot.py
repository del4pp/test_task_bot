import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)