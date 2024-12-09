import json

import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.text import back_main_menu, adverts, none_advert, forward_advert, choice_language, choice_language_ru, \
    contact, ask_question, ask_question_ru, contact_ru, back_main_menu_ru, change_phone, change_phone_ru, ordering, \
    ordering_ru, send_location, send_location_ru, basket, basket_ru, to_back, to_back_ru


async def main_menu_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [ordering],
            [ask_question, contact],
            [choice_language, change_phone]
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


async def location_buttons(msg: str):
    if msg == ordering:
        design = [[(KeyboardButton(send_location, request_location=True))], [back_main_menu]]
    else:
        design = [[(KeyboardButton(send_location_ru, request_location=True))], [back_main_menu_ru]]
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=design)


async def shop_menu_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    categories = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/categories/").content)['results']
    if tg_user['language'] == 'uz':
        design = [
            [back_main_menu, basket]
        ]
        for i in range(0, len(categories), 2):
            try:
                design.append([categories[i]['name'], categories[i + 1]['name']])
            except IndexError:
                design.append([categories[i]['name']])
    else:
        design = [
            [back_main_menu_ru, basket_ru]
        ]
        for i in range(0, len(categories), 2):
            try:
                design.append([categories[i]['ru_name'], categories[i + 1]['ru_name']])
            except IndexError:
                design.append([categories[i]['ru_name']])
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=design)


async def category_menu_buttons(chat_id: int, txt: str):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    foods = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/?category={txt}").content)['results']
    if tg_user['language'] == 'uz':
        design = [
            [to_back, basket]
        ]
        for i in range(0, len(foods), 2):
            try:
                design.append([foods[i]['name'], foods[i + 1]['name']])
            except IndexError:
                design.append([foods[i]['name']])
    else:
        design = [
            [to_back_ru, basket_ru]
        ]
        for i in range(0, len(foods), 2):
            try:
                design.append([foods[i]['ru_name'], foods[i + 1]['ru_name']])
            except IndexError:
                design.append([foods[i]['ru_name']])
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=design)


async def put_in_basket_reply_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [to_back, basket]
        ]
    else:
        design = [
            [to_back_ru, basket_ru]
        ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def to_back_button(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [to_back]
        ]
    else:
        design = [
            [to_back_ru]
        ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
