from fileinput import close

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import token, chat_id, chat_id2  # Создается фаил и в него добовляются токен бота и чат группы, куда должна осуществляться отправка автоматических сообщений.
import asyncio
from aiogram import Bot, Dispatcher, executor, types
import json
import datetime
from pytz import timezone
from aiogram.dispatcher.filters import Text



bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
time_UTH = datetime.datetime.now(datetime.timezone.utc)
NYC = timezone('Asia/Baku')
time_world = time_UTH.astimezone(NYC)
week_day_let = time_world.weekday()
hour_world_let = time_world.hour
minute_world = datetime.datetime.now().minute

# Установка дня недели
def week_day():
    time_UTH = datetime.datetime.now(datetime.timezone.utc)
    NYC = timezone('Asia/Baku')
    time_world = time_UTH.astimezone(NYC)
    return time_world.weekday()

# Устанока мирового времени
def hour_world():
    time_UTH = datetime.datetime.now(datetime.timezone.utc)
    NYC = timezone('Asia/Baku')
    time_world = time_UTH.astimezone(NYC)
    return time_world.hour

# функция установки даты заданного дня
def get_data(k):
    a = datetime.datetime.now().date()
    bb = datetime.timedelta(days=k)
    c = a+bb
    disc = {
        1: "Января",
        2: "Фервраля",
        3: "Марта",
        4: "Апреля",
        5: "Мая",
        6: "Июня",
        7: "Июля",
        8: "Августа",
        9: "Сентября",
        10: "Октября",
        11: "Ноября",
        12: "Декабря"
    }
    for i in disc:
        if i == c.month:
            return f'{c.day} {disc[i]}'


########################################################################################################################
###################СЕКРЕТНЫЕ КОМАНДЫ####################################################################################
########################################################################################################################

# Внесение пользователя в базу данных при команде старт
@dp.message_handler(commands='start')
async def start(message: types.Message):
    with open('players.json', encoding='utf-8') as f:
         new_dict = json.load(f)
    if f'{message.from_user.id}' in new_dict:
             await message.reply(f'Зравствуйте, {message.from_user.first_name}. Вы уже есть в нашей базе дынных.')
    else:
        new_dict[f'{message.from_user.id}'] = {
                 "user_id": message.from_user.id,
                 "first_name": message.from_user.first_name,
                 "last_name": message.from_user.last_name,
                 "username": message.from_user.username,
                 "willPlay": False,
                 "confirm": False,
                 "rate": 1,
             }
        await message.reply(f'Приятно познакомиться, {message.from_user.first_name}. Вы успешно добавлены в нашу базу данных!\nПрисоединяйтесь к нашей группе https://t.me/testBotfootball')
        with open('players.json', 'w', encoding="utf-8") as w:
            json.dump(new_dict, w, indent=4, ensure_ascii=False)

# Скачивание базы данных
@dp.message_handler(commands='json_send')
async def send_data(message: types.Message):
    file = open('players.json', 'rb')
    await bot.send_document(message.chat.id, file)
    file.close()

# Вывод списка участников по команде /list
@dp.message_handler(commands="list", commands_prefix="/!")
async def tell_me_players(message: types.Message):
    with open('players.json', encoding='utf-8') as f:
        list = []
        new_dict = json.load(f)

    s = 1
    for i in new_dict['all_players'].values():
        list.append(f'{s}.  {i}')
        s += 1
    l = len(new_dict['all_players'])
    k = 'Всего ' + str(l) + " игроков:\n\n" + ("\n".join(list))
    await bot.send_message(message.chat.id, k)

########################################################################################################################
###################КОМАНДЫ ДЛЯ ГРУППЫ###################################################################################
########################################################################################################################



# Первичная запись в список
@dp.message_handler(Text(equals='Хочу играть!'))
async def wantPlay(message: types.Message):
    start_buttons2 = ["Отказаться"]
    keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard2.add(*start_buttons2)
    with open('players.json', encoding='utf-8') as f:
        new_dict = json.load(f)
    if f'{message.from_user.id}' in new_dict:
        if f'{message.from_user.id}'in new_dict['all_players']:
            await message.reply('Вы уже записаны на предстоящую игру')
        else:
                new_dict[f'{message.from_user.id}']["willPlay"] = True
                new_dict['all_players'][f'{message.from_user.id}'] = message.from_user.first_name
                with open('players.json', 'w', encoding="utf-8") as w:
                    json.dump(new_dict, w, indent=4, ensure_ascii=False)
                await message.reply('Отлично! Записываю вас в список игроков.')
                await bot.send_message(message.from_user.id, 'Вы успешно записались на игру!!!\nУбедительно просим вас, в случае изменения ваших планов, уведомить нас, нажав кнопку отказа от игры. Благодарим за внимание.', reply_markup=keyboard2)

    else:
        new_dict['all_players'][f'{message.from_user.id}'] = message.from_user.first_name
        new_dict[f'{message.from_user.id}'] = {
                            "user_id": message.from_user.id,
                            "first_name": message.from_user.first_name,
                            "last_name": message.from_user.last_name,
                            "username": message.from_user.username,
                             "willPlay": True,
                             "confirm": False,
                            "rate": 1
                }
        with open('players.json', 'w', encoding="utf-8") as w:
            json.dump(new_dict, w, indent=4, ensure_ascii=False)
        await message.reply('Отлично! Записываю вас в список игроков.')
        await bot.send_message(message.from_user.id, 'Вы успешно записались на на игру!!!\nУбедительно просим вас, в случае изменения ваших планов, уведомить нас, нажав кнопку отказа от игры. Благодарим за внимание.', reply_markup=keyboard2)


# Подтверждение участия во время переклички
@dp.message_handler(Text(equals='Подтверждаю!'))
async def confirm(message: types.Message):

        with open('players.json', encoding='utf-8') as f:
            new_dict = json.load(f)
        if f'{message.from_user.id}' in new_dict:
            if f'{message.from_user.id}'in new_dict['all_players']:
                if new_dict[f'{message.from_user.id}']["willPlay"] == True and new_dict[f'{message.from_user.id}']["confirm"] == True:
                    await message.reply('Вы уже подтвердили ваше участие!')
                else:
                    new_dict[f'{message.from_user.id}']["willPlay"] = True
                    new_dict[f'{message.from_user.id}']["confirm"] = True
                    with open('players.json', 'w', encoding="utf-8") as w:
                        json.dump(new_dict, w, indent=4, ensure_ascii=False)
                    await message.reply('Отлично!Подтверждение принято!')
                    await bot.send_message(message.from_user.id,'Вы успешно <b>Подтвердили</b> участие в игре!!!\nУбедительно просим вас, в случае изменения ваших планов, уведомить нас, нажав соответствующую кнопку в <b>Группе</b>. Благодарим за внимание.')
            else:
                new_dict['all_players'][f'{message.from_user.id}'] = message.from_user.first_name
                new_dict[f'{message.from_user.id}']["willPlay"] = True
                new_dict[f'{message.from_user.id}']["confirm"] = True
                with open('players.json', 'w', encoding="utf-8") as w:
                    json.dump(new_dict, w, indent=4, ensure_ascii=False)
                await message.reply('Отлично!Вы успешно записались на завтрашнюю игру!')
                await bot.send_message(message.from_user.id,'Вы успешно <b>Подтвердили</b> участие в игре!!!\nУбедительно просим вас, в случае изменения ваших планов, уведомить нас, нажав соответствующую кнопку в <b>Группе</b>. Благодарим за внимание.')
        else:
            new_dict['all_players'][f'{message.from_user.id}'] = message.from_user.first_name
            new_dict[f'{message.from_user.id}'] = {
                            "user_id": message.from_user.id,
                            "first_name": message.from_user.first_name,
                            "last_name": message.from_user.last_name,
                            "username": message.from_user.username,
                             "willPlay": True,
                             "confirm": True,
                             "rate": 1
                }
            await message.reply('Отлично! Вы успешно записались на завтрашнюю игру!')
            await bot.send_message(message.from_user.id,'Вы успешно <b>Подтвердили</b> участие в игре!!!\nУбедительно просим вас, в случае изменения ваших планов, уведомить нас, нажав соответствующую кнопку в <b>Группе</b>. Благодарим за внимание.')
            with open('players.json', 'w', encoding="utf-8") as w:
                json.dump(new_dict, w, indent=4, ensure_ascii=False)



# Отказ от участия во время переклички.
@dp.message_handler(Text(equals='Не хочу играть!'))
async def reject(message: types.Message):

        with open('players.json', encoding='utf-8') as f:
            new_dict = json.load(f)
        if f'{message.from_user.id}' in new_dict:
            if f'{message.from_user.id}'in new_dict['all_players']:
                new_dict[f'{message.from_user.id}']["confirm"] = False
                new_dict[f'{message.from_user.id}']["willPlay"] = False
                del new_dict['all_players'][f'{message.from_user.id}']
                with open('players.json', 'w', encoding="utf-8") as w:
                    json.dump(new_dict, w, indent=4, ensure_ascii=False)
                await message.reply('Хорошо.До встречи на следующей неделе')
                await bot.send_message(message.from_user.id,'Ваш <b>отказ</b> от участия был принят!\nНо вы все еще можете присоединиться к игре, нажав соответствующую кнопку в <b>Группе</b> до <u>19:00</u>. Благодарим за внимание.')

            else:
                new_dict[f'{message.from_user.id}']["confirm"] = False
                new_dict[f'{message.from_user.id}']["willPlay"] = False
                with open('players.json', 'w', encoding="utf-8") as w:
                    json.dump(new_dict, w, indent=4, ensure_ascii=False)
                await message.reply('Вы не состоите в списке игроков этой недели.')
        else:
            new_dict[f'{message.from_user.id}'] = {
                            "user_id": message.from_user.id,
                            "first_name": message.from_user.first_name,
                            "last_name": message.from_user.last_name,
                            "username": message.from_user.username,
                             "willPlay": False,
                             "confirm": False,
                             "rate": 1
                }
            await message.reply('Вы не состоите в списке игроков этой недели.')
            with open('players.json', 'w', encoding="utf-8") as w:
                json.dump(new_dict, w, indent=4, ensure_ascii=False)



# Вывод списка участников по экранной кнопке
@dp.message_handler(Text(equals='Посмотреть список игроков'))
async def tell_me_playersHandler(message: types.Message):
        
        with open('players.json', encoding='utf-8') as f:
            list = []
            new_dict = json.load(f)
     
        s=1
        for i in new_dict['all_players'].values():
            list.append(f'{s}.  {i}')
            s+=1
        l = len(new_dict['all_players'])
        k = 'Всего ' + str(l) + " игроков:\n\n" + ("\n".join(list))
        await bot.send_message(message.chat.id,k)


########################################################################################################################
###################КОМАНДЫ ДЛЯ ЛИЧКИ####################################################################################
########################################################################################################################
# Отказ от участия.
@dp.message_handler(Text(equals="Отказаться"))
async def reject(message: types.Message):

        with open('players.json', encoding='utf-8') as f:
            new_dict = json.load(f)
        if f'{message.from_user.id}'in new_dict['all_players']:
            new_dict[f'{message.from_user.id}']["confirm"] = False
            new_dict[f'{message.from_user.id}']["willPlay"] = False
            del new_dict['all_players'][f'{message.from_user.id}']
            await message.reply('Хорошо.До встречи на следующей неделе.')
            user = message.from_user.first_name
            await bot.send_message(chat_id, f'Пользователь {user} отказался от участия в игре через личный чат.')
            with open('players.json', 'w', encoding="utf-8") as w:
                json.dump(new_dict, w, indent=4, ensure_ascii=False)
        else:
            await message.reply('Вы не состоите в списке игроков этой недели.')
            with open('players.json', 'w', encoding="utf-8") as w:
                json.dump(new_dict, w, indent=4, ensure_ascii=False)



########################################################################################################################
###################ТАЙМЕР###############################################################################################
########################################################################################################################

# Установка таймера на выполнение функций
async def timer():
    cicl1 = 0
    cicl2 = 0
    cicl3 = 0
    cicl4 = 0
    cicl5 = 0
    while True:

        if week_day() == 2 and hour_world() == 12 and cicl1 == 0:
        #if hour_world() == 10 and cicl1 == 0 or hour_world() == 15 and cicl1 == 0:
            cicl1 = 1
            cicl5 = 0
            start_buttons = ["Хочу играть!"]
            smart_buttons_add = ["Посмотреть список игроков"]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*start_buttons)
            keyboard.add(*smart_buttons_add)
            await bot.send_message(chat_id, f'Запись на игру в СУББОТУ {get_data(3)}. время игры с 07:30 до 09:00. Играем  1.5 часа. Собираемся в 07:00. Место игры Поле AZFAR Тарлан шадлыг еви архасы, 9 мкр.\nДля подтверждения нажмите на <b><u>вспомогательную кнопку</u></b>.', reply_markup=keyboard, parse_mode='html')
            stats = InlineKeyboardMarkup()
            stats.add(InlineKeyboardButton(f'Перейти', url='https://t.me/testBotfootball'))
            await bot.send_message(chat_id2,f"Не пропустите!!!\nЗапись на игру в СУББОТУ {get_data(3)}. Bремя игры с 07:30 до 09:00. Играем  1.5 часа. Собираемся в 07:00. Место игры Поле AZFAR Тарлан шадлыг еви архасы, 9 мкр.\nДля подтверждения нажмите на <b><u>вспомогательную кнопку</u></b>.",reply_markup=stats)



        elif week_day() == 4 and hour_world() == 12 and cicl2 == 0:
        #elif hour_world() == 11 and cicl2 == 0 or hour_world() == 16 and cicl2 == 0:
            cicl2 = 1
            cicl5 = 0
            start_buttons2 = ["Подтверждаю!", "Не хочу играть!"]
            smart_buttons_add = ["Посмотреть список игроков"]
            keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard2.add(*start_buttons2)
            keyboard2.add(*smart_buttons_add)
            await bot.send_message(chat_id, f'Просьба <b>подтвердить</b> участие в игре {get_data(1)}.\nДля подтверждения воспользуйтесь <b><u>вспомогательными кнопками</u></b>',reply_markup=keyboard2)
            stats = InlineKeyboardMarkup()  # СОЗДАЁМ ОСНОВУ ДЛЯ ИНЛАЙН КНОПКИ
            stats.add(InlineKeyboardButton(f'Перейти', url='https://t.me/testBotfootball'))
            await bot.send_message(chat_id2,f"Просьба <b>подтвердить</b> участие в игре {get_data(1)}.\nДля подтверждения воспользуйтесь <b><u>вспомогательными кнопками</u></b>", reply_markup=stats)

        elif week_day() == 4 and hour_world() == 16 and cicl3 == 0:
        #elif hour_world() == 12 and cicl3 == 0 or hour_world() == 17 and cicl3 == 0:
            cicl3 = 1
            with open('players.json', encoding='utf-8') as f:
                new_dict = json.load(f)
            for i in new_dict:
                if "willPlay" in new_dict[f'{i}']:
                    if new_dict[f'{i}']["willPlay"] != new_dict[f'{i}']["confirm"]:
                        await bot.send_message(chat_id,f'@{new_dict[i]["username"]}\n {new_dict[i]["first_name"]}, пожалуйста, подтвердите ваше участие.')

        elif week_day() == 4 and hour_world() == 19 and cicl4 == 0:
        #elif hour_world() == 13 and cicl4 == 0 or hour_world() == 18 and cicl4 == 0:
            cicl4 = 1
            cicl5 = 0
            start_buttons3 = ["Посмотреть список игроков"]
            keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard3.add(*start_buttons3)
            with open('players.json', encoding='utf-8') as f:
                new_dict = json.load(f)
            for i in new_dict:
                if "willPlay" in new_dict[f'{i}']:
                    if new_dict[f'{i}']["willPlay"] != new_dict[f'{i}']["confirm"]:
                        f = new_dict[i]['user_id']
                        print(str(f))
                        del new_dict['all_players'][str(f)]
            with open('players.json', 'w', encoding="utf-8") as w:
                json.dump(new_dict, w, indent=4, ensure_ascii=False)
            await bot.send_message(chat_id, 'Запись на игру на этой неделе окончена! Чтобы посмотреть список участников, нажмите на <b><u>вспомогательную кнопку</u></b>',reply_markup=keyboard3)
            with open('players.json', encoding='utf-8') as f:
                list = []
                new_dict = json.load(f)

            s = 1
            for i in new_dict['all_players'].values():
                list.append(f'{s}.  {i}')
                s += 1
            l = len(new_dict['all_players'])
            k = 'Всего ' + str(l) + " игроков:\n\n" + ("\n".join(list))
            await bot.send_message(chat_id2,f'Запись на игру на этой неделе <b>окончена</b>!\n {k}')

        elif week_day() == 5 and hour_world() == 12 and cicl5 == 0:
        #elif hour_world() == 14 and cicl2 == 1 or hour_world() == 19 and cicl2 == 1:
            cicl1 = 0
            cicl2 = 0
            cicl3 = 0
            cicl4 = 0
            cicl5 = 1
            with open('players.json', encoding='utf-8') as f:
                new_dict = json.load(f)
                for i in new_dict:
                    new_dict[i]['confirm'] = False
                    new_dict[i]['willPlay'] = False
                new_dict['all_players'] = {}

            with open('players.json', 'w', encoding="utf-8") as w:
                json.dump(new_dict, w, indent=4, ensure_ascii=False)
        await asyncio.sleep(10)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(timer())
    executor.start_polling(dp)


