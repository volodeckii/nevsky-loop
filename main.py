import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "8658859502:AAEa1fsHa-5GhhF5Jag1Kpr4D8CMFgEg8Z4"

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

# --- СЦЕНА 4: ВАННАЯ И ПЕЙДЖЕР ---
@dp.callback_query(lambda c: c.data == "scene_4_bathroom")
async def scene_4_bathroom(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="upload_photo")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Взять пейджер и прочитать сообщение", callback_data="scene_5_pager_read")
    kb.button(text="Бросить его и искать оружие", callback_data="scene_5_search_weapon")
    kb.adjust(1)
    
    text = ("Я отскочил от двери, влетел в ванную и с щелчком задвинул задвижку. В коридоре раздался грохот — входную дверь высадили.\n\n"
            "Тяжелые мокрые шаги медленно приближаются. Я пячусь к раковине, тяжело дыша, и вдруг слышу звук. Писк. "
            "В пустой металлической раковине лежит старый черный пейджер. Экран светится зеленым, на него только что пришло сообщение. "
            "Шаги за дверью замерли, кто-то положил руку на ручку...")
            
    try:
        # УБЕДИСЬ, ЧТО НАЗВАНИЕ КАРТИНКИ СОВПАДАЕТ С ТВОИМ ФАЙЛОМ НА GITHUB!
        photo = FSInputFile("pager.jpg")
        await callback.message.answer_photo(photo=photo, caption=text, reply_markup=kb.as_markup())
    except Exception:
        await callback.message.answer(f"Текст:\n\n{text}", reply_markup=kb.as_markup())
        
    await callback.answer()

# --- СЦЕНА 4: НАПАДЕНИЕ У ДВЕРИ (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_4_attack")
async def scene_4_attack(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Резкий вдох. Открыть глаза.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Я рванул замок и со всей силы толкнул дверь плечом. Тяжелое деревянное полотно с хрустом впечаталось в фигуру в дождевике. "
            "Он пошатнулся, но не упал. Я с рычанием бросился на него, целясь в шею, но его реакция была нечеловеческой. \n\n"
            "Взмах руки в черной перчатке. Короткая вспышка тусклого света на лезвии. Жгучая, невыносимая боль пронзила грудь. "
            "Я осел на грязный кафель подъезда, захлебываясь. Черный капюшон склонился надо мной. Темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- ПЕРЕЗАПУСК ПЕТЛИ ---
@dp.callback_query(lambda c: c.data == "restart_loop")
async def restart_loop(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(2)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Ты под чем-то? Какая смерть?", callback_data="scene_2")
    kb.button(text="Успокойся. Подробности. Как умер?", callback_data="scene_2")
    kb.adjust(1) 
    
    text = ("*СНОВА ЭТОТ КОШМАР*\n\n"
            "Я... я опять проснулся в кровати. Холодный пот льет ручьем. На часах 19:42. Я же только что умер в подъезде! "
            "Слушай, контакт на проездном — это моя единственная зацепка. Помоги мне, иначе я так и буду умирать здесь вечно!")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 5: ПРОЧИТАТЬ ПЕЙДЖЕР (СЮЖЕТ) ---
@dp.callback_query(lambda c: c.data == "scene_5_pager_read")
async def scene_5_pager_read(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Лезть в узкое вентиляционное окно под потолком", callback_data="scene_6_vent")
    kb.button(text="Спрятаться в самой ванной за шторкой", callback_data="scene_6_hide")
    kb.adjust(1)
    
    text = ("Я дрожащими руками хватаю пейджер. На узком зеленоватом экране светится сообщение:\n\n"
            "«ОНИ ЗНАЮТ О ПЕТЛЕ. УХОДИ. ИЩИ ЧЕРНЫЙ ЖЕТОН У МЕТРО ВАСИЛЕОСТРОВСКАЯ»\n\n"
            "В этот момент хлипкая дверь ванной содрогается от чудовищного удара. Дерево трещит. "
            "Еще один удар — и он ворвется сюда. У меня есть считанные секунды!")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 5: ИСКАТЬ ОРУЖИЕ (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_5_search_weapon")
async def scene_5_search_weapon(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Снова этот кошмар. Проснуться.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("К черту пейджер! Я лихорадочно шарю по полкам, хватаю тяжелые парикмахерские ножницы и встаю в стойку. "
            "Дверь разлетается в щепки. В ванную вваливается массивная фигура в черном дождевике. \n\n"
            "Я бью ножницами наотмашь, целясь в шею... но лезвие со скрежетом скользит по чему-то твердому под плащом. Броня? "
            "Он даже не дрогнул. Огромная рука в перчатке перехватывает мое горло и с нечеловеческой силой впечатывает в кафель. Воздух кончился. Снова темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 6: ВЕНТИЛЯЦИЯ (СПАСЕНИЕ НА УЛИЦУ) ---
@dp.callback_query(lambda c: c.data == "scene_6_vent")
async def scene_6_vent(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Рвануть дворами к метро", callback_data="scene_7_subway")
    kb.button(text="Спрятаться в арке и осмотреться", callback_data="scene_7_arch")
    kb.adjust(1)
    
    text = ("Я запрыгнул на край раковины, сорвал решетку вентиляции и втиснулся в узкую шахту. "
            "В этот же момент дверь ванной с треском вылетела. Я замер в темноте, не дыша. Внизу кто-то тяжело топтался, скрипел стеклом на полу. \n\n"
            "Выждав минуту, я пополз по пыльному коробу. Он вывел меня на чердак, а оттуда — через служебную лестницу — прямо в темный петербургский двор. "
            "Дождь льет стеной. До метро Василеостровская пара кварталов, но улицы могут патрулировать...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 6: ПРЯТАТЬСЯ ЗА ШТОРКОЙ (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_6_hide")
async def scene_6_hide(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Снова этот кошмар. Проснуться.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Паника сковала меня. Я залез в саму ванну и задернул дешевую пластиковую шторку. Гениальный план, ничего не скажешь... "
            "Дверь с грохотом вылетела. Шаги приблизились к раковине. Секунда тишины. \n\n"
            "Шторку резко сдернули. Человек в дождевике даже не стал доставать нож. Он просто протянул руку в черной перчатке и сжал мое лицо, вдавливая в затылок. "
            "Хруст шейных позвонков. Темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 4: НОЖ - УДАР В ЛОБ (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_4_strike")
async def scene_4_strike(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Резкий вдох. Открыть глаза.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Едва дверь приоткрылась, я с криком рванул вперед, нанося удар ножом сверху вниз. \n\n"
            "Но я недооценил его реакцию. Дверь резко распахнулась до конца, ударив меня по руке. Нож со звоном отлетел в сторону. "
            "Фигура в дождевике сделала неуловимое движение. Тупое лезвие пробило ребра. Я осел на пол, хватая ртом воздух. "
            "Холодные глаза из-под капюшона. Темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 4: НОЖ - НАПАСТЬ СО СПИНЫ (ВЫЖИВАНИЕ) ---
@dp.callback_query(lambda c: c.data == "scene_4_stealth")
async def scene_4_stealth(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Рвануть по лестнице вниз, на улицу!", callback_data="scene_7_subway") # Заметь, ведет на ту же сцену, что и вентиляция!
    kb.button(text="Осмотреть его карманы", callback_data="scene_5_loot")
    kb.adjust(1)
    
    text = ("Я вжался в стену, почти не дыша. Дверь скрипнула, и высокая фигура в мокром дождевике медленно шагнула в прихожую. "
            "Он двинулся на кухню, держа в руке что-то блестящее. \n\n"
            "Это мой шанс. Я замахнулся и со всей силы ударил рукоятью ножа (тяжелой стальной пяткой) ему в основание черепа. "
            "Раздался глухой стук. Человек рухнул на пол, как подкошенный, но тут же начал шевелиться. Удар лишь оглушил его на пару секунд!")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 5: ОСМОТРЕТЬ КАРМАНЫ (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_5_loot")
async def scene_5_loot(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Резкий вдох. Открыть глаза.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Жадность или глупое любопытство сыграли со мной злую шутку. Я наклонился над лежащим телом и сунул руку в карман его мокрого дождевика.\n\n"
            "Внезапно его рука, словно стальной капкан, сомкнулась на моем запястье. Он не был в отключке! Резкий рывок на себя, тусклый блеск лезвия... "
            "Холодная сталь вошла мне точно под ребра. Я рухнул рядом с ним, глядя, как он медленно поднимается. Темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 4: ОКНО - НА КРЫШУ (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_4_roof")
async def scene_4_roof(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Снова этот кошмар. Проснуться.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Я рванул вверх по ржавым ступеням. Дождь хлестал в лицо, металл скользил под руками. Я выбрался на плоскую крышу и обернулся.\n\n"
            "Он уже был там. Черный силуэт на фоне грозового неба. Я попятился, поскользнулся на мокром рубероиде и потерял равновесие. "
            "Край крыши. Пустота. Ощущение свободного падения и резкий, дробящий кости удар о мокрый асфальт двора. Темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 4: ОКНО - ВНИЗ ВО ДВОР (ВЫЖИВАНИЕ) ---
@dp.callback_query(lambda c: c.data == "scene_4_yard")
async def scene_4_yard(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Рвануть дворами к метро", callback_data="scene_7_subway")
    kb.button(text="Спрятаться в арке и осмотреться", callback_data="scene_7_arch")
    kb.adjust(1)
    
    text = ("Не раздумывая, я начал быстро спускаться вниз. Ржавые крепления опасно скрипели, но выдержали. Я спрыгнул в грязь темного петербургского двора-колодца.\n\n"
            "Глянув наверх, я увидел, как из моего разбитого окна высовывается фигура в черном. Он заметил меня. "
            "Нужно убираться отсюда! До метро Василеостровская пара кварталов, но бежать по открытым улицам — чистое самоубийство.")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 7: МЕТРО ВАСИЛЕОСТРОВСКАЯ (СЮЖЕТ И ЖЕТОН) ---
@dp.callback_query(lambda c: c.data == "scene_7_subway")
async def scene_7_subway(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    
    # Меняем статус бота на "отправляет фото"
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="upload_photo")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Спуститься в подземный переход", callback_data="scene_8_underground")
    kb.button(text="Осмотреть телефонную будку у входа", callback_data="scene_8_booth")
    kb.adjust(1)
    
    text = ("Я рванул через дворы, перемахивая через лужи и пугая редких бродячих собак. Сердце колотилось в горле. "
            "Наконец, впереди показался массивный козырек станции метро «Василеостровская». Двери были закрыты — станция не работает. \n\n"
            "Я подошел ближе. На каменном парапете у входа, прямо под тусклым фонарем, лежал абсолютно черный, матовый металлический жетон метрополитена. "
            "Под ним клочок бумаги, размокший от дождя. На нем корявым почерком: «Спускайся. Они боятся темноты».\n\n"
            "Я сжал холодный жетон в кулаке. Куда идти дальше?")
            
    try:
        # ИМЯ ФАЙЛА КАРТИНКИ (УБЕДИСЬ, ЧТО ОНО СОВПАДАЕТ С GITHUB)
        photo = FSInputFile("token.jpg")
        await callback.message.answer_photo(photo=photo, caption=text, reply_markup=kb.as_markup())
    except Exception:
        # Если картинка не прогрузится, бот пришлет хотя бы текст
        await callback.message.answer(f"Текст:\n\n{text}", reply_markup=kb.as_markup())
        
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
