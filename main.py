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
    kb.button(text="Хватай нож и спроси, кто там!", callback_data="scene_3_knife")
    kb.button(text="Бей окно, лезь на пожарную лестницу!", callback_data="scene_3_window")
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
# --- СЦЕНА 3: НОЖ И ЗАСАДА ---
@dp.callback_query(lambda c: c.data == "scene_3_knife")
async def scene_3_knife(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Ударить, как только дверь приоткроется!", callback_data="scene_4_strike")
    kb.button(text="Пропустить его в коридор и напасть со спины", callback_data="scene_4_stealth")
    kb.adjust(1)
    
    text = ("Я метнулся на кухню, выхватил из подставки самый длинный шеф-нож и крикнул в сторону коридора: «Кто там?! Я вызвал полицию!».\n\n"
            "Стук мгновенно прекратился. Повисла мертвая тишина, только дождь барабанит по карнизу. А затем я услышал тихий металлический скрежет — он вскрывает замок отмычкой. "
            "Я вжался спиной в стену сбоку от входной двери, сжав рукоять ножа так, что побелели костяшки. Замок щелкнул. Ручка начала медленно опускаться вниз...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 3: ПОЖАРНАЯ ЛЕСТНИЦА ---
@dp.callback_query(lambda c: c.data == "scene_3_window")
async def scene_3_window(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Лезть наверх, на крышу", callback_data="scene_4_roof")
    kb.button(text="Спускаться вниз, в темный двор", callback_data="scene_4_yard")
    kb.adjust(1)
    
    text = ("Я схватил тяжелую табуретку и со всего размаху всадил ее в окно. Стекло брызнуло во все стороны. Холодный ливень ударил прямо в лицо. "
            "Я перекинул ноги через подоконник и вцепился в ржавые прутья пожарной лестницы. \n\n"
            "В этот самый момент входная дверь в квартиру с треском вылетела. Я успел заметить в коридоре высокую фигуру в черном дождевике, прежде чем начать двигаться. "
            "Металл скользкий от дождя, руки дрожат. Куда рвануть?")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

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
    print("Бот и веб-сервер запущены! Петля активна.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
