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

# --- СЦЕНА 8: ТЕЛЕФОННАЯ БУДКА (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_8_booth")
async def scene_8_booth(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Резкий вдох. Открыть глаза.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Я подошел к разбитой телефонной будке. Внутри пахло сыростью и старым пластиком. Я снял трубку — гудков не было, только тихий статический треск. \n\n"
            "Внезапно треск превратился в шепот: «Ты не там ищешь». "
            "Я резко обернулся, но дверь будки уже была заблокирована. Снаружи стоял он. Фигура в дождевике просто прижала ладонь к стеклу. "
            "Стекло взорвалось внутрь тысячами острых осколков. Один из них попал прямо в артерию на шее. Горячая кровь. Темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 8: ПОДЗЕМНЫЙ ПЕРЕХОД (СЮЖЕТ И ТУРНИКЕТ) ---
@dp.callback_query(lambda c: c.data == "scene_8_underground")
async def scene_8_underground(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Опустить черный жетон в щель", callback_data="scene_9_token")
    kb.button(text="Перепрыгнуть через турникет", callback_data="scene_9_jump")
    kb.adjust(1)
    
    text = ("Я послушался записки и шагнул в сырую темноту подземного перехода. Свет с улицы сюда почти не проникал. "
            "Ступени вели всё ниже и ниже, глубже, чем должно быть обычное метро. \n\n"
            "Внезапно туннель перегородила массивная железная решетка. В ней была оставлена только одна узкая калитка, а перед ней — старый советский турникет. "
            "Лампочка на нем не горела. На металлическом корпусе блестела узкая щель жетоноприемника. \n\n"
            "Где-то на ступенях позади меня послышались тяжелые, хлюпающие шаги. Он идет следом! Времени в обрез.")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 9: ПРЫЖОК ЧЕРЕЗ ТУРНИКЕТ (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_9_jump")
async def scene_9_jump(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Резкий вдох. Открыть глаза.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Я решил не тратить время и, опершись на скользкий металл, прыгнул через турникет. \n\n"
            "В ту же секунду пространство вокруг меня дрогнуло, словно на зажеванной видеокассете. "
            "Воздух стал плотным, как бетон. Мое тело буквально застыло в воздухе прямо над турникетом, я не мог пошевелить даже пальцем, словно баг в программном коде.\n\n"
            "Система не прощает нарушений. Из темноты не спеша вышел человек в дождевике. Он подошел, посмотрел на меня с абсолютным равнодушием "
            "и вонзил нож мне в сердце. Темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 9: ЧЕРНЫЙ ЖЕТОН (СЮЖЕТ - ПЛАТФОРМА) ---
@dp.callback_query(lambda c: c.data == "scene_9_token")
async def scene_9_token(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Зайти в пустой вагон", callback_data="scene_10_train")
    kb.button(text="Осмотреть странные часы на стене", callback_data="scene_10_clock")
    kb.adjust(1)
    
    text = ("Я закинул матовый черный жетон в прорезь. Раздался не металлический лязг, а странный электронный звук, похожий на загрузку старого компьютера. "
            "Турникет мягко провернулся. Шаги преследователя позади внезапно стихли, будто нас отрезало друг от друга невидимой стеной.\n\n"
            "Спустившись по неработающему эскалатору на платформу «Василеостровской», я обомлел. Она выглядела... иначе. "
            "Никакой рекламы, никаких современных указателей. Только тусклый зеленоватый свет и идеальная, мертвая тишина. "
            "Воздух здесь словно наэлектризован, а реальность кажется хрупкой, будто я выпал из привычного мира в параллельное измерение.\n\n"
            "У перрона с открытыми дверями стоит абсолютно пустой состав. А на стене станции висят огромные часы, стрелки которых быстро крутятся в обратную сторону.")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 10: ЧАСЫ (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_10_clock")
async def scene_10_clock(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(3)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Снова этот кошмар. Проснуться.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Я подошел к огромным циферблатам. Стрелки бешено вращались против часовой. Я завороженно смотрел на них, пытаясь понять логику механизма, как вдруг осознал: они буквально отматывают мое время назад.\n\n"
            "Глухой звук шагов позади. Пространство на платформе снова сомкнулось. Тот факт, что я задержался, позволил «ему» нагнать меня. "
            "Я обернулся слишком поздно. Человек в дождевике стоял вплотную. Холодное лезвие. Темнота. Очередная ветка реальности обрывается...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 10: ПУСТОЙ ВАГОН (СЮЖЕТ - ПАРАЛЛЕЛЬНЫЕ МИРЫ) ---
@dp.callback_query(lambda c: c.data == "scene_10_train")
async def scene_10_train(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Смотреть в черное окно туннеля", callback_data="scene_11_window")
    kb.button(text="Открыть папку на сиденье", callback_data="scene_11_folder")
    kb.adjust(1)
    
    text = ("Я запрыгнул в вагон. Двери тут же с шипением захлопнулись. Поезд дернулся и начал набирать скорость, уходя в абсолютно черный туннель. \n\n"
            "В вагоне неестественно тихо. Нет привычного стука колес, только ровный низкий гул, словно работают мощные серверные кулеры. "
            "Я прошел вглубь салона. На одном из дерматиновых сидений лежала пухлая картонная папка. Из нее торчали какие-то распечатки, базы данных, схемы и фотографии.\n\n"
            "А за окном туннеля начало происходить нечто невообразимое. Вместо кабелей и бетона там мелькали вспышки света, похожие на обрывки других жизней... параллельных реальностей, где я принимал другие решения, жил другой жизнью и не попадал в эту петлю.")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 11: ОКНО (СМЕРТЬ ОТ ПЕРЕГРУЗКИ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_11_window")
async def scene_11_window(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Резкий вдох. Открыть глаза.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Я прислонился лбом к холодному стеклу. Вспышки в туннеле становились всё четче. Я увидел... себя. "
            "В одной из реальностей я просто крутил баранку автомобиля, уставший после обычной смены. В другой — меня насмерть сбивала машина. "
            "Это была наглядная демонстрация квантового бессмертия. Я видел бесконечное древо параллельных миров.\n\n"
            "Но человеческий мозг не создан для того, чтобы видеть исходный код симуляции. От бесконечного потока данных пространство начало искажаться, "
            "мысли превратились в ослепительный белый шум. Разум просто не выдержал перегрузки. Темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 11: ПАПКА С ДОСЬЕ (СЮЖЕТ) ---
@dp.callback_query(lambda c: c.data == "scene_11_folder")
async def scene_11_folder(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Выйти на пустую платформу", callback_data="scene_12_platform")
    kb.button(text="Остаться в вагоне", callback_data="scene_12_stay")
    kb.adjust(1)
    
    text = ("Я отвернулся от пугающего окна и открыл папку. Внутри было мое досье. Но не полицейское. "
            "Кто-то буквально препарировал мою цифровую жизнь: логи настроек моих приватных браузеров, схемы с фейковыми аккаунтами на Reddit, "
            "зарегистрированными через Proton Mail, и даже глубокий анализ EXIF-метаданных моих личных фотографий.\n\n"
            "Они использовали продвинутые методы разведки по открытым источникам, чтобы отследить каждый мой шаг в сети. "
            "Под кипой распечаток лежал старый бумажный билет, на котором было выбито: «Конечная. Узел связи». \n\n"
            "В этот момент поезд издал пронзительный визг тормозов. Двери с шипением открылись в полумрак неизвестной станции.")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 12: ОСТАТЬСЯ В ВАГОНЕ (СМЕРТЬ И ПЕТЛЯ) ---
@dp.callback_query(lambda c: c.data == "scene_12_stay")
async def scene_12_stay(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Снова этот кошмар. Проснуться.", callback_data="restart_loop")
    kb.adjust(1)
    
    text = ("Я решил, что безопаснее остаться внутри, и отступил вглубь вагона. Двери с шипением закрылись, отрезая меня от станции.\n\n"
            "Поезд сорвался с места. Вскоре ровный гул серверов сменился жестким металлическим лязгом. Звук был до боли знакомый — точь-в-точь как стук растянутой цепи ГРМ на моем старом пежо с двигателем EP6 перед тем, как он окончательно встал и потребовал капиталки.\n\n"
            "Лязг перерос в оглушающий рев. Вагон начало трясти так, что меня швырнуло на пол. Стены стали раскаляться докрасна, воздух выгорел за секунду. Похоже, система просто удалила этот вагон как программный мусор. Темнота...")
    
    await callback.message.answer(text, reply_markup=kb.as_markup())
    await callback.answer()

# --- СЦЕНА 12: ПЛАТФОРМА «УЗЕЛ СВЯЗИ» (СЮЖЕТ) ---
@dp.callback_query(lambda c: c.data == "scene_12_platform")
async def scene_12_platform(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(4)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Подойти к главному терминалу", callback_data="scene_13_terminal")
    kb.button(text="Осмотреть гермодверь в конце зала", callback_data="scene_13_door")
    kb.adjust(1)
    
    text = ("Я сделал глубокий вдох и шагнул на холодный бетон. За спиной тут же сомкнулись двери, и поезд-призрак бесшумно растворился во мраке туннеля.\n\n"
            "Станция «Узел связи» вообще не была похожа на метро. Это напоминало гигантский подземный дата-центр. Бесконечные ряды гудящих серверных стоек, мигающие индикаторы коммутаторов и толстые пучки оптоволокна, уходящие куда-то под потолок. \n\n"
            "Посреди зала возвышался одинокий стол с включенным главным терминалом. Экран заливал темноту ядовито-зеленым светом. А в самом конце зала виднелась огромная стальная гермодверь с массивным вентилем.")
    
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
