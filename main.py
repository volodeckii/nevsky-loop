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
    kb.button(text="Посмотри в глазок. Только тихо!", callback_data="scene_3")
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

@dp.callback_query(lambda c: c.data == "scene_3")
async def scene_3(callback: types.CallbackQuery):
    await callback.answer("Продолжение следует! База работает отлично 🚀", show_alert=True)

# Заглушка веб-сервера для Render (чтобы сервис не засыпал)
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    # Запускаем веб-сервер и бота одновременно
    asyncio.create_task(web_server())
    print("Бот и веб-сервер запущены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
