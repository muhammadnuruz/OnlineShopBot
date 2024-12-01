import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.inline_buttons import language_buttons
from bot.buttons.reply_buttons import main_menu_buttons, back_main_menu_button
from bot.buttons.text import back_main_menu, choice_language, choice_language_ru, back_main_menu_ru, choice_language_en, \
    change_phone, change_phone_ru, change_phone_en, back_main_menu_en
from bot.dispatcher import dp, bot
from main import admins


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru, back_main_menu_en]), state='*')
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=msg.text, reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(equals=[back_main_menu, back_main_menu_ru, back_main_menu_en]), state='*')
async def back_main_menu_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text=call.data, reply_markup=await main_menu_buttons(call.from_user.id))


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
    try:
        if tg_user['detail']:
            await state.set_state('language_1')
            await msg.answer(text="""
Tilni tanlang

-------------

Выберите язык

-------------

Select a language""", reply_markup=await language_buttons())
    except KeyError:
        if tg_user.get('language') == 'uz':
            await msg.answer(text=f"Bot yangilandi ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
        elif tg_user.get('language') == 'en':
            await msg.answer(text=f"Bot has been updated ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
        else:
            await msg.answer(text=f"Бот обновлен ♻", reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(startswith='language_'), state='language_1')
async def phone_number_function(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[-1]
    async with state.proxy() as data:
        data['language'] = lang
    await call.message.delete()
    await state.set_state('phone_number')

    # Telefon raqamni kiritish yoki yuborish uchun tugma yaratish
    contact_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button.add(KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True))

    if lang == "uz":
        await call.message.answer(
            text="""
📞 Ro'yxatdan o'tish uchun telefon raqamingizni kiriting yoki tugma orqali yuboring.

Raqamni +998********* shaklida yuboring.""",
            reply_markup=contact_button
        )
    elif lang == "en":
        await call.message.answer(
            text="""
📞 To register, please enter your phone number or send it via the button.

Send your number in the format +998*********.""",
            reply_markup=contact_button
        )
    else:
        await call.message.answer(
            text="""
📞 Чтобы зарегистрироваться, введите свой номер телефона или отправьте его через кнопку.

Отправьте номер в формате +998*********.""",
            reply_markup=contact_button
        )


@dp.message_handler(content_types=['text', 'contact'], state='phone_number')
async def handle_phone_number(msg: types.Message, state: FSMContext):
    phone_number = None
    if msg.content_type == 'contact':
        phone_number = msg.contact.phone_number
    elif msg.text.startswith("+998") and len(msg.text) == 13 and msg.text[1:].isdigit():
        phone_number = msg.text
    else:
        await msg.answer(
            "Iltimos, telefon raqamingizni to'g'ri formatda kiriting (+998*********) yoki tugma orqali yuboring.")
        return

    user_data = await state.get_data()
    language = user_data.get('language', 'uz')
    for admin in admins:
        await bot.send_message(
            chat_id=admin,
            text=f"""
Yangi user 🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Username: @{msg.from_user.username}
Ism-Familiya: {msg.from_user.full_name}
Telefon raqam: {phone_number}""",
            parse_mode='HTML'
        )
    data = {
        "chat_id": str(msg.from_user.id),
        "username": msg.from_user.username,
        "full_name": msg.from_user.full_name,
        "phone_number": phone_number,
        "language": language
    }
    requests.post(url="http://127.0.0.1:8000/api/telegram-users/create/", json=data)

    if language == 'uz':
        await msg.answer("""
Buyurtma berishni boshlash uchun 🛍 Buyurtma berish tugmasini bosing

Shuningdek, aksiyalarni ko'rishingiz va bizning filiallar bilan tanishishingiz mumkin""",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    elif language == 'en':
        await msg.answer("""
To start ordering, click the 🛍 Order button

You can also view promotions and find out about our branches""",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("""
Чтобы начать заказ, нажмите кнопку 🛍Заказать

Вы также можете увидеть акции и познакомиться с нашими партнерами.""",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()


@dp.message_handler(Text(equals=[choice_language, choice_language_ru, choice_language_en]))
async def change_language_function_1(msg: types.Message):
    await msg.answer(text="""
Tilni tanlang

-------------

Выберите язык

-------------

Select a language""", reply_markup=await language_buttons())


@dp.callback_query_handler(Text(startswith='language_'))
async def language_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content)
    data = {
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        "language": call.data.split("_")[-1]
    }
    requests.patch(url=f"http://127.0.0.1:8000/api/telegram-users/update/{tg_user['id']}/", data=data)
    await call.message.delete()
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text="Til o'zgartirildi 🇺🇿", reply_markup=await main_menu_buttons(call.from_user.id))
    elif call.data.split("_")[-1] == 'en':
        await call.message.answer(text="Language has been changed 🇬🇧",
                                  reply_markup=await main_menu_buttons(call.from_user.id))
    else:
        await call.message.answer(text="Язык изменен 🇷🇺", reply_markup=await main_menu_buttons(call.from_user.id))


@dp.message_handler(Text(equals=[change_phone, change_phone_ru, change_phone_en]))
async def change_phone_number_handler(msg: types.Message, state: FSMContext):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content
    )
    user_language = tg_user.get('language', 'uz')

    if user_language == 'uz':
        text = "📞 Yangi telefon raqamingizni kiriting. Raqamni +998********* shaklida yuboring:"
    elif user_language == 'en':
        text = "📞 Please enter your new phone number. Send it in the format +998*********:"
    else:
        text = "📞 Введите новый номер телефона. Отправьте его в формате +998*********:"

    await msg.answer(text=text, reply_markup=await back_main_menu_button(msg.from_user.id))
    await state.set_state('change_phone_number')


@dp.message_handler(state='change_phone_number')
async def save_new_phone_number(msg: types.Message, state: FSMContext):
    new_phone_number = msg.text.strip()

    if not new_phone_number.startswith("+998") or len(new_phone_number) != 13 or not new_phone_number[1:].isdigit():
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content
        )
        user_language = tg_user.get('language', 'uz')

        if user_language == 'uz':
            text = "❌ Telefon raqami noto'g'ri. Iltimos, raqamni +998********* shaklida yuboring."
        elif user_language == 'en':
            text = "❌ Invalid phone number. Please send the number in the format +998*********."
        else:
            text = "❌ Неверный номер телефона. Пожалуйста, отправьте его в формате +998*********."

        await msg.answer(text=text)
        return

    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content
    )
    data = {"phone_number": new_phone_number}
    response = requests.patch(url=f"http://127.0.0.1:8000/api/telegram-users/update/{tg_user['id']}/", data=data)
    tg_user = json.loads(response.content)
    user_language = tg_user.get('language', 'uz')

    if user_language == 'uz':
        text = "✅ Telefon raqamingiz muvaffaqiyatli o'zgartirildi."
    elif user_language == 'en':
        text = "✅ Your phone number has been successfully updated."
    else:
        text = "✅ Ваш номер телефона успешно обновлен."

    await msg.answer(text=text, reply_markup=await main_menu_buttons(msg.from_user.id))

    await state.finish()
