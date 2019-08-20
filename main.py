from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode, ContentTypes
from aiogram.utils.markdown import bold, code, italic, text

from config import TOKEN
import keyboard
import func



bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(lambda message: not func.chat_id_found(message.chat.id), commands=['start'])
async def welcome_message(message: types.Message):
    func.chat_id_add(message.chat.id)
    func.column_add(message.chat.id, "state", 1234)
    await message.reply("Привет!\nЯ — твой бот-помощник в школе испанского языка ESP.HOLA Вместе мы доберемся до свободного владения языком (уровня С2), моя задача — помнить всякое важное, твоя — тренироваться!\nЯ помогу записаться на занятия, покажу дорогу к нам в школу, предупрежу о любых изменениях расписания, напомню про домашку, и вообще я классный 👌🏻\nХочешь присоединиться к семье Esp.Hola? 😊", reply = False, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard.inline("Конечно!", "#setstate@1235"))


# @dp.message_handler(lambda message: func.column_take(message.chat.id, "state") == 1234, commands=['start'])
# async def full_name_request(message: types.Message):
#     full_name = func.check_full_name(message.chat.first_name + " " + message.chat.last_name) if "last_name" in message.chat else None
#     if full_name:
#         first_name, last_name = full_name
#         await message.reply('Вы *%s %s*?\nЕсли имя-фамилия определены неверно, пожалуйста, *напишите правильные* в формате: *Имя Фамилия*.\nЕсли все верно, нажмите "Далее" под этим сообщением\n' % (first_name, last_name), reply = False, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard.inline("Далее", "#setstate@1235"))
#     else:
#         await message.reply('Пожалуйста, *напишите имя и фамилию* в формате: *Имя Фамилия*.\n', reply = False, parse_mode=ParseMode.MARKDOWN)
#
# @dp.message_handler(lambda message: func.column_take(message.chat.id, "state") == 1235, commands=['start'])
# async def phone_number_again(message: types.Message):
#     await message.reply("Для взаимодействия на всех этапах работы с ботом может понадобиться Ваш номер телефона.\nПожалуйста, нажмите на кнопку \"*Поделиться номером*\".", parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard.phone_number("Поделиться номером 📲"), reply = False)
#
# @dp.message_handler(lambda message: func.column_take(message.chat.id, "state") == 1236, commands=['start'])
# async def welcome_again(message: types.Message):
#     await message.reply("Рад снова Вас видеть, %s!\nПеред Вами *сервис доставки еды на дом*." % (func.column_take(message.chat.id, "first_name")), reply = False, parse_mode=ParseMode.MARKDOWN)
#
# # @dp.message_handler(commands=['help'])
# # async def process_help_command(message: types.Message):
# #     await message.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")
#
@dp.message_handler(commands=['delete'])
async def process_help_command(message: types.Message):
    func.chat_id_del(message.chat.id)
    await message.reply("Данные о Вас удалены!")

@dp.message_handler(content_types=ContentTypes.CONTACT)
async def get_contact(message: types.Message):
    if func.column_take(message.chat.id, "state") == 1236:
        func.column_add(message.chat.id, "phone", message.contact["phone_number"])
        await bot.send_message(message.chat.id, "Спасибо за регистрацию! Теперь Вы можете полноценно пользоваться сервисом!", reply_markup = keyboard.remove())
        await take_level(message)


async def take_level(message: types.Message):
    func.column_add(message.chat.id, "state", 1237)
    text = "Пожалуйста, оцени свой уровень владения испанским (нажми на одну из кнопок под сообщением):\n\
\n\
*А1*\n\
\"Знакомство\". Буду учиться с самого начала!\n\
\n\
*А1.2*\n\
\"Влюбленность\". Уже могу рассказать о предпочтениях в еде, музыке и кино, пожаловаться на боль в спине, рассказать о планах на будущее и что произошло сегодня утром.\n\
\n\
*А2.1*\n\
\"Привыкание\". Не представляю жизнь без испанского. Без труда перевожу тексты (иногда с помощью Esp.Hola), могу поддержать разговор на разные темы, попросить размер S в ZARA или поругаться с администрацией отеля.\n\
\n\
*А2.2*\n\
\"Становление\". Чувствую, что пора брать билеты в Испанию. И беру, активнее принимаясь за испанский. Вместе мы повторяем пройденный материал и добавляем тему внешности и характера. Рассказать испанцам о нашем прошлом и будущем - ¡sin problemas!\n\
\n\
*B1.1*\n\
\"Зависимость\". Хотелось остановиться на А2.2, но не получилось.\n\
Правильно. Научимся выражать свое мнение, эмоции, спорить и даже, hostia, ругаться на испанском! Хотя вы это уже, наверное, умеете...\n\
\n\
*B1.2*\n\
\"Принятие\". Уже знаю, что не остановлюсь. Когда ты читаешь тексты любых типов и все это понимаешь уже без словаря — это бесценно! На этом этапе мы любим проводить дебаты, чтобы каждый мог высказать свое мнение по тому или иному вопросу. Добавим мистического субхунтиво!\n\
\n\
*B2.1*\n\
\"Любовь\". Уже на 90% испанец или испанка.\n\
Слово \"субхунтиво\" вы слышите чаще, чем свое имя. Мы научимся использовать разные стили письма, чтобы написать письмо работодателю, ведь вы уже запланировали переезд в Испанию, не так ли?\n\
\n\
*B2.2*\n\
\"Обожание\". Ваш испанский настолько превосходен, что вам уже предложили работу в центре Мадрида на Гран Виа. Вы слушаете радио Cadena 100 в испанском такси и вместе с водителем ругаете испанское правительство, особенно, Рахоя.\
*C*\n\
\"100% испанец\".\n\
Наша школа - ваш второй дом. Мы помогаем поддерживать ваш испанский на высоком уровне, добавляем в вашу речь много новой, не всегда приличной лексики, рассказываем о тонкостях и важных языковых нюансах. В Испании никто не догадается, что вы - не местный."
    kb = keyboard.inline([["A1.1", "A1.2", "A2.1", "A2.2"], ["B1.1", "B1.2", "B2.1", "B2.2"], ["C"]], [["#setlevel@A1.1", "#setlevel@A1.2", "#setlevel@A2.1", "#setlevel@A2.2"], ["#setlevel@B1.1", "#setlevel@B1.2", "#setlevel@B2.1", "#setlevel@B2.2"], ["#setlevel@C"]])
    await message.reply(text, parse_mode=ParseMode.MARKDOWN, reply_markup = kb, reply = False)



@dp.message_handler(lambda message: func.column_take(message.chat.id, "state") == 1235)
async def text_message1(message: types.Message):
    full_name = func.check_full_name(message.text)
    if full_name:
        first_name, last_name = full_name
        func.column_add(message.chat.id, "first_name", first_name)
        func.column_add(message.chat.id, "last_name", last_name)
        await take_phone(message)
    else:
        await bot.send_message(message.chat.id, "Неверный формат. Попробуйте снова.")

@dp.message_handler(lambda message: func.column_take(message.chat.id, "state") == 1240)
async def question_to_db(message: types.Message):
    func.column_add(message.chat.id, "question", message.text[:64])
    await bot.send_message(message.chat.id, "Мы уже работаем над ответом на твой вопрос!)")

@dp.message_handler()
async def text_message(message: types.Message):
    # await bot.send_message(message.chat.id, message.text, reply_markup=keyboard.reply([["📄 Меню", "🍱 Корзина"], ["👤 Профиль", "💬 Помощь"]] ))
    await bot.send_message(message.chat.id, message.text)


@dp.callback_query_handler(lambda callback_query: "#setstate@1236" in callback_query.data)
async def take_phone_callback(callback: types.CallbackQuery):
    message = callback.message; await callback.answer()
    if func.column_take(message.chat.id, "state") == 1235:
        full_name = func.check_full_name(message.chat.first_name + " " + message.chat.last_name)
        first_name, last_name = full_name
        func.column_add(message.chat.id, "first_name", first_name)
        func.column_add(message.chat.id, "last_name", last_name)
        await take_phone(message)

@dp.callback_query_handler(lambda callback_query: "#setstate@1241" in callback_query.data)
async def reg_well_done(callback: types.CallbackQuery):
    message = callback.message; await callback.answer()
    if func.column_take(message.chat.id, "state") == 1240:
        await message.reply("Отлично! Скоро мы свяжемся с тобой, чтобы договориться о встрече 🙌🏻\nДобро пожаловать в Esp.Hola! 💛", parse_mode=ParseMode.MARKDOWN, reply = False)


async def take_phone(message: types.Message):
    func.column_add(message.chat.id, "state", 1236)
    await message.reply("Еще мне нужно знать твой номер телефона, чтобы пригласить тебя в школу, и просто на всякий случай 👌🏻\nНажми \"Поделиться номером\" под этим сообщением", parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard.phone_number("Поделиться номером 📲"), reply = False)

async def days_choose(message: types.Message):
    func.column_add(message.chat.id, "state", 1238)
    await message.reply("Когда тебе удобно заниматься?", parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard.inline([["Понедельник-Среда"],["Вторник-Четверг"]], [["#setdays@Понедельник-Среда"],["#setdays@Вторник-Четверг"]]), reply = False)

async def time_choose(message: types.Message):
    func.column_add(message.chat.id, "state", 1239)
    await message.reply("Отлично! Твой выбор *{days}*\nА в какое время тебе удобно приходить?".format(days = func.column_take(message.chat.id, "days")), parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard.inline([["8:00", "10:00", "12:00"], ["14:00", "15:00", "16:00"], ["18:00", "19:00", "20:00"], ["Изменить дни недели"]], [["#settime@8:00", "#settime@10:00", "#settime@12:00"], ["#settime@14:00", "#settime@15:00", "#settime@16:00"], ["#settime@18:00", "#settime@19:00", "#settime@20:00"], ["#dayschoose"]]), reply = False)

async def questions_step(message: types.Message):
    func.column_add(message.chat.id, "state", 1240)
    await message.reply("Остались ли у тебя вопросы? Напиши их в ответ на это сообщение или нажми кнопку \"✅ Готово!\" ниже", parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard.inline("✅ Готово!", "#setstate@1241"), reply = False)


@dp.callback_query_handler(lambda callback_query: "#setstate@1235" in callback_query.data)
async def of_course_callback(callback: types.CallbackQuery):
    message = callback.message; await callback.answer()
    func.column_add(message.chat.id, "state", 1235)
    full_name = func.check_full_name(message.chat.first_name + " " + message.chat.last_name) if "last_name" in message.chat else None
    if full_name:
        first_name, last_name = full_name
        await bot.send_message(message.chat.id, "Привет!\nТы *{first_name}* *{last_name}*?\nЕсли имя-фамилия определены неверно, пожалуйста, *напиши правильные*!\nЕсли все верно, нажми \"Дальше\" под этим сообщением.".format(first_name = first_name, last_name = last_name), parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard.inline("Дальше ➡️", "#setstate@1236"))
    else:
        await message.reply('Пожалуйста, *напишите имя и фамилию* в формате: *Имя Фамилия*.\n', reply = False, parse_mode=ParseMode.MARKDOWN)



@dp.callback_query_handler(lambda callback_query: "#setdays" in callback_query.data)
async def setdays_callback(callback: types.CallbackQuery):
    message = callback.message; await callback.answer()
    if func.column_take(message.chat.id, "state") == 1238:
        days = callback.data.replace("#setdays@", "")
        func.column_add(message.chat.id, "days", days)
        await time_choose(message)

@dp.callback_query_handler(lambda callback_query: "#dayschoose" in callback_query.data)
async def days_choose_callback(callback: types.CallbackQuery):
    message = callback.message; await callback.answer()
    if func.column_take(message.chat.id, "state") == 1239:
        await days_choose(message)

@dp.callback_query_handler(lambda callback_query: "#setlevel" in callback_query.data)
async def setlevel_callback(callback: types.CallbackQuery):
    message = callback.message; await callback.answer()
    if func.column_take(message.chat.id, "state") == 1237:
        level = callback.data.replace("#setlevel@", "")
        func.column_add(message.chat.id, "level", level)
        await days_choose(message)

@dp.callback_query_handler(lambda callback_query: "#settime" in callback_query.data)
async def settime_callback(callback: types.CallbackQuery):
    message = callback.message; await callback.answer()
    if func.column_take(message.chat.id, "state") == 1239:
        time = callback.data.replace("#settime@", "")
        func.column_add(message.chat.id, "time", time)
        await questions_step(message)

@dp.callback_query_handler()
async def any_callback(callback: types.CallbackQuery):
    message = callback.message; await callback.answer()
    await bot.send_message(message.chat.id, "callback: " + callback.data)

if __name__ == '__main__':
    executor.start_polling(dp)
