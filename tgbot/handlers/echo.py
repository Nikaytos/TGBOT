from aiogram import Dispatcher
from aiogram.types import Message


async def user_message(message: Message):
    welcome_text = "Вітання! Я бот. Для отримання інструкцій використовуй команду /help."
    await message.answer(welcome_text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(user_message)
