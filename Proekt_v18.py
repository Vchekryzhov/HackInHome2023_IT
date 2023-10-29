import sqlite3
import telebot
from telebot import types
import bcrypt
import pandas as pd
import os
import re
import openpyxl

# 6944633884:AAGqYnI85VIRnq9DlR4AoiZ1O6pWAEm0y38
bot = telebot.TeleBot("6944633884:AAGqYnI85VIRnq9DlR4AoiZ1O6pWAEm0y38")
conn = sqlite3.connect('C:\\Users\\Dmitriy Novichkov\\Desktop\\HackInHome 2023\\database.db',
                       check_same_thread=False)
cursor = conn.cursor()
cursor.execute('SELECT MAX(Indexes) FROM FirstOfAll')
max_index = cursor.fetchone()[0]

commands = ["❓ Поиск", "👋 Справка", "📲 Добавить документ", "🕹 Удалить ключ доступа", "📕 Тип", "📗 Название",
            "📘 Номер", "💾 Дата выхода", "💾 Дата ввода действия на предприятие", "📋 Ключевые слова",
            "💼 Добавить/изменить ключ доступа", "📩 Извлечь таблицу", "✅ Документы"]

key = ""  # Хранит промежуточное значение для алгоритма добавления/редактирования и алгоритма удаления ключа.
want_delete_it = False  # Подтверждает намерение удалить ключ доступа.
want_add_it = False  # Подтверждает намерение добавить ключ доступа.
want_add_it2 = False  # Подтверждает намерение добавить ключ доступа.
want_add_doc = False  # Подтверждает намерение добавить документ.
want_change_doc = False  # Подтверждает намерение изменить документ.
is_find = False  # Ищем мы что-то или нет.

lst_mgs = []  # Список для хранения всех сообщений для вывода поиска.
lst_idx = []  # Список для хранения всех индексов сообщений для вывода поиска.

users_laws = dict()  # Пользователи и их ключ доступа.
admin_user_id = []  # Пользователи-админы.
all_users_id = set()  # Все пользователи.

salt = bcrypt.gensalt()  # "Соль" для добавления в алгоритмы хеширования.

# Переменная содержит вообще все типы документов. Пока что добавление здесь новых типов документов не предусмотрено.
# Нужно для определения, кто какой доступ имеет.
types_docs = ["ГОСТ (гос. Стандарт)", "РД (рук документ)", "Указ (президента)", "Постановление правительства",
              "СТО (стандарт организации)", "МИ (металогическая инструкция)", "РИ (Рабочая инструкция)",
              "Приказ (директора предприятия)", "Распоряжение директора предприятия)",
              "Уведомление (подразделений предприятия)", "Договор (между разными предприятиями)"]

win = bcrypt.hashpw('win'.encode(), salt)  # Создаём тестовый ключ доступа.
winwin = bcrypt.hashpw('winwin'.encode(), salt)  # Создаём тестовый ключ доступа.
access_levels = {win: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], winwin: [4, 2, 5]}  # Ключи доступа и их возможности.
admin_password = bcrypt.hashpw('abswin'.encode(), salt)  # Создаём ключ админа. Тестовый.


def date_is_valid(message):
    date_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
    if re.match(date_pattern, message):
        return True


def number_is_valid(message):
    for i in range(0, 10):
        if str(i) in message:
            return True


def check_user(user_id, type_el):
    if user_id in admin_user_id:
        return True
    for el in access_levels[users_laws[user_id]]:
        if type_el == types_docs[el - 1]:
            return True
    return False


def search_by_type(message):
    for i in range(1, max_index + 1):
        cursor.execute('SELECT Type FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenated_result = ''.join(str(item) for item in res[0]).lower()

        if message in concatenated_result:
            lst_idx.append(int(i))
    global is_find
    is_find = False


def search_by_name(message):
    for i in range(1, max_index + 1):
        cursor.execute('SELECT Name FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenated_result = ' '.join(str(item) for item in res[0]).lower()

        if message in concatenated_result:
            lst_idx.append(int(i))
    global is_find
    is_find = False


def search_by_number(message):
    for i in range(1, max_index + 1):
        cursor.execute('SELECT Number FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenated_result = ' '.join(str(item) for item in res[0]).lower()
        if message == concatenated_result:
            lst_idx.append(int(i))
    global is_find
    is_find = False


def search_by_release_date(message):
    for i in range(1, max_index + 1):
        cursor.execute('SELECT ReleaseDate FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenated_result = ' '.join(str(item) for item in res[0]).lower()
        if message == concatenated_result:
            lst_idx.append(int(i))
    global is_find
    is_find = False


def search_by_start_date(message):
    for i in range(1, max_index + 1):
        cursor.execute('SELECT StartDate FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenated_result = ' '.join(str(item) for item in res[0]).lower()
        if message == concatenated_result:
            lst_idx.append(int(i))
    global is_find
    is_find = False


def search_by_key_words(message):
    for i in range(1, max_index + 1):
        cursor.execute('SELECT KeyWords FROM FirstOfAll WHERE Indexes = ?',
                       (i,))
        res = cursor.fetchall()

        concatenated_result = ' '.join(str(item) for item in res[0]).lower()
        if message in concatenated_result:
            lst_idx.append(int(i))
    global is_find
    is_find = False


def process_search_query(message, choice):
    search_query = message.text
    if choice == "📕 Тип":
        search_query = search_query.lower()
        search_by_type(search_query)
        if len(lst_idx) > 0:
            for i in lst_idx:
                cursor.execute(
                    'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                    (i,))
                mgs = cursor.fetchall()
                mgs = list(mgs[0])
                lst_mgs.append(mgs)
            if check_user(message.from_user.id, lst_mgs[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for el in range(len(lst_mgs)):
                    for i in range(len(lst_mgs[el])):
                        lst_mgs[el][i] = lst_mgs[el][i].replace("\n", " ")
                    bot.send_message(message.chat.id, text=str(lst_idx[el]) + ". " + "\n".join(lst_mgs[el]))
                lst_mgs.clear()
                lst_idx.clear()
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif choice == "📗 Название":
        search_query = search_query.lower()
        search_by_name(search_query)
        if len(lst_idx) > 0:
            for i in lst_idx:
                cursor.execute(
                    'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                    (i,))
                mgs = cursor.fetchall()
                mgs = list(mgs[0])
                lst_mgs.append(mgs)
            if check_user(message.from_user.id, lst_mgs[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for el in range(len(lst_mgs)):
                    for i in range(len(lst_mgs[el])):
                        lst_mgs[el][i] = lst_mgs[el][i].replace("\n", " ")
                    bot.send_message(message.chat.id, text=str(lst_idx[el]) + ". " + "\n".join(lst_mgs[el]))
                lst_mgs.clear()
                lst_idx.clear()
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif choice == "📘 Номер":
        search_query = search_query.lower()
        search_by_number(search_query)
        if len(lst_idx) > 0:
            for i in lst_idx:
                cursor.execute(
                    'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                    (i,))
                mgs = cursor.fetchall()
                mgs = list(mgs[0])
                lst_mgs.append(mgs)
            if check_user(message.from_user.id, lst_mgs[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for el in range(len(lst_mgs)):
                    for i in range(len(lst_mgs[el])):
                        lst_mgs[el][i] = lst_mgs[el][i].replace("\n", " ")
                    bot.send_message(message.chat.id, text=str(lst_idx[el]) + ". " + "\n".join(lst_mgs[el]))
                lst_mgs.clear()
                lst_idx.clear()
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif choice == "💾 Дата выхода":
        search_query = search_query.lower()
        search_by_release_date(search_query)
        if len(lst_idx) > 0:
            for i in lst_idx:
                cursor.execute(
                    'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                    (i,))
                mgs = cursor.fetchall()
                mgs = list(mgs[0])
                lst_mgs.append(mgs)
            if check_user(message.from_user.id, lst_mgs[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for el in range(len(lst_mgs)):
                    for i in range(len(lst_mgs[el])):
                        lst_mgs[el][i] = lst_mgs[el][i].replace("\n", " ")
                    bot.send_message(message.chat.id, text=str(lst_idx[el]) + ". " + "\n".join(lst_mgs[el]))
                lst_mgs.clear()
                lst_idx.clear()
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif choice == "💾 Дата ввода действия на предприятие":
        search_query = search_query.lower()
        search_by_start_date(search_query)
        if len(lst_idx) > 0:
            for i in lst_idx:
                cursor.execute(
                    'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                    (i,))
                mgs = cursor.fetchall()
                mgs = list(mgs[0])
                lst_mgs.append(mgs)
            if check_user(message.from_user.id, lst_mgs[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for el in range(len(lst_mgs)):
                    for i in range(len(lst_mgs[el])):
                        lst_mgs[el][i] = lst_mgs[el][i].replace("\n", " ")
                    bot.send_message(message.chat.id, text=str(lst_idx[el]) + ". " + "\n".join(lst_mgs[el]))
                lst_mgs.clear()
                lst_idx.clear()
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")
    elif choice == "📋 Ключевые слова":
        search_query = search_query.lower()
        search_by_key_words(search_query)
        if len(lst_idx) > 0:
            for i in lst_idx:
                cursor.execute(
                    'SELECT Type, Name, Number, ReleaseDate, StartDate, KeyWords FROM FirstOfAll WHERE Indexes = ?',
                    (i,))
                mgs = cursor.fetchall()
                mgs = list(mgs[0])
                lst_mgs.append(mgs)
            if check_user(message.from_user.id, lst_mgs[0][0]):
                bot.send_message(message.chat.id, text="Возможно, Вы имели ввиду?\n")
                for el in range(len(lst_mgs)):
                    for i in range(len(lst_mgs[el])):
                        lst_mgs[el][i] = lst_mgs[el][i].replace("\n", " ")
                    bot.send_message(message.chat.id, text=str(lst_idx[el]) + ". " + "\n".join(lst_mgs[el]))
                lst_mgs.clear()
                lst_idx.clear()
            else:
                bot.send_message(message.chat.id,
                                 text="Ошибка авторизации! У Вас нет доступа к данному типу документов!")
        else:
            bot.send_message(message.chat.id, text="Повторите запрос")


def process_document_type(message):
    bot.send_message(message.chat.id, "Введите тип документа:")
    bot.register_next_step_handler(message, process_document_name)


def process_document_name(message):
    document_name = message.text
    bot.send_message(message.chat.id, "Введите название документа:")
    bot.register_next_step_handler(message, process_document_number, document_name)


def process_document_number(message, document_type):
    document_number = message.text
    bot.send_message(message.chat.id, "Введите номер документа:")
    bot.register_next_step_handler(message, process_start_date, document_type, document_number)


def process_start_date(message, document_type, document_name):
    entry_date = message.text
    if number_is_valid(message.text):
        bot.send_message(message.chat.id, "Введите дату выхода (в формате ГГГГ-ММ-ДД 00:00:00):")
        bot.register_next_step_handler(message, process_exit_date, document_type, document_name, entry_date)
    else:
        bot.send_message(message.chat.id, "Некорректный номер, попробуйте еще раз")
        bot.register_next_step_handler(message, process_start_date, document_type, document_name)


def process_exit_date(message, document_type, document_name, document_number):
    exit_date = message.text
    if date_is_valid(message.text):
        bot.send_message(message.chat.id, "Введите дату ввода в действие (в формате ГГГГ-ММ-ДД 00:00:00):")
        bot.register_next_step_handler(message, process_key_words_date, document_type, document_name,
                                       document_number, exit_date)
    else:
        bot.send_message(message.chat.id, "Некорректная дата выхода, попробуйте еще раз")
        bot.register_next_step_handler(message, process_exit_date, document_type, document_name, document_number)


def process_key_words_date(message, document_type, document_name, document_number, entry_date):
    key_words = message.text
    if date_is_valid(message.text):
        bot.send_message(message.chat.id, "Введите ключевые слова (разделите их запятыми):")
        bot.register_next_step_handler(message, save_document, document_type, document_name,
                                       document_number, entry_date, key_words)
    else:
        bot.send_message(message.chat.id, "Некорректная дата ввода в действие, попробуйте еще раз")
        bot.register_next_step_handler(message, process_key_words_date, document_type,
                                       document_name, document_number, entry_date)


def save_document(message, document_type, document_name, document_number, entry_date, exit_date):
    keywords = message.text
    global want_add_doc
    want_add_doc = False
    try:
        # Вставка данных в таблицу
        cursor.execute('''INSERT INTO FirstOfAll (Indexes, Type, Name, Number, ReleaseDate, StartDate, KeyWords)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', (max_index + 1, document_type, document_name,
                                                            document_number, entry_date, exit_date, keywords))
        conn.commit()
        bot.send_message(message.chat.id, "Документ успешно добавлен в базу данных!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


def change_str1(message):
    msg = message.text.split('\n')
    try:
        if int(msg[0]) > max_index or int(msg[0]) <= 0:
            bot.send_message(message.chat.id, "Некорректно указанный индекс!")
        else:
            conn.execute("UPDATE FirstOfAll SET Type = ?, Name = ?, Number = ?, ReleaseDate = ?, StartDate = ?,"
                         "KeyWords = ? WHERE Indexes = ?", (str(msg[1]), str(msg[2]),
                                                            str(msg[3]), str(msg[4]), str(msg[5]), str(msg[6]), msg[0]))
            conn.commit()
            bot.send_message(message.chat.id, "Документ успешно изменён!")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так!")
    finally:
        global want_change_doc
        want_change_doc = False


def del_str(message):
    global max_index
    if int(message.text) > max_index or int(message.text) <= 0:
        bot.send_message(message.chat.id, "Некорректно указанный индекс!")
    else:
        conn.execute("DELETE FROM FirstOfAll WHERE Indexes = ?", (message.text,))
        for i in range(int(message.text) + 1, max_index + 1):
            conn.execute("UPDATE FirstOfAll SET Indexes = ? WHERE Indexes = ?", (i - 1, i))
        conn.commit()
        max_index -= 1
        bot.send_message(message.chat.id, "Документ успешно удалён!")


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
            btn3 = types.KeyboardButton("✅ Документы")
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
            btn3 = types.KeyboardButton("✅ Документы")
            markup.add(btn1, btn2, btn3)
            button4 = types.KeyboardButton("🕹 Удалить ключ доступа")
            button5 = types.KeyboardButton("💼 Добавить/изменить ключ доступа")
            button6 = types.KeyboardButton("📩 Извлечь таблицу")
            markup.add(button4, button5, button6)
            bot.send_message(message.chat.id, text='Вы вошли в систему как администратор.\n'
                                                   'Выберите один из предложенных вариантов:', reply_markup=markup)
            users_laws[message.from_user.id] = "abswin"
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
def func(message):
    global want_add_it, key, want_delete_it, is_find, want_add_it2, want_add_doc, max_index, want_change_doc
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
        bot.send_message(message.chat.id, text="Выберите интересующий Вас вопрос из справки:", reply_markup=markup)
    elif message.text == "✅ Документы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("📲 Добавить документ")
        btn2 = types.KeyboardButton("⌨️ Отредактировать документ")
        btn3 = types.KeyboardButton("💣 Удалить документ")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text="Выберите интересующую Вас опцию:", reply_markup=markup)
    elif message.text == "📲 Добавить документ":
        want_add_doc = True
        process_document_type(message)
        cursor.execute('SELECT MAX(Indexes) FROM FirstOfAll')
        max_index = cursor.fetchone()[0]
    elif message.text == "⌨️ Отредактировать документ":
        want_change_doc = True
        bot.send_message(message.chat.id, text="Укажите индекс изменяемой строки, а после через перенос строки "
                                               "укажите все новые параметры строки:")
        bot.register_next_step_handler(message, change_str1)
    elif message.text == "💣 Удалить документ":
        want_change_doc = True
        bot.send_message(message.chat.id, text="Укажите индекс удаляемой строки:")
        bot.register_next_step_handler(message, del_str)

        cursor.execute('SELECT MAX(Indexes) FROM FirstOfAll')
        max_index = cursor.fetchone()[0]
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
    elif message.text == "📩 Извлечь таблицу":
        if message.from_user.id not in admin_user_id:
            bot.send_message(message.chat.id, text="Ошибка! Вы не обладаете правами администратора.")
        else:
            query = "SELECT * FROM FirstOfAll"
            df = pd.read_sql_query(query, conn)
            temp_excel_file = "temp_data.xlsx"
            df.to_excel(temp_excel_file, index=False)
            with open(temp_excel_file, 'rb') as document:
                bot.send_document(message.chat.id, document)
            document.close()
            os.remove(temp_excel_file)
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
        bot.send_message(message.chat.id, "Нажмите поиск,"
                                          " после этого введите свой запрос")

    elif message.text == "Что этот бот умеет делать?":
        bot.send_message(message.chat.id, text="Этот бот умеет"
                                               " добавлять новые документы в базу данных"
                                               " и находить документ по запросу")

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Справка")
        button2 = types.KeyboardButton("❓ Поиск")
        button3 = types.KeyboardButton("✅ Документы")
        markup.add(button1, button2, button3)
        if message.from_user.id in admin_user_id:
            button4 = types.KeyboardButton("🕹 Удалить ключ доступа")
            button5 = types.KeyboardButton("💼 Добавить/изменить ключ доступа")
            button6 = types.KeyboardButton("📩 Извлечь таблицу")
            markup.add(button4, button5, button6)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню.", reply_markup=markup)
    else:
        if not is_find and not want_add_doc and not want_change_doc:
            bot.send_message(message.chat.id, text="Ошибка. Такой команды нет.")


bot.polling(none_stop=True)
