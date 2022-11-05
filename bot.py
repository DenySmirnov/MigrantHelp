import telebot
import sqlite3
import json
import botapi

from telebot import types

bot = botapi.key
con = sqlite3.connect("user.db", check_same_thread=False)
cur = con.cursor()
keyboard = types.InlineKeyboardMarkup()
home_site_button = types.InlineKeyboardButton(text="Перейти", url="https://www.olx.ua/uk/dopomoga/proponuiu_dopomohu/zhytlo/")
work_site_button = types.InlineKeyboardButton(text="Перейти", url="https://www.olx.ua/d/uk/rabota/q-%D0%BF%D0%B5%D1%80%D0%B5%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D1%86%D1%8B/")
keyboard.add(home_site_button)

@bot.message_handler(commands=['chatid'])
def chatid(message):
    cid = message.chat.id
    bot.reply_to(message, f'{cid}')
@bot.message_handler(commands=['banuser'])
def ban(message):
    user_id = str(message.chat.id)
    if(user_id == '1204588707'):
        bot.send_message(message.chat.id, text="ID юзера".format(message.from_user))
        @bot.message_handler(content_types=['text'])
        def func(message):
            userforban = message.text
            checkban = cur.execute(f"SELECT id FROM user WHERE id = {userforban}")
            if checkban.fetchone() != None:
                cur.execute(f"UPDATE user SET last_menu = 'banned' WHERE id = '{userforban}'")
                con.commit()
                bot.send_message(message.chat.id, text="Юзера послано за корабльом🛳".format(message.from_user))
            else:
                bot.send_message(message.chat.id, text="Юзера не існує".format(message.from_user))
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    check = cur.execute(f"SELECT id FROM user WHERE id = {user_id}")
    if check.fetchone() == None:
        cur.execute(f"""
            INSERT INTO user VALUES
                ({user_id}, '0', '0', 'start')
            """)
        con.commit()
    checkban = cur.execute(f"SELECT last_menu FROM user WHERE id = {user_id}")
    checkban = str(checkban.fetchone()[0])
    if(checkban == 'banned'):
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text="За багаточислені скарги зі сторони волонтерів Вас послано за корабльом🛳".format(message.from_user), reply_markup = a)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        home_need = types.KeyboardButton("🏠 Потрібне житло")
        work_need = types.KeyboardButton("🛠 Потрібна робота")
        food_need = types.KeyboardButton("👕 Потрібні речі/їжа")
        human_search = types.KeyboardButton("👨‍🦰 Зникла людина")
        help_center = types.KeyboardButton("🆘 Центри допомоги")
        settings = types.KeyboardButton("⚙️ Налаштування")
        markup.add(home_need, work_need, food_need)
        markup.add(human_search, help_center)
        markup.add(settings)
        bot.send_message(message.chat.id, text="Вітаю, {0.first_name}!👋\nЦе тестовий бот-помічник для переселенців в Україні.\nДля навігації скористуйтеся меню нижче:".format(message.from_user), reply_markup = markup)
        cur.execute(f"""UPDATE user SET last_menu = 'start' WHERE id = {user_id}""")
        con.commit()
@bot.message_handler(content_types=['text'])
def func(message):
    user_id = message.chat.id
    if(message.text == "🏠 Потрібне житло"):
        b = "()',.?"
        #for char in b:
        #    text = text.replace(char, "")
        cur.execute(f"UPDATE user SET last_menu = 'home_need' WHERE id = {user_id}")
        con.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        home_site = types.KeyboardButton("🏠 Відвідати сайт")
        home_create = types.KeyboardButton("🏠 Заповнити форму")
        back = types.KeyboardButton ("🔙 Назад")
        markup.add(home_site, home_create, back)
        bot.send_message(message.chat.id, text="Ви можете знайти собі житло:\n1.На сайті OLX в розділі допомоги з житлом\n2.На сайтах з пошуку житла\n3.Створити форму з запитом на житло в нашому каналі".format(message.from_user), reply_markup=markup)
    if(message.text == "🏠 Відвідати сайт"):
        bot.send_message(message.chat.id, "Для перегляду варіантів натисніть кнопку нижче", reply_markup=keyboard)
    if(message.text == "🔙 Назад"):
        cur.execute(f"UPDATE user SET last_menu = 'start' WHERE id = {user_id}")
        con.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        home_need = types.KeyboardButton("🏠 Потрібне житло")
        work_need = types.KeyboardButton("🛠 Потрібна робота")
        food_need = types.KeyboardButton("👕 Потрібні речі/їжа")
        human_search = types.KeyboardButton("👨‍🦰 Зникла людина")
        help_center = types.KeyboardButton("🆘 Центри допомоги")
        settings = types.KeyboardButton("⚙️ Налаштування")
        markup.add(home_need, work_need, food_need)
        markup.add(human_search, help_center)
        markup.add(settings)
        bot.send_message(message.chat.id, text="Вітаю, {0.first_name}!👋\nЦе тестовий бот-помічник для переселенців в Україні.\nДля навігації скористуйтеся меню нижче:".format(message.from_user), reply_markup=markup)
    if(message.text == "🏠 Заповнити форму"):
        a = telebot.types.ReplyKeyboardRemove()
        b = "()',.?"
        #for char in b:
        #    text = text.replace(char, "")
        cur.execute(f"UPDATE user SET last_menu = 'home_form' WHERE id = {user_id}")
        con.commit()
        bot.send_message(message.chat.id, text="Запит на пошук житла буде створений та розміщений в нашому каналі\nАле для початку скажіть наступне:".format(message.from_user), reply_markup = a)
        check1 = cur.execute(f"SELECT city_from FROM user WHERE id = {user_id}")
        check1 = str(check1.fetchone()[0])
        #for check1 in b:
            #checknew = check1.replace(check1, "")
        if check1 == '0':
            cur.execute(f"UPDATE user SET last_menu = 'city_from' WHERE id = {user_id}")
            con.commit()
            bot.send_message(message.chat.id, text="З якого Ви приїхали міста (Наприклад: Ірпінь, Маріуполь і тд.)".format(message.from_user))
        else:
            check2 = cur.execute(f"SELECT city_to FROM user WHERE id = {user_id}")
            check2 = str(check2.fetchone()[0])
            if check2 == '0':
                cur.execute(f"UPDATE user SET last_menu = 'city_to' WHERE id = {user_id}")
                con.commit()
                bot.send_message(message.chat.id, text="В якому Ви шукаєте допомогу (Наприклад: Київ, Львів і тд.)".format(message.from_user))
            else:
                cur.execute(f"UPDATE user SET last_menu = 'number_people' WHERE id = {user_id}")
                bot.send_message(message.chat.id, text="На скільки чоловік Вам потрібне житло?".format(message.from_user))
    if(message.text == "⚙️ Налаштування"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        changeCityFrom = types.KeyboardButton("⚙️ Змінити місто звідки Ви")
        changeCityTo = types.KeyboardButton("⚙️ Змінити місто де Ви зараз")
        back = types.KeyboardButton ("🔙 Назад")
        markup.add(changeCityFrom)
        markup.add(changeCityTo)
        markup.add(back)
        bot.send_message(message.chat.id, text="Тут Ви можете змінити місто звідки і де Ви:".format(message.from_user), reply_markup=markup)
    if(message.text == "🛠 Потрібна робота"):
        b = "()',.?"
        #for char in b:
        #    text = text.replace(char, "")
        cur.execute(f"UPDATE user SET last_menu = 'work_need' WHERE id = {user_id}")
        con.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        work_site = types.KeyboardButton("🛠 Відвідати сайт")
        work_create = types.KeyboardButton("🛠 Заповнити форму")
        back = types.KeyboardButton ("🔙 Назад")
        markup.add(work_site, work_create, back)
        bot.send_message(message.chat.id, text="Ви можете знайти собі роботу:\n1.На сайті OLX в розділі 'Робота'\n2.В центрі зайнятості міста, в якому Ви перебуваєте\n3.Створити форму з запитом на роботу в нашому каналі".format(message.from_user), reply_markup=markup)
    if(message.text == "🛠 Відвідати сайт"):
        bot.send_message(message.chat.id, "Для перегляду варіантів натисніть кнопку нижче", reply_markup=keyboard(work_site_button))
    if(message.text == "⚙️ Змінити місто звідки Ви"):
        check1 = cur.execute(f"SELECT city_from FROM user WHERE id = {user_id}")
        check1 = str(check1.fetchone()[0])
        bot.send_message(message.chat.id, text=f"Ваше місто, з якого Ви було записано як: {check1}\nВведіть нове місто:".format(message.from_user))
        cur.execute(f"UPDATE user SET last_menu = 'changeFrom' WHERE id = {user_id}")
    if(message.text == "⚙️ Змінити місто де Ви зараз"):
        check2 = cur.execute(f"SELECT city_to FROM user WHERE id = {user_id}")
        check2 = str(check2.fetchone()[0])
        bot.send_message(message.chat.id, text=f"Ваше місто, в якому Ви було записано як: {check2}\nВведіть нове місто:".format(message.from_user))
        cur.execute(f"UPDATE user SET last_menu = 'changeTo' WHERE id = {user_id}")
    else:
        #bot.send_message(message.chat.id, text="In progress🛠🛠🛠")
        b = "()',.?"
        checkAnswer = cur.execute(f"SELECT last_menu FROM user WHERE id = {user_id}")
        checkAnswer = str(checkAnswer.fetchone()[0])
        con.commit()
        if(checkAnswer == 'city_from'):
            a = telebot.types.ReplyKeyboardRemove()
            city_from = message.text
            bot.send_message(message.chat.id, text=f"Місто з якого Ви записано: {city_from}".format(message.from_user), reply_markup = a)
            cur.execute(f"UPDATE user SET city_from = '{city_from}' WHERE id = {user_id}")
            con.commit()
            check2 = cur.execute(f"SELECT city_to FROM user WHERE id = {user_id}")
            check2 = str(check2.fetchone()[0])
            if check2 == '0':
                cur.execute(f"UPDATE user SET last_menu = 'city_to' WHERE id = {user_id}")
                con.commit()
                bot.send_message(message.chat.id, text="В якому Ви шукаєте допомогу (Наприклад: Київ, Львів і тд.)".format(message.from_user))
        if(checkAnswer == 'city_to'):
            a = telebot.types.ReplyKeyboardRemove()
            city_to = message.text
            bot.send_message(message.chat.id, text=f"Місто з якого Ви записано: {city_to}".format(message.from_user), reply_markup = a)
            cur.execute(f"UPDATE user SET city_to = '{city_to}' WHERE id = {user_id}")
            con.commit()
            cur.execute(f"UPDATE user SET last_menu = 'number_people' WHERE id = {user_id}")
            bot.send_message(message.chat.id, text="На скільки чоловік Вам потрібне житло?".format(message.from_user))
        if(checkAnswer == 'number_people'):
            a = telebot.types.ReplyKeyboardRemove()
            global number_people, final_text
            number_people = message.text
            user_username = message.from_user.username
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            home_form_yes = types.KeyboardButton("Так")
            home_form_no = types.KeyboardButton("Ні")
            markup.add(home_form_yes)
            markup.add(home_form_no)
            global text_home_help
            city_to = cur.execute(f"SELECT city_to FROM user WHERE id = {user_id}")
            city_to = str(city_to.fetchone()[0])
            text_home_help = f"Нам потрібне житло!🏠\nМісто: {city_to}\nКількість чоловік: {number_people}\nЗвертатися до: @{user_username}"
            bot.send_message(message.chat.id, text='Повідомлення матиме наступний вигляд, надіслати?'.format(message.from_user), reply_markup=markup)
            bot.send_message(message.chat.id, text=text_home_help.format(message.from_user), reply_markup=markup)
            cur.execute(f"UPDATE user SET last_menu = 'send yn' WHERE id = {user_id}")
            con.commit()
        if(checkAnswer == 'send yn'):
            if(message.text == "Так"):
                print(text_home_help)
                bot.send_message(-826924649, text=text_home_help)
            if(message.text == "Ні"):
                bot.send_message(message.chat.id, text="Введення даних скасовано\nТакі дані як міста були записані, якщо Ви не робили це раніше".format(message.from_user))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            home_need = types.KeyboardButton("🏠 Потрібне житло")
            work_need = types.KeyboardButton("🛠 Потрібна робота")
            food_need = types.KeyboardButton("👕 Потрібні речі/їжа")
            human_search = types.KeyboardButton("👨‍🦰 Зникла людина")
            help_center = types.KeyboardButton("🆘 Центри допомоги")
            settings = types.KeyboardButton("⚙️ Налаштування")
            markup.add(home_need, work_need, food_need)
            markup.add(human_search, help_center)
            markup.add(settings)
            bot.send_message(message.chat.id, text="Ви повернулися до меню".format(message.from_user), reply_markup = markup)
        if(checkAnswer == 'changeFrom'):
            newCityFrom = message.text
            bot.send_message(message.chat.id, text=f"Місто змінено: {newCityFrom}".format(message.from_user))
            cur.execute(f"UPDATE user SET city_from = '{newCity}' WHERE id = {user_id}")
            con.commit()
        if(checkAnswer == 'changeTo'):
            newCity = message.text
            bot.send_message(message.chat.id, text=f"Місто змінено: {newCity}".format(message.from_user))
            cur.execute(f"UPDATE user SET city_to = '{newCity}' WHERE id = {user_id}")
            con.commit()

        #else:
            #check = cur.execute(f"SELECT last_menu FROM user WHERE id = {user_id}")
            #check = str(cur.fetchone())
            #for char in b:
                #check = check.replace(char, "")
            #print(check)
            #if(check == "0"):
                #bot.send_message(message.chat.id, text="Бот був на доробці через що був зупинений🛠\nПропишіть заново команду /start".format(message.from_user))

bot.infinity_polling()
