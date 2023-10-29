import sqlite3
import telebot
from telebot import types
import bcrypt

# 6944633884:AAGqYnI85VIRnq9DlR4AoiZ1O6pWAEm0y38
bot = telebot.TeleBot("6944633884:AAGqYnI85VIRnq9DlR4AoiZ1O6pWAEm0y38") 
conn = sqlite3.connect('C:\\Users\\Dmitriy Novichkov\\Desktop\\HackInHome 2023\\database.db',
                       check_same_thread=False)
cursor = conn.cursor()
cursor.execute('SELECT MAX(Indexes) FROM FirstOfAll')
max_index = cursor.fetchone()[0]

commands = ["❓ Поиск", "👋 Справка", "✅ Добавить документ", "🕹 Удалить ключ доступа", "📕 Тип", "📗 Название",
            "📘 Номер", "💾 Дата выхода", "💾 Дата ввода действия на предприятие", "📋 Ключевые слова",
            "💼 Добавить/изменить ключ доступа"]

key = ""
want_delete_it = False      # Подтверждает намерение удалить ключ доступа.
want_add_it = False         # Подтверждает намерение добавить ключ доступа.
want_add_it2 = False        # Подтверждает намерение добавить ключ доступа.
is_find = False

users_laws = dict()
admin_user_id = []
all_users_id = set()

salt = bcrypt.gensalt()

types_docs = ["ГОСТ (гос. Стандарт)", "РД (рук документ)", "Указ (президента)", "Постановление правительства",
              "СТО (стандарт организации)", "МИ (металогическая инструкция)", "РИ (Рабочая инструкция)",
              "Приказ (директора предприятия)", "Распоряжение директора предприятия)",
              "Уведомление (подразделений предприятия)", "Договор (между разными предприятиями)"]
win = bcrypt.hashpw('win'.encode(), salt)
winwin = bcrypt.hashpw('winwin'.encode(), salt)
access_levels = {win: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], winwin: [4, 2, 5]}
admin_password = bcrypt.hashpw('abswin'.encode(), salt)


def check_user(user_id, type_el):
    if user_id in admin_user_id:
        return True
    for el in access_levels[users_laws[user_id]]:
        if type_el == types_docs[el - 1]:
            return True
    return False


def searchByType(message, id_user):
    ind = -1
    for i in range(1, max_index + 1):
        cursor.execute('SELECT Type FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenatedResult = ''.join(str(item) for item in res[0]).lower()

        if message in concatenatedResult:
            ind = i
    global is_find
    is_find = False
    return ind


def searchByName(message):
    ind = -1
    for i in range(1, max_index + 1):
        cursor.execute('SELECT Name FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenatedResult = ' '.join(str(item) for item in res[0]).lower()
        if message in concatenatedResult:
            ind = i
    global is_find
    is_find = False
    return ind


def searchByNumber(message):
    ind = -1
    for i in range(1, max_index + 1):
        cursor.execute('SELECT Number FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenatedResult = ' '.join(str(item) for item in res[0]).lower()
        if message == concatenatedResult:
            ind = i
    global is_find
    is_find = False
    return ind


def searchByReleaseDate(message):
    ind = -1
    for i in range(1, max_index + 1):
        cursor.execute('SELECT ReleaseDate FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenatedResult = ' '.join(str(item) for item in res[0]).lower()
        if message == concatenatedResult:
            ind = i
    global is_find
    is_find = False
    return ind

def searchByStartDate(message):
    ind = -1
    for i in range(1, max_index + 1):
        cursor.execute('SELECT StartDate FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenatedResult = ' '.join(str(item) for item in res[0]).lower()
        if message == concatenatedResult:
            ind = i
    global is_find
    is_find = False
    return ind


def searchByKeyWords(message):
    ind = -1
    for i in range(1, max_index + 1):
        cursor.execute('SELECT KeyWords FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenatedResult = ' '.join(str(item) for item in res[0]).lower()
        if message in concatenatedResult:
            ind = i
    global is_find
    is_find = False
    return ind


@bot.message_handler(commands=['nevermind'])
def forget_me(message):
    if message.from_user.id in all_users_id:
        all_users_id.remove(message.from_user.id)
        if message.from_user.id in admin_user_id:
            admin_user_id.remove(message.from_user.id)
        if message.from_user.id in users_laws.keys():
            del users_laws[message.from_user.id]
        bot.send_message(message.chat.id, text='Данные о пользователе стёрты.')


def process_search_query(message, choice):
    search_query = message.text
    if (choice == "📕 Тип"):
        search_query = search_query.lower()
        resInd = searchByType(search_query, message.from_user.id)
        if (resInd >= 0):
            cursor.execute(
                'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                (resInd,))
            res = cursor.fetchall()
            res[0] = list(res[0])
            if check_user(message.from_user.id, res[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for i in res[0]:
                    i = i.replace("\n", " ")
                    bot.send_message(message.chat.id, text=i)
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif (choice == "📗 Название"):
        search_query = search_query.lower()
        resInd = searchByName(search_query)
        if (resInd != -1):
            bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
            cursor.execute(
                'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                (resInd,))
            res = cursor.fetchall()
            res[0] = list(res[0])
            if check_user(message.from_user.id, res[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for i in res[0]:
                    i = i.replace("\n", " ")
                    bot.send_message(message.chat.id, text=i)
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif (choice == "📘 Номер"):
        search_query = search_query.lower()
        resInd = searchByNumber(search_query)
        if (resInd != -1):
            cursor.execute(
                'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                (resInd,))
            res = cursor.fetchall()
            res[0] = list(res[0])
            if check_user(message.from_user.id, res[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for i in res[0]:
                    i = i.replace("\n", " ")
                    bot.send_message(message.chat.id, text=i)
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif (choice == "💾 Дата выхода"):
        search_query = search_query.lower()
        resInd = searchByReleaseDate(search_query)
        if (resInd != -1):
            cursor.execute(
                'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                (resInd,))
            res = cursor.fetchall()
            res[0] = list(res[0])
            if check_user(message.from_user.id, res[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for i in res[0]:
                    i = i.replace("\n", " ")
                    bot.send_message(message.chat.id, text=i)
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif (choice == "💾 Дата ввода действия на предприятие"):
        search_query = search_query.lower()
        resInd = searchByStartDate(search_query)
        if (resInd != -1):
            cursor.execute(
                'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                (resInd,))
            res = cursor.fetchall()
            res[0] = list(res[0])
            if check_user(message.from_user.id, res[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for i in res[0]:
                    i = i.replace("\n", " ")
                    bot.send_message(message.chat.id, text=i)
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif (choice == "📋 Ключевые слова"):
        search_query = search_query.lower()
        resInd = searchByKeyWords(search_query)
        if (resInd != -1):
            cursor.execute(
                'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                (resInd,))
            res = cursor.fetchall()
            res[0] = list(res[0])
            if check_user(message.from_user.id, res[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for i in res[0]:
                    i = i.replace("\n", " ")
                    bot.send_message(message.chat.id, text=i)
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")


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
    if message.from_user.id in users_laws.keys():
        bot.register_next_step_handler(message, func)
        func(message)

    else:  # Если нет, то требуем пароль.
        if bcrypt.hashpw(message.text.encode(), salt) in access_levels.keys():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("👋 Справка")
            btn2 = types.KeyboardButton("❓ Поиск")
            btn3 = types.KeyboardButton("✅ Добавить документ")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, text='Аутентификация пройдена.\n'
                                                   'Выберите один из предложенных вариантов:', reply_markup=markup)
            # В случае правильного ответа добавляем сотрудника в список разрешенных и переходим к следующей процедуре
            users_laws[message.from_user.id] = bcrypt.hashpw(message.text.encode(), salt)
            bot.register_next_step_handler(message, func)
        elif admin_password == bcrypt.hashpw(message.text.encode(), salt):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("👋 Справка")
            btn2 = types.KeyboardButton("❓ Поиск")
            btn3 = types.KeyboardButton("✅ Добавить документ")
            markup.add(btn1, btn2, btn3)
            button4 = types.KeyboardButton("🕹 Удалить ключ доступа")
            button5 = types.KeyboardButton("💼 Добавить/изменить ключ доступа")
            markup.add(button4, button5)
            bot.send_message(message.chat.id, text='Вы вошли в систему как администратор.\n'
                                                   'Выберите один из предложенных вариантов:', reply_markup=markup)
            users_laws[message.from_user.id] = "abswin"
            admin_user_id.append(message.from_user.id)
            bot.register_next_step_handler(message, func)
        else:
            if (message.from_user.id in all_users_id and bcrypt.hashpw(message.text.encode(), salt)
                    not in commands):
                bot.reply_to(message, 'Пароль неверный. Вы не прошли верификацию. Повторите попытку...')
            elif (bcrypt.hashpw(message.text.encode(), salt) in commands
                  and message.from_user.id in all_users_id):
                bot.reply_to(message, 'У вас нет прав доступа для использования этой команды. Введите пароль...')
            else:
                bot.reply_to(message, 'Начните беседу с ботом, использовав команду /start.')


@bot.message_handler(content_types=['text'])
def func(message):
    global want_add_it, key, want_delete_it, is_find, want_add_it2
    if message.text == "❓ Поиск":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("📕 Тип")
        btn2 = types.KeyboardButton("📗 Название")
        btn3 = types.KeyboardButton("📘 Номер")
        btn4 = types.KeyboardButton("💾 Дата выхода")
        btn5 = types.KeyboardButton("💾 Дата ввода действия на предприятие")
        btn6 = types.KeyboardButton("📋 Ключевые слова")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)
        bot.send_message(message.chat.id, text="Укажите, по какому столбцу Вы хотите вести поиск:", reply_markup=markup)

    elif message.text == "👋 Справка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как создать запрос в БД?")
        btn2 = types.KeyboardButton("Что этот бот умеет делать?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выберите интересующий вас вопрос из справки:", reply_markup=markup)
    elif message.text == "📕 Тип":
        is_find = True
        choice = "📕 Тип"
        bot.send_message(message.chat.id, text="Введите поисковый запрос")
        bot.register_next_step_handler(message, process_search_query, choice)
    elif message.text == "📗 Название":
        is_find = True
        choice = "📗 Название"
        bot.send_message(message.chat.id, text="Введите поисковый запрос")
        bot.register_next_step_handler(message, process_search_query, choice)
    elif message.text == "📘 Номер":
        is_find = True
        choice = "📘 Номер"
        bot.send_message(message.chat.id, text="Введите поисковый запрос")
        bot.register_next_step_handler(message, process_search_query, choice)
    elif message.text == "💾 Дата выхода":
        is_find = True
        choice = "💾 Дата выхода"
        bot.send_message(message.chat.id, text="Введите поисковый запрос")
        bot.register_next_step_handler(message, process_search_query, choice)
    elif message.text == "💾 Дата ввода действия на предприятие":
        is_find = True
        choice = "💾 Дата ввода действия на предприятие"
        bot.send_message(message.chat.id, text="Введите поисковый запрос")
        bot.register_next_step_handler(message, process_search_query, choice)
    elif message.text == "📋 Ключевые слова":
        is_find = True
        choice = "📋 Ключевые слова"
        bot.send_message(message.chat.id, text="Введите поисковый запрос")
        bot.register_next_step_handler(message, process_search_query, choice)
    elif message.text == "👋 Справка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как создать запрос в БД?")
        btn2 = types.KeyboardButton("Что этот бот умеет делать?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выберите интересующий вас вопрос из справки:", reply_markup=markup)
    elif message.text == "✅ Добавить документ":
        pass
    elif want_delete_it:
        want_delete_it = False
        key = bcrypt.hashpw(message.text.encode(), salt)
        if key in access_levels.keys():
            del access_levels[key]
            bot.send_message(message.chat.id, text='Код доступа был удалён.')
        else:
            bot.send_message(message.chat.id, text='Был указан неверный ключ доступа.')
    elif want_add_it:
        key = bcrypt.hashpw(message.text.encode(), salt)
        want_add_it = False
        want_add_it2 = True
        string = ""
        for i in range(len(types_docs)):
            string += str(i + 1) + ". " + types_docs[i] + "\n"
        bot.send_message(message.chat.id, text='Укажите, к каким типам документов будет иметь доступ. '
                                               'Введите через пробел числа, соответствующие индексам.\n' + string)
    elif want_add_it2:
        result = message.text.split()
        for i in range(len(result)):
            result[i] = int(result[i])
        access_levels[key] = result
        bot.send_message(message.chat.id, text="Ключ добавлен/изменён.")
        want_add_it2 = False
    elif message.text == "🕹 Удалить ключ доступа":
        if message.from_user.id not in admin_user_id:
            bot.send_message(message.chat.id, text="Ошибка! Вы не обладаете правами администратора.")
        else:
            bot.send_message(message.chat.id, text='Укажите удаляемый ключ доступа:')
            want_delete_it = True
    elif message.text == "💼 Добавить/изменить ключ доступа":
        if message.from_user.id not in admin_user_id:
            bot.send_message(message.chat.id, text="Ошибка! Вы не обладаете правами администратора.")
        else:
            bot.send_message(message.chat.id, text='Укажите ключ доступа:')
            want_add_it = True
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
            button4 = types.KeyboardButton("🕹 Удалить ключ доступа")
            button5 = types.KeyboardButton("💼 Добавить/изменить ключ доступа")
            markup.add(button4, button5)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню.", reply_markup=markup)
    else:
        if not is_find:
            bot.send_message(message.chat.id, text="Ошибка. Такой команды нет.")


bot.polling(none_stop=True)
