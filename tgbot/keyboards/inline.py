from aiogram import Dispatcher
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton, InputFile

from tgbot.config import Config


async def user_files_oop(query: CallbackQuery):
    await query.message.delete()
    text = "Файли ООП:"
    keyboard = get_files_oop_keyboard()
    await query.message.answer(text, reply_markup=keyboard)


async def user_files_oop_callback(query: CallbackQuery, config: Config):
    await query.message.delete()
    await query.message.answer_chat_action("upload_document")
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Назад", callback_data="oop_back"))
    name = None
    url_name = None
    input_file = None
    caption = None
    data = query.data
    if data == "lab1":
        name = list(config.dict.url.keys())[0]
        url_name = list(config.dict.url.values())[0]
        caption = "Перша лаба"
        input_file = InputFile.from_url(url_name, filename=name)
    elif data == "lab2":
        name = list(config.dict.url.keys())[1]
        url_name = list(config.dict.url.values())[1]
        input_file = InputFile.from_url(url_name, filename=name)
        caption = "Друга лаба"
    elif data == "lab3":
        name = list(config.dict.url.keys())[2]
        url_name = list(config.dict.url.values())[2]
        input_file = InputFile.from_url(url_name, filename=name)
        caption = "Третя лаба"
    await query.message.answer_document(input_file, caption=caption, reply_markup=keyboard)


async def user_info_pp(query: CallbackQuery, config: Config):
    await query.message.delete()
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Назад", callback_data="info_back"))
    text = "Пошти прєподов:\n"
    for name, email in config.dict.emails.items():
        text += f"{name} — <code>{email}</code>\n"
    await query.message.answer(text, reply_markup=keyboard)


async def user_meet_callback(query: CallbackQuery, config: Config):
    await query.message.delete()
    text = "Оберіть ваше заняття:"
    keyboard = InlineKeyboardMarkup(row_width=1)
    data = query.data
    if data == "lectures":
        for meet_name, meet_link in config.dict.lectures.items():
            keyboard.add(InlineKeyboardButton(meet_name, url=meet_link, disable_web_page_preview=True))
    elif data == "practicums":
        for meet_name, meet_link in config.dict.practicums.items():
            keyboard.add(InlineKeyboardButton(meet_name, url=meet_link, disable_web_page_preview=True))
    elif data == "labs":
        for meet_name, meet_link in config.dict.labs.items():
            keyboard.add(InlineKeyboardButton(meet_name, url=meet_link, disable_web_page_preview=True))
    keyboard.add(InlineKeyboardButton("Назад", callback_data="meet_back"))
    await query.message.answer(text, reply_markup=keyboard)


def get_files_oop_keyboard():
    buttons = [
        InlineKeyboardButton("Lab1", callback_data="lab1"),
        InlineKeyboardButton("Lab2", callback_data="lab2"),
        InlineKeyboardButton("Lab3", callback_data="lab3")
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        keyboard.add(button)
    keyboard.add(InlineKeyboardButton("Назад", callback_data="files_back"))
    return keyboard


def get_info_keyboard():
    buttons = [
        InlineKeyboardButton("Пошти прєподов", callback_data="teachers_emails")
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(buttons[0])
    return keyboard


def get_files_keyboard():
    buttons = [
        InlineKeyboardButton("ООП", callback_data="oop"),
        InlineKeyboardButton("ЛМВ", callback_data="lmv"),
        InlineKeyboardButton("ВМ", callback_data="vm")
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        keyboard.add(button)
    return keyboard


def get_meet_keyboard():
    buttons = [
        InlineKeyboardButton("Лекції", callback_data="lectures"),
        InlineKeyboardButton("Практичні", callback_data="practicums"),
        InlineKeyboardButton("Лаби", callback_data="labs"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        keyboard.add(button)

    return keyboard


async def user_back(query: CallbackQuery):
    await query.message.delete()
    keyboard = None
    text = None
    data = query.data
    if data == "meet_back":
        keyboard = get_meet_keyboard()
        text = "Оберіть тип занять:"
    elif data == "info_back":
        keyboard = get_info_keyboard()
        text = "Чо нада?"
    elif data == "files_back":
        keyboard = get_files_keyboard()
        text = "Дисципліни:"
    elif data == "oop_back":
        keyboard = get_files_oop_keyboard()
        text = "Файли ООП:"
    await query.message.answer(text, reply_markup=keyboard)

back = ["meet_back", "info_back", "files_back", "oop_back"]


def register_inline(dp: Dispatcher):
    dp.register_callback_query_handler(user_meet_callback, lambda query: query.data in ["lectures", "practicums", "labs"])
    dp.register_callback_query_handler(user_files_oop_callback, lambda query: query.data in ["lab1", "lab2", "lab3"])
    dp.register_callback_query_handler(user_info_pp, lambda query: query.data == "teachers_emails")
    dp.register_callback_query_handler(user_files_oop, lambda query: query.data == "oop")
    dp.register_callback_query_handler(user_back, lambda query: query.data in back)
