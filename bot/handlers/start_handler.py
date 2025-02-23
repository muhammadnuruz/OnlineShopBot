import json
from collections import Counter
from token import AWAIT

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.inline_buttons import language_buttons
from bot.buttons.reply_buttons import main_menu_buttons, back_main_menu_button, to_back_button, shop_menu_buttons, \
    location_buttons
from bot.buttons.text import back_main_menu, choice_language, choice_language_ru, back_main_menu_ru, change_phone, \
    change_phone_ru, to_back_ru, to_back
from bot.dispatcher import dp, bot
from main import admins


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru]), state='*')
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=msg.text, reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(equals=[back_main_menu, back_main_menu_ru]), state='*')
async def back_main_menu_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text=call.data, reply_markup=await main_menu_buttons(call.from_user.id))


@dp.message_handler(Text(equals=[to_back, to_back_ru]),
                    state=['get_food', 'put_in_basket', 'basket_menu', 'confirm_payment', 'confirm_order'])
async def ordering_function_3(msg: types.Message, state: FSMContext):
    try:
        await state.finish()
        await state.set_state('ordering_state')
        await msg.answer(text=msg.text, reply_markup=await shop_menu_buttons(msg.from_user.id))
    except Exception as e:
        await state.finish()
        await msg.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(msg.from_user.id))
        await bot.send_message(admins[0], text=e)


@dp.message_handler(state="confirm_payment")
async def payment_confirmed_handler(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            pass
        args = message.get_args()
        if str(data['i_time']) != str(args):
            await message.reply(text="Вы еще не заплатили ❌",
                                reply_markup=await to_back_button(chat_id=message.from_user.id))
            return
        tg_user_response = requests.get(
            url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{message.from_user.id}/"
        )
        tg_user = tg_user_response.json()
        response = requests.get(f"http://127.0.0.1:8000/api/baskets/{message.from_user.id}/")
        basket_data = response.json()
        basket_items = basket_data.get("results", [])

        food_counter = Counter(item["food"] for item in basket_items)

        basket_text = (
            "\U0001F6D2 Sizning buyurtmalaringiz:\n\n"
            if tg_user.get("language") == "uz"
            else "\U0001F6D2 Ваши заказы:\n\n"
        )

        total_price = 0
        food_items = {}

        for food_id, quantity in food_counter.items():
            food_response = requests.get(url=f"http://127.0.0.1:8000/api/foods/id/{food_id}/")
            food_data = food_response.json()
            food_name = food_data.get("name") if tg_user["language"] == "uz" else food_data.get("ru_name")
            food_price = int(food_data.get("price", 0))

            if food_name not in food_items:
                food_items[food_name] = {"price": food_price, "quantity": quantity}
            else:
                food_items[food_name]["quantity"] += quantity

            total_price += food_price * quantity
            basket_text += f"{food_name} {food_price} so'm x {quantity} = {food_price * quantity} so'm\n"

        post_data = {
            "total_price": total_price,
            "delivery_address": tg_user.get('location', 'No location'),
            "latitude": tg_user.get('latitude'),
            "longitude": tg_user.get('longitude'),
            "payment_confirmed": True,
            "user": tg_user.get('id'),
            "food_items": [
                {"food_name": name, "price": item['price'], "quantity": item['quantity']} for name, item in
                food_items.items()
            ]
        }

        order_response = requests.post(url="http://127.0.0.1:8000/api/orders/create/", json=post_data)
        if order_response.status_code != 201:
            raise ValueError("Failed to create order")

        requests.delete(f"http://127.0.0.1:8000/api/baskets/delete_all_baskets/{tg_user['id']}/")

        basket_text += (
            f"\nJami: {total_price} so'm\nGeolokatsiya: {tg_user.get('location', 'No location')}"
            if tg_user["language"] == "uz"
            else f"\nИтого: {total_price} сум\nГеолокация: {tg_user.get('location', 'No location')}"
        )

        admin_text = (
            f"🛒 <b>Новый заказ</b>\n\n"
            f"👤 <b>Клиент:</b> {tg_user.get('full_name', 'No name')}\n"
            f"📞 <b>Телефон:</b> {tg_user.get('phone_number', 'No phone')}\n"
            f"🏠 <b>Адрес доставки:</b> {tg_user.get('location', 'No location')}\n\n"
            f"📦 <b>Заказанные товары:</b>\n{basket_text}\n\n"
            f"💳 <b>Общая сумма:</b> {total_price} сум\n"
        )
        for admin_id in admins:
            await bot.send_message(chat_id=admin_id, text=admin_text, parse_mode="HTML")

        await state.finish()
        await message.reply(
            f"Buyurtmangiz qabul qilindi! {basket_text}"
            if tg_user["language"] == "uz"
            else f"Ваш заказ принят! {basket_text}",
            reply_markup=await main_menu_buttons(message.from_user.id)
        )

    except Exception as e:
        await state.finish()
        await message.answer(text="Xatolik yuz berdi!", reply_markup=await main_menu_buttons(message.from_user.id))
        await bot.send_message(admins[0], text=f"Payment confirmation error: {e}")


@dp.message_handler(CommandStart(), state="*")
async def start_handler(msg: types.Message, state: FSMContext):
    args = msg.get_args()
    if args == 'confirm_payment':
        await state.set_state("basket_menu")
        await msg.answer(text="Заказ подтвержден ✔")
        await msg.answer("Пожалуйста, пришлите свое местоположение.", reply_markup=await location_buttons())
    else:
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)
        try:
            if tg_user['detail']:
                await state.set_state('language_1')
                await msg.answer(text="""
    Tilni tanlang
    
    -------------
    
    Выберите язык""", reply_markup=await language_buttons())
        except KeyError:
            await state.finish()
            if tg_user.get('language') == 'uz':
                await msg.answer(text=f"Bot yangilandi ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
            else:
                await msg.answer(text=f"Бот обновлен ♻", reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(startswith='language_'), state='language_1')
async def phone_number_function(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[-1]
    async with state.proxy() as data:
        data['language'] = lang
    await call.message.delete()
    await state.set_state('phone_number')

    contact_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button.add(KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True))

    if lang == "uz":
        await call.message.answer(
            text="""
📞 Ro'yxatdan o'tish uchun telefon raqamingizni kiriting yoki tugma orqali yuboring.

Raqamni +998********* shaklida yuboring.""",
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
    else:
        await msg.answer("""
Чтобы начать заказ, нажмите кнопку 🛍Заказать

Вы также можете увидеть акции и познакомиться с нашими партнерами.""",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()


@dp.message_handler(Text(equals=[choice_language, choice_language_ru]))
async def change_language_function_1(msg: types.Message):
    await msg.answer(text="""
Tilni tanlang

-------------

Выберите язык""", reply_markup=await language_buttons())


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
    else:
        await call.message.answer(text="Язык изменен 🇷🇺", reply_markup=await main_menu_buttons(call.from_user.id))


@dp.message_handler(Text(equals=[change_phone, change_phone_ru]))
async def change_phone_number_handler(msg: types.Message, state: FSMContext):
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content
    )
    user_language = tg_user.get('language', 'uz')

    if user_language == 'uz':
        text = "📞 Yangi telefon raqamingizni kiriting. Raqamni +998********* shaklida yuboring:"
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
    else:
        text = "✅ Ваш номер телефона успешно обновлен."

    await msg.answer(text=text, reply_markup=await main_menu_buttons(msg.from_user.id))

    await state.finish()
