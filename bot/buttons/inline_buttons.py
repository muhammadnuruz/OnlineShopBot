import json
import random

import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons.text import uz_language, ru_language, back_main_menu_ru, back_main_menu


async def language_buttons():
    design = [
        [InlineKeyboardButton(text=uz_language, callback_data='language_uz'),
         InlineKeyboardButton(text=ru_language, callback_data='language_ru')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def category_button(lang: str):
    categories = json.loads(requests.get(url="http://127.0.0.1:8000/api/categories").content)
    design = []
    for category in categories['results']:
        design.append([InlineKeyboardButton(text=category['name'], callback_data=category['id'])])
    if lang == 'uz':
        design.append([InlineKeyboardButton(text=back_main_menu, callback_data=back_main_menu)])
    else:
        design.append([InlineKeyboardButton(text=back_main_menu_ru, callback_data=back_main_menu_ru)])
    return InlineKeyboardMarkup(inline_keyboard=design)


async def put_in_basket_buttons(count: str = '1'):
    design = [
        [
            InlineKeyboardButton(text="➖", callback_data="delete_in_basket"),
            InlineKeyboardButton(text=count, callback_data="none"),
            InlineKeyboardButton(text="➕", callback_data="add_in_basket")
        ],
        [InlineKeyboardButton(text="📥", callback_data='put_in_basket')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)
