import configparser
from aiogram import Dispatcher
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton

config_info = configparser.ConfigParser()
config_info.optionxform = lambda option: option
config_info.read('info.ini', encoding='utf-8')

emails = dict(config_info.items('emails'))
lectures = dict(config_info.items('lec'))
practicums = dict(config_info.items('prac'))
labs = dict(config_info.items('lab'))


def get_info_keyboard():
    buttons = [
        InlineKeyboardButton("Пошти прєподов", callback_data="teachers_emails")
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(buttons[0])
    return keyboard


def get_meet_keyboard():
    buttons = [
        InlineKeyboardButton("Лекції", callback_data="lectures"),
        InlineKeyboardButton("Практичні", callback_data="practicums"),
        InlineKeyboardButton("Лаби", callback_data="labs"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(buttons[0], buttons[1], buttons[2])
    return keyboard


async def user_info_pp(query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Назад", callback_data="info_back"))
    pp = "Пошти прєподов:\n"
    for name, email in emails.items():
        pp += f"{name} — <code>{email}</code>\n"
    await query.message.edit_text(pp)
    await query.message.edit_reply_markup(keyboard)


async def user_meet_callback(query: CallbackQuery):

    keyboard = InlineKeyboardMarkup(row_width=1)

    data = query.data

    if data == "lectures":
        for meet_name, meet_link in lectures.items():
            keyboard.add(InlineKeyboardButton(meet_name, url=meet_link, disable_web_page_preview=True))
    elif data == "practicums":
        for meet_name, meet_link in practicums.items():
            keyboard.add(InlineKeyboardButton(meet_name, url=meet_link, disable_web_page_preview=True))
    elif data == "labs":
        for meet_name, meet_link in labs.items():
            keyboard.add(InlineKeyboardButton(meet_name, url=meet_link, disable_web_page_preview=True))
    keyboard.add(InlineKeyboardButton("Назад", callback_data="meet_back"))
    await query.message.edit_text("Оберіть ваше заняття:")
    await query.message.edit_reply_markup(keyboard)


async def user_back(query: CallbackQuery):
    keyboard = None
    text = None
    data = query.data
    if data == "meet_back":
        keyboard = get_meet_keyboard()
        text = "Оберіть тип занять:"
    elif data == "info_back":
        keyboard = get_info_keyboard()
        text = "Чо нада?"
    await query.message.edit_text(text)
    await query.message.edit_reply_markup(keyboard)


def register_inline(dp: Dispatcher):
    dp.register_callback_query_handler(user_meet_callback, lambda query: query.data in ["lectures", "practicums", "labs"])
    dp.register_callback_query_handler(user_info_pp, lambda query: query.data == "teachers_emails")
    dp.register_callback_query_handler(user_back, lambda query: query.data in ["meet_back", "info_back"])
