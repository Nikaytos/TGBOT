from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.inline import get_meet_keyboard, get_info_keyboard
from tgbot.keyboards.reply import get_start_keyboard


async def user_start(message: Message):
    welcome_text = "Вітання! Я бот. Для отримання інструкцій використовуй команду /help."
    keyboard = get_start_keyboard()
    if message.chat.type == "private":
        await message.reply(welcome_text, reply_markup=keyboard)
    else:
        await message.reply(welcome_text)


async def user_help(message: Message):
    help_text = "Це мій бот. Ось що я вмію:\n" \
                "/help - вивести цю довідку\n" \
                "Meet - посилання на всі уроки\n" \
                "Інфа - інформація про всяке (пошти і т.п.)"
    await message.answer(help_text)


async def user_meet(message: Message):
    keyboard = get_meet_keyboard()
    await message.answer("Оберіть тип занять:", reply_markup=keyboard)


async def user_info(message: Message):
    keyboard = get_info_keyboard()
    await message.answer("Чо нада?", reply_markup=keyboard)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(user_help, commands=["help"], state="*")
    dp.register_message_handler(user_meet, lambda message: message.text.lower() == "meet")
    dp.register_message_handler(user_info, lambda message: message.text.lower() == "інфа")