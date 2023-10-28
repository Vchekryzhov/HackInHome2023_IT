import sqlite3
import telebot
from telebot import types
from Levenshtein import distance as lev

bot = telebot.TeleBot("6944633884:AAGqYnI85VIRnq9DlR4AoiZ1O6pWAEm0y38") 
conn = sqlite3.connect('C:\\Users\\Dmitriy Novichkov\\Desktop\\HackInHome 2023\\database.db', #'C:\\Users\\Sam\\PycharmProjects\\SamProject\\database.db',
                       check_same_thread=False)
cursor = conn.cursor()
cursor.execute('SELECT MAX(Indexes) FROM FirstOfAll')
max_index = cursor.fetchone()[0]

commands = ["❓ Поиск", "👋 Справка", "✅ Добавить документ", "🕹 Сменить пароль", "📕 Тип", "📗 Название",
            "📘 Номер", "💾 Дата выхода", "💾 Дата ввода действия на предприятие", "📋 Ключевые слова", "📒 Индекс"]

want_change_it = False      # Подтверждает намерение изменить пароль.

allowed_user_id = []        # база пользователей которым разрешен доступ
admin_user_id = []
all_users_id = set()
password = "win"
admin_password = "abswin"


def search(message):
    NUMBER_OF_ERRORS = float("inf")
    iterator = 0
    message = message.lower()
    newResult = ''  # Обнуляем newResult перед началом поиска
    for i in range(1, max_index + 1):
        cursor.execute('SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?', (i,))
        res = cursor.fetchall()

        tmpResult = concatenatedResult = ' '.join(str(item) for item in res[0])
        concatenatedResult = concatenatedResult.lower()
        minErrors = lev(message, concatenatedResult)
        if NUMBER_OF_ERRORS > minErrors:
            NUMBER_OF_ERRORS = minErrors
            iterator = i
            newResult = tmpResult  # Сохраняем новый результат, если он ближе
    return iterator, newResult


def search_type(message):
    NUMBER_OF_ERRORS = float("inf")
    iterator = 0
    message = message.lower()
    newResult = ''  # Обнуляем newResult перед началом поиска
    for i in range(1, max_index + 1):
        cursor.execute('SELECT Type FROM FirstOfAll WHERE Indexes = ?', (i,))
        res = cursor.fetchall()

        tmpResult = concatenatedResult = ' '.join(str(item) for item in res[0])
        concatenatedResult = concatenatedResult.lower()
        minErrors = lev(message, concatenatedResult)
        if NUMBER_OF_ERRORS > minErrors:
            NUMBER_OF_ERRORS = minErrors
            iterator = i
            newResult = tmpResult  # Сохраняем новый результат, если он ближе
    return iterator, newResult


#@bot.message_handler(content_types=['text'])
def get_it_for_find(message):
    bot.send_message(message.chat.id, text="Что Вы ищете:")
    global search_query
    search_query = message.text


def process_search_query(message):
    first_message = message.text
    global search_query
    search_query = ""
    bot.register_next_step_handler(message, get_it_for_find)

    if first_message == "📒 Индекс":
        pass
    elif first_message == "📕 Тип":
        it, resStr = search_type(search_query)
    elif first_message == "📗 Название":
        pass
    elif first_message == "📘 Номер":
        pass
    elif first_message == "💾 Дата выхода":
        pass
    elif first_message == "💾 Дата ввода действия на предприятие":
        pass
    elif first_message == "📋 Ключевые слова":
        pass

    bot.send_message(message.chat.id, text="Возможно, Вы имели в виду:\n")
    #bot.send_message(message.chat.id, text=resStr)


def get_numbers():
    cursor.execute('SELECT Number FROM FirstOfAll')  # Здесь 'test' - это имя вашей таблицы в базе данных
    numbers = cursor.fetchall()  # Получаем все значения из столбца "номер"
    return [number[0] for number in numbers]  # Возвращаем список значений из столбца "номер"


@bot.message_handler(commands=['nevermind'])
def forget_me(message):
    if message.from_user.id in all_users_id:
        all_users_id.remove(message.from_user.id)
        if message.from_user.id in admin_user_id:
            admin_user_id.remove(message.from_user.id)
        if message.from_user.id in allowed_user_id:
            allowed_user_id.remove(message.from_user.id)
        bot.send_message(message.chat.id, text='Данные о пользователе стёрты.')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text="Здравствуйте, я бот, который поможет Вам с поиском документов в БД.\n"
                          "Для начала пройдите аутентификацию. Введите пароль...")
    all_users_id.add(message.from_user.id)
    bot.register_next_step_handler(message, authentication)


@bot.message_handler(content_types=['text'])
def authentication(message):

    # Если пользователь есть в базе разрешенных пользователей, то переходим к процедуре общения с ним.
    if message.from_user.id in allowed_user_id:
        bot.register_next_step_handler(message, func)
        func(message)

    else:  # Если нет, то требуем пароль.
        if password == message.text:  # Наш пароль с маленькой или большой буквы
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("👋 Справка")
            btn2 = types.KeyboardButton("❓ Поиск")
            btn3 = types.KeyboardButton("✅ Добавить документ")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, text='Аутентификация пройдена.\n'
                                                   'Выберите один из предложенных вариантов:', reply_markup=markup)
            # В случае правильного ответа добавляем сотрудника в список разрешенных и переходим к следующей процедуре
            allowed_user_id.append(message.from_user.id)
            bot.register_next_step_handler(message, func)
        elif admin_password == message.text:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("👋 Справка")
            btn2 = types.KeyboardButton("❓ Поиск")
            btn3 = types.KeyboardButton("✅ Добавить документ")
            markup.add(btn1, btn2, btn3)
            button4 = types.KeyboardButton("🕹 Сменить пароль")
            markup.add(button4)
            bot.send_message(message.chat.id, text='Вы вошли в систему как администратор.\n'
                                                   'Выберите один из предложенных вариантов:', reply_markup=markup)
            allowed_user_id.append(message.from_user.id)
            admin_user_id.append(message.from_user.id)
            bot.register_next_step_handler(message, func)
        else:
            if message.from_user.id in all_users_id and message.text not in commands:
                bot.reply_to(message, 'Пароль неверный. Вы не прошли верификацию. Повторите попытку...')
            elif message.text in commands and message.from_user.id in all_users_id:
                bot.reply_to(message, 'У вас нет прав доступа для использования этой команды. Введите пароль...')
            else:
                bot.reply_to(message, 'Начните беседу с ботом, использовав команду /start.')


@bot.message_handler(content_types=['text'])
def change_password(message):
    global  want_change_it
    if want_change_it:
        global password
        password = message.text
        bot.send_message(message.chat.id, text='Пароль был сменён.')
        want_change_it = False


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "❓ Поиск":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("📒 Индекс")
        btn2 = types.KeyboardButton("📕 Тип")
        btn3 = types.KeyboardButton("📗 Название")
        btn4 = types.KeyboardButton("📘 Номер")
        btn5 = types.KeyboardButton("💾 Дата выхода")
        btn6 = types.KeyboardButton("💾 Дата ввода действия на предприятие")
        btn7 = types.KeyboardButton("📋 Ключевые слова")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7,back)
        bot.send_message(message.chat.id, text="Укажите, по какому столбцу Вы хотите вести поиск:", reply_markup=markup)

        bot.register_next_step_handler(message, process_search_query)

    elif message.text == "👋 Справка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как создать запрос в БД?")
        btn2 = types.KeyboardButton("Что этот бот умеет делать?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выберите интересующий вас вопрос из справки:", reply_markup=markup)
    elif message.text == "✅ Добавить документ":
        pass
    elif message.text == "🕹 Сменить пароль":
        if message.from_user.id not in admin_user_id:
            bot.send_message(message.chat.id, text="Ошибка! Вы не обладаете правами администратора.")
        else:
            bot.send_message(message.chat.id, text="Введите новый пароль для входа пользователей:")
            global want_change_it
            want_change_it = True
            bot.register_next_step_handler(message, change_password)
    elif message.text == "Как создать запрос в БД?":
        bot.send_message(message.chat.id, "Нажмите поиск"
                                          " После этого введите свой запрос")

    elif message.text == "Что этот бот умеет делать?":
        bot.send_message(message.chat.id, text="Этот бот умеет"
                                               " добавлять новые документы в базу данных"
                                               " и находить документ по запросу")

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Справка")
        button2 = types.KeyboardButton("❓ Поиск")
        button3 = types.KeyboardButton("✅ Добавить документ")
        markup.add(button1, button2, button3)
        if message.from_user.id in admin_user_id:
            button4 = types.KeyboardButton("🕹 Сменить пароль")
            markup.add(button4)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    elif message.text == "Показать номера":
        numbers = get_numbers()  # Получаем значения из столбца "номер"
        if numbers:
            bot.send_message(message.chat.id, text=f"Значения из столбца 'номер': {', '.join(map(str, numbers))}")
        else:
            bot.send_message(message.chat.id, text="Столбец 'номер' пуст.")
    else:
        bot.send_message(message.chat.id, text="Ошибка. Такой команды нет.")


bot.polling(none_stop=True)
