from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start_keyboard():
    buttons = [
        KeyboardButton("Файлікі"),
        KeyboardButton("Meet"),
        KeyboardButton("Інфа"),
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(buttons[0]).row(buttons[1], buttons[2])
    return keyboard
