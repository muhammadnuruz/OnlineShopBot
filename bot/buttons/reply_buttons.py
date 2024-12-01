import json

import requests
from aiogram.types import ReplyKeyboardMarkup

from bot.buttons.text import back_main_menu, adverts, none_advert, forward_advert, choice_language, choice_language_ru, \
    contact, ask_question, ask_question_ru, contact_ru, back_main_menu_ru, contact_en, \
    ask_question_en, choice_language_en, back_main_menu_en, change_phone, change_phone_en, change_phone_ru, ordering, \
    ordering_en, ordering_ru


async def main_menu_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [ordering],
            [ask_question, contact],
            [choice_language, change_phone]
        ]
    elif tg_user['language'] == "en":
        design = [
            [ordering_en],
            [ask_question_en, contact_en],
            [choice_language_en, change_phone_en]
        ]
    else:
        design = [
            [ordering_ru],
            [ask_question_ru, contact_ru],
            [choice_language_ru, change_phone_ru]
        ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu_button(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [[back_main_menu]]
    elif tg_user['language'] == 'en':
        design = [[back_main_menu_en]]
    else:
        design = [[back_main_menu_ru]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_menu_buttons():
    design = [
        [adverts],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def advert_menu_buttons():
    design = [
        [none_advert, forward_advert],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
