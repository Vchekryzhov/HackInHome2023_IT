import sqlite3
import telebot
from telebot import types
#import config

bot = telebot.TeleBot("6944633884:AAGqYnI85VIRnq9DlR4AoiZ1O6pWAEm0y38")

conn = sqlite3.connect('Победа.db', check_same_thread=False)
cursor = conn.cursor()


def get_numbers():
    cursor.execute('SELECT Номер FROM JustAMoment')  # Здесь 'test' - это имя вашей таблицы в базе данных
    numbers = cursor.fetchall()  # Получаем все значения из столбца "номер"
    return [number[0] for number in numbers]  # Возвращаем список значений из столбца "номер"

def find_docs():
    pass

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Справка")
    btn2 = types.KeyboardButton("❓ Поиск")
    btn3 = types.KeyboardButton("✅ Добавить документ")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     text="Привет, я бот, который поможет тебе с поиском документов в базе данных", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "❓ Поиск"):
        bot.send_message(message.chat.id, text="Введите теги, тип документа, дату выхода, номер и тд.")
    elif (message.text == "👋 Справка"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как создать запрос в бд?")
        btn2 = types.KeyboardButton("Что этот бот умеет делать?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выберите интересующий вас вопрос из справки:", reply_markup=markup)
    elif (message.text == "✅ Добавить документ"):
        pass
    elif (message.text == "Как создать запрос в бд?"):
        bot.send_message(message.chat.id, "Нажмите поиск"
                                          " После этого введите свой запрос")

    elif (message.text == "Что этот бот умеет делать?"):
        bot.send_message(message.chat.id, text="Этот бот, умеет"
                                               " добавлять новые документы в базу данных"
                                               " и находить документ по запросу")

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Справка")
        button2 = types.KeyboardButton("❓ Поиск")
        button3 = types.KeyboardButton("✅ Добавить документ")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    elif message.text == "Показать номера":
        numbers = get_numbers()  # Получаем значения из столбца "номер"
        if numbers:
            bot.send_message(message.chat.id, text=f"Значения из столбца 'номер': {', '.join(map(str, numbers))}")
        else:
            bot.send_message(message.chat.id, text="Столбец 'номер' пуст.")
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.chat.id, 'Привет! Ваше имя добавлено в базу данных!')
#
#         us_id = message.from_user.id
#         us_name = message.from_user.first_name
#         us_sname = message.from_user.last_name
#         username = message.from_user.username
#
#         db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)


bot.polling(none_stop=True)