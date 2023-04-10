from aiogram import Dispatcher
from aiogram.types import Message
import re


async def user_natu(message: Message):
    text = "натурал тут тільки Андрій"
    await message.reply(text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(user_natu, regexp=re.compile(r"(?i)\bнатурал\b"))
