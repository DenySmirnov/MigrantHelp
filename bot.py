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
keyboard.add(home_site_button)

@bot.message_handler(commands=['chatid'])
def chatid(message):
    cid = message.chat.id
    bot.reply_to(message, f'{cid}')
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    check = cur.execute(f"SELECT id FROM user WHERE id = {user_id}")
    if check.fetchone() == None:
        cur.execute(f"""
            INSERT INTO user VALUES
                ({user_id}, '{0}', '{0}', 'start')
            """)
        con.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    home_need = types.KeyboardButton("🏠 Потрібне житло")
    work_need = types.KeyboardButton("🛠 Потрібна робота")
    food_need = types.KeyboardButton("👕 Потрібні речі/їжа")
    human_search = types.KeyboardButton("👨‍🦰 Зникла людина")
    help_center = types.KeyboardButton("🆘 Центри допомоги")
    markup.add(home_need, work_need, food_need)
    markup.add(human_search, help_center)
    bot.send_message(message.chat.id, text="Вітаю, {0.first_name}!👋\nЦе тестовий бот-помічник для переселенців в Україні.\nДля навігації скористуйтеся меню нижче:".format(message.from_user), reply_markup = markup)
    cur.execute(f"""UPDATE user SET last_menu = 'start' WHERE id = {user_id}""")
    con.commit()
    @bot.message_handler(content_types=['text'])
    def func(message):
        if(message.text == "🏠 Потрібне житло"):
            b = "()',.?"
            text = message.text
            #for char in b:
            #    text = text.replace(char, "")
            cur.execute(f"UPDATE user SET last_menu = '{text}' WHERE id = {user_id}")
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
            cur.execute(f"UPDATE user SET last_menu = '{message.text}' WHERE id = {user_id}")
            con.commit()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            home_need = types.KeyboardButton("🏠 Потрібне житло")
            work_need = types.KeyboardButton("🛠 Потрібна робота")
            food_need = types.KeyboardButton("👕 Потрібні речі/їжа")
            human_search = types.KeyboardButton("👨‍🦰 Зникла людина")
            help_center = types.KeyboardButton("🆘 Центри допомоги")
            markup.add(home_need, work_need, food_need)
            markup.add(human_search, help_center)
            bot.send_message(message.chat.id, text="Вітаю, {0.first_name}!👋\nЦе тестовий бот-помічник для переселенців в Україні.\nДля навігації скористуйтеся меню нижче:".format(message.from_user), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text="In progress🛠🛠🛠")

#типу є зміни лол))
        #else:
            #check = cur.execute(f"SELECT last_menu FROM user WHERE id = {user_id}")
            #check = str(cur.fetchone())
            #for char in b:
                #check = check.replace(char, "")
            #print(check)
            #if(check == "0"):
                #bot.send_message(message.chat.id, text="Бот був на доробці через що був зупинений🛠\nПропишіть заново команду /start".format(message.from_user))

bot.infinity_polling()
