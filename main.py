import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "8658859502:AAGtsBnmte6n_uhqHowBFFoO1Jm2yS3EY3g"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- СЦЕНА 1: ПРОБУЖДЕНИЕ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await asyncio.sleep(2) 
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Ты под чем-то? Какая смерть?", callback_data="scene_2")
    kb.button(text="Успокойся. Подробности. Как умер?", callback_data="scene_2")
    kb.adjust(1) 
    
    text = ("Слушай, я не знаю, кто ты. Твой контакт был нацарапан на обратной стороне моего проездного. "
            "Если это чья-то больная шутка, то мне ни черта не смешно. Я... я только что умер. "
            "И снова проснулся у себя в квартире. На Васильевском острове.")
    
    await message.answer(text, reply_markup=kb.as_markup())

# --- СЦЕНА 2: АВАРИЯ (С ФОТО) ---
@dp.callback_query(lambda c: c.data == "scene_2")
async def scene_2(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="upload_photo")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Посмотри в глазок. Только тихо!", callback_data="scene_3_peephole")
    kb.button(text="Хватай нож и спроси, кто там!", callback_data="scene_3")
    kb.button(text="Бей окно, лезь на пожарную лестницу!", callback_data="scene_3")
    kb.adjust(1)
    
    text = ("Я переходил Лиговский. Визг тормозов, удар, хруст... и темнота. А потом резкий вдох — и я лежу в своей кровати. "
            "Дождь за окном стучит точно так же. Время на электронных часах — 19:42. Ровно за час до аварии.\n\n"
            "Бляха... Кто-то ломится в дверь. Стучат так, что штукатурка сыплется. Что делать?!")
            
    try:
        photo = FSInputFile("OIG2.jpg")
        await callback.message.answer_photo(photo=photo, caption=text, reply_markup=kb.as_markup())
    except Exception:
        await callback.message.answer(f"Текст:\n\n{text}", reply_markup=kb.as_markup())
        
    await callback.answer()

# --- СЦЕНА 3: ГЛАЗОК ---
@dp.callback_query(lambda c: c.data == "scene_3_peephole")
async def scene_3_peephole(callback: types.CallbackQuery):
    # Убираем кнопки у прошлого сообщения, чтобы игрок не мог нажать их дважды
    await callback.message.edit_reply_markup(reply_markup=None) 
    
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Рвануть дверь и сбить его с ног!", callback_data="scene_4_attack")
    kb.button(text="Отбежать в ванную и запереться", callback_data="scene_4_bathroom")
    kb.adjust(1)
    
    text = ("Я на цыпочках подкрался к двери и прильнул к глазку. На лестничной клетке мигает перегоревшая лампа. "
            "Там стоит кто-то в черном мокром дождевике. Лица не видно, капюшон надвинут на самые глаза. "
            "Он вдруг перестает стучать, медленно поднимает голову к глазку и... я клянусь, он смотрит прямо на меня. "
            "Достает из кармана что-то металлическое и начинает ковыряться в замке. Он вскрывает дверь!")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()
