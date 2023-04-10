from aiogram import Dispatcher
from aiogram.types import Message


async def admin(message: Message):
    admin_text = "Адмін в чатє, ку!"
    await message.reply(admin_text)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin, lambda message: message.text == 'admin', is_admin=True)
