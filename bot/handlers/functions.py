import json

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_buttons import back_main_menu_button, main_menu_buttons
from bot.buttons.text import contact, contact_ru, ask_question_ru, ask_question, contact_en, ask_question_en
from bot.dispatcher import dp, bot
from main import admins

locations = {
    "Yunusobod filliali": (41.3653103, 69.291063),
    "Chirchiq filliali": (41.436581, 69.545277),
    "Best Medical filliali": (41.33356, 69.36789),
    "Mirzo Ulug'bek fillial": (41.347393, 69.339413),
    "Sifat Medical filliali": (41.3202702, 69.3501809),
    "Farhod Lor filliali": (41.382077, 69.353685),
}

phone_numbers = {
    "Yunusobod filliali": "+998912787878",
    "Chirchiq filliali": "+998958083303",
    "Best Medical filliali": "+998912787878",
    "Mirzo Ulug'bek fillial": "+998912787878",
    "Sifat Medical filliali": "+998909942704",
    "Farhod Lor filliali": "+998335833900",
}


@dp.message_handler(Text(equals=[contact, contact_ru, contact_en]))
async def contact_function(msg: types.Message):
    if msg.text == contact:
        await msg.answer(text="📞 Yagona telefon raqami: +998912787878")
    elif msg.text == contact_en:
        await msg.answer(text="📞 Single phone number: +998912787878")
    else:
        await msg.answer(text="📞 Единственный номер телефона: +998912787878")


@dp.message_handler(Text(equals=[ask_question, ask_question_ru, ask_question_en]))
async def ask_question_function(msg: types.Message, state: FSMContext):
    await state.set_state('ask_question')

    if msg.text == ask_question:
        await msg.answer(
            text="✍️ Talab va istaklaringizni yozib qoldiring. Biz yechim topishga harakat qilamiz:",
            reply_markup=await back_main_menu_button(msg.from_user.id)
        )
    elif msg.text == ask_question_en:
        await msg.answer(
            text="✍️ Write down your requests and suggestions. We will try to find a solution:",
            reply_markup=await back_main_menu_button(msg.from_user.id)
        )
    else:
        await msg.answer(
            text="✍️ Запишите ваши требования и пожелания. Мы постараемся найти решение:",
            reply_markup=await back_main_menu_button(msg.from_user.id)
        )


@dp.message_handler(state='ask_question')
async def receive_question_and_notify_admins(msg: types.Message, state: FSMContext):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content
    )
    user_language = tg_user.get('language', 'uz')
    user_phone = tg_user.get('phone_number', 'Noma’lum')

    user_info = (
        f"👤 **Foydalanuvchi ma'lumotlari:**\n"
        f"ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>\n"
        f"Username: @{msg.from_user.username}\n"
        f"Ism-Familiya: {msg.from_user.full_name}\n"
        f"📞 Telefon: {user_phone}\n"
        f"✉️ Xabar: \n\n{msg.text}"
    )

    for admin in admins:
        await bot.send_message(chat_id=admin, text=user_info, parse_mode='HTML')

    if user_language == 'uz':
        await msg.answer(
            text="✅ Xabaringiz adminlarga jo'natildi! Rahmat.",
            reply_markup=await main_menu_buttons(msg.from_user.id)
        )
    elif user_language == 'en':
        await msg.answer(
            text="✅ Your message has been sent to the admins! Thank you.",
            reply_markup=await main_menu_buttons(msg.from_user.id)
        )
    else:
        await msg.answer(
            text="✅ Ваше сообщение отправлено администраторам! Спасибо.",
            reply_markup=await main_menu_buttons(msg.from_user.id)
        )

    await state.finish()

# @dp.message_handler(Text(equals=[social_networks, social_networks_ru]))
# async def sociable_networks_function(msg: types.Message):
#     if msg.text == social_networks:
#         await msg.answer(text="""
# Bizning ijtimoiy tarmoqlarga obuna bo'ling 👇:
#
# Instagram: https://www.instagram.com/arzon.lab/
# YouTube: https://youtube.com/@arzonlab
# Facebook: https://www.facebook.com/profile.php?id=61558339262051
# Telegram: https://t.me/arzonlab""")
#     else:
#         await msg.answer(text="""
# Подписывайтесь на наши социальные сети 👇:
#
# Instagram: https://www.instagram.com/arzon.lab/
# YouTube: https://youtube.com/@arzonlab
# Facebook: https://www.facebook.com/profile.php?id=61558339262051
# Telegram: https://t.me/arzonlab""")
#
#
# @dp.message_handler(Text(equals=[location, location_ru]))
# async def contact_function(msg: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#
#     for location_name in locations.keys():
#         keyboard.add(types.KeyboardButton(location_name))
#     if msg.text == location:
#         keyboard.add(back_main_menu)
#         await msg.answer("Iltimos, lokatsiyangizni tanlang:", reply_markup=keyboard)
#     else:
#         keyboard.add(back_main_menu_ru)
#         await msg.answer("Пожалуйста, выберите вашу локацию:", reply_markup=keyboard)


# @dp.message_handler(lambda message: message.text in locations)
# async def location_handler(msg: types.Message):
#     latitude, longitude = locations[msg.text]
#     phone_number = phone_numbers[msg.text]
#
#     if msg.text in locations:  # Ensure the location is valid
#         await msg.answer(text=f"Tanlangan lokatsiya: {msg.text}\nAloqa uchun: {phone_number}" if msg.text == location
#         else f"Выбранная локация: {msg.text}\nКонтактный номер: {phone_number}")
#         await msg.answer_location(latitude=latitude, longitude=longitude)


# @dp.message_handler(Text(equals=[search_analyses, search_analyses_ru]))
# async def start_analysis_search(msg: types.Message, state: FSMContext):
#     await state.set_state('search_type')
#     if msg.text == search_analyses:
#         await msg.answer(text="Iltimos, analiz nomini kiriting:",
#                          reply_markup=await back_main_menu_button(msg.from_user.id))
#     else:
#         await msg.answer(text="Пожалуйста, введите название анализа:",
#                          reply_markup=await back_main_menu_button(msg.from_user.id))
#
#
# @dp.message_handler(state='search_type')
# async def process_analysis_name(msg: types.Message, state: FSMContext):
#     tg_user = json.loads(
#         requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
#     response = requests.get(f"http://127.0.0.1:8000/api/types/search/{msg.text}/")
#     if response.status_code == 200:
#         analysis_data = response.json()
#         if analysis_data:
#             for analyse in analysis_data.get('results'):
#                 if tg_user['language'] == 'uz':
#                     result = (
#                         f"🔎 Natija:\n\n"
#                         f"🔡 Bo'lim: {analyse.get('category', 'Nomalum')}\n"
#                         f"📝 Nomi: {analyse.get('name', 'Nomalum')}\n"
#                         f"💵 Narxi: {analyse.get('price', 'Nomalum')} so'm\n"
#                         f"ℹ️ Ma'lumot: {analyse.get('info', 'Malumot mavjud emas')}\n"
#                         f"🕒 Tayyor bo'lish vaqti: {analyse.get('to_be_ready', 'Nomalum')} kun"
#                     )
#                 else:
#                     result = (
#                         f"🔎 Результат:\n\n"
#                         f"🔡 Категория: {analyse.get('category', 'Неизвестно')}\n"
#                         f"📝 Название: {analyse.get('ru_name', 'Неизвестно')}\n"
#                         f"💵 Цена: {analyse.get('price', 'Неизвестно')} сум\n"
#                         f"ℹ️ Информация: {analyse.get('ru_info', 'Информация отсутствует')}\n"
#                         f"🕒 Время готовности: {analyse.get('to_be_ready', 'Неизвестно')} день"
#                     )
#
#                 await msg.answer(result)
#         else:
#             await msg.answer(
#                 "❌ Bu nomga mos analiz topilmadi." if tg_user[
#                                                           'language'] == 'uz' else "❌ Анализ с таким названием не найден.")
#     else:
#         await msg.answer(
#             "❌ Bu nomga mos analiz topilmadi." if tg_user[
#                                                       'language'] == 'uz' else "❌ Анализ с таким названием не найден.")
#
#
# @dp.message_handler(Text(equals=[get_analyses_result, get_analyses_result_ru]))
# async def search_analysis_handler(msg: types.Message, state: FSMContext):
#     if msg.text == get_analyses_result:
#         await msg.answer("Iltimos, analizning ID raqamini kiriting:",
#                          reply_markup=await back_main_menu_button(msg.from_user.id))
#     else:
#         await msg.answer("Пожалуйста, введите идентификационный номер анализа:",
#                          reply_markup=await back_main_menu_button(msg.from_user.id))
#     await state.set_state('waiting_for_analysis_id')
#
#
# @dp.message_handler(state='waiting_for_analysis_id')
# async def process_analysis_id(msg: types.Message, state: FSMContext):
#     analysis_id = msg.text
#     tg_user = json.loads(
#         requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
#
#     if not analysis_id.isdigit():
#         if tg_user['language'] == 'uz':
#             await msg.answer("❌ Iltimos, to'g'ri ID kiriting.")
#         else:
#             await msg.answer("❌ Пожалуйста, введите действительный идентификатор.")
#         return
#
#     response = requests.get(f"http://127.0.0.1:8000/api/analyses/{analysis_id}/")
#
#     if response.status_code == 200:
#         analysis_data = response.json()
#
#         temp_file_path = f"/tmp/{os.path.basename(analysis_data.get('file'))}"
#
#         async with aiohttp.ClientSession() as session:
#             async with session.get(analysis_data.get('file')) as resp:
#                 if resp.status == 200:
#                     with open(temp_file_path, 'wb') as f:
#                         f.write(await resp.read())
#
#         await msg.answer_document(document=types.InputFile(temp_file_path),
#                                   reply_markup=await main_menu_buttons(msg.from_user.id))
#
#         os.remove(temp_file_path)
#
#     else:
#         if tg_user['language'] == 'uz':
#             await msg.answer("❌ Bu ID ga mos analiz topilmadi.", reply_markup=await main_menu_buttons(msg.from_user.id))
#         else:
#             await msg.answer("❌ Анализ по этому идентификатору не найден.",
#                              reply_markup=await main_menu_buttons(msg.from_user.id))
#
#     await state.finish()
