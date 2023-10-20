import telebot
from telebot import types
import sqlite3
import emoji
import random

telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot("6141817809:AAHWHCtd06XQONFyVxjsmbS0nHmy2q9T6Ks")

connection = sqlite3.connect('dict_final.db', check_same_thread=False)
cur = connection.cursor()

HELP = '''
Список доступных команд:
* /start  - начать работу
* /menu - вывести меню
* /help - показать подсказку
* /topics - показать доступные темы
'''
states = {}  # словарь для хранения состояний пользователей

START = range(10)  # возможные состояния пользователя


@bot.message_handler(commands=['start'])
def start_message(message):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    bot.send_message(message.chat.id, "Привет, {0.first_name}!".format(message.from_user))
    helper(message)
    menu(message)


@bot.message_handler(commands=['topics'])
def topics_menu(message):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Особенности речи')
    item2 = types.KeyboardButton('Расстройства головного мозга')
    item3 = types.KeyboardButton('Нейролингвистика и нейронауки')
    item4 = types.KeyboardButton('Функции головного мозга')
    item5 = types.KeyboardButton('Методы нейролингвистики')
    item6 = types.KeyboardButton('Строение головного мозга и нервной системы')

    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, "Выберете тему", reply_markup=markup)
    bot.register_next_step_handler(message, topics)


@bot.message_handler(commands=['menu'])
def menu(message):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Ввести термин')
    item2 = types.KeyboardButton('Ввести тему')

    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Выберете из меню", reply_markup=markup)


@bot.message_handler(commands=['yes'])
def yes_no(message, text):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Да')
    item2 = types.KeyboardButton('Нет')

    markup.add(item1, item2)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['help'])
def helper(message):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    if message.chat.type == 'private':
        if message.text == 'Ввести термин':
            bot.send_message(message.chat.id, "Введите термин")
            bot.register_next_step_handler(message, u_message)
        elif message.text == 'Ввести тему':
            topics_menu(message)
        else:
            bot.send_message(message.chat.id, "Не совсем понимаю(")
            menu(message)


def u_message(message):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    if message.chat.type == 'private':
        term = message.text
        answer = cur.execute(
            "SELECT Термин, Определение, Связанные_термины, Ссылка, Название_статьи, Автор FROM terms_n "
            "WHERE Термин = ?",
            (term.upper(),)).fetchall()

        answer_2 = cur.execute(
            "SELECT Термин, Альтернативный_запрос, Определение, Связанные_термины, Ссылка, Название_статьи, "
            "Автор FROM terms_n WHERE Альтернативный_запрос = ?",
            (term.upper(),)).fetchall()

        if answer:
            answer = [*answer[0]]
            if answer[3]:
                final_answer = (emoji.emojize(f':check_mark:{term.upper()} - '
                                              f'{answer[1]}\n\nНазвание статьи: '
                                              f'{answer[4]} ({answer[5]})\nСсылка: {answer[3]}'))
            else:
                final_answer = (emoji.emojize(f'{term.upper()} - {answer[1]}'))
            bot.send_message(message.chat.id, final_answer)

            if answer[2]:
                with open('my_file.dat', 'w+') as f:
                    f.write(answer[2])
                yes_no(message, 'Хотите увидеть связанные термины?')
                bot.register_next_step_handler(message, extra)
            else:
                menu(message)

        if answer_2:
            answer_2 = [*answer_2[0]]
            if answer_2[4]:
                final_answer = (emoji.emojize(f':check_mark:{answer_2[0]} ({answer_2[1]}) - '
                                              f'{answer_2[2]}\n\nНазвание статьи: '
                                              f'{answer_2[5]} ({answer_2[6]})\nСсылка: {answer_2[4]}'))
            else:
                final_answer = (emoji.emojize(f'{answer_2[0]} ({answer_2[1]}) - {answer_2[2]}'))
            bot.send_message(message.chat.id, final_answer)

            if answer_2[3]:
                with open('my_file.dat', 'w+') as f:
                    f.write(answer_2[3])

                yes_no(message, 'Хотите увидеть связанные термины?')
                bot.register_next_step_handler(message, extra)
            else:
                menu(message)

        if not answer and not answer_2:
            bot.send_message(message.chat.id, 'Нет такого термина')
            menu(message)


def extra(message):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    if message.text == 'Да':
        with open('my_file.dat') as f:
            terms = f.read()

        final_answer = [emoji.emojize(f':check_mark:{i}') for i in terms.split(",")]

        bot.send_message(message.chat.id, "\n\n".join(final_answer))
        yes_no(message, 'Хотите увидеть значение терминов?')
        bot.register_next_step_handler(message, definitions_extra)
    else:
        menu(message)


def definitions_extra(message):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    if message.text == 'Да':
        with open('my_file.dat') as f:
            terms = f.read()

        final_answer = []
        for i in terms.split(","):
            reply = cur.execute("SELECT Термин, Определение FROM terms_n WHERE Термин = ?", (i.strip(),)).fetchall()
            if reply:
                new_answer = [*reply[0]]
                final_answer.append(emoji.emojize(f':check_mark: {" - ".join(new_answer)}'))
        bot.send_message(message.chat.id, "\n\n".join(final_answer))
    menu(message)


def topics(message):
    secret = random.randint(1, 49494985894939494944)
    states[secret] = START
    reply = cur.execute("SELECT Термин, Определение, Раздел FROM terms_n WHERE Раздел = ?",
                        (message.text.upper(),)).fetchall()
    topic_1 = []
    if reply:
        for i in reply:
            new_answer = [*i]
            topic_1.append(emoji.emojize(f':brain:{new_answer[0]} - {new_answer[1]}'))

        bot.send_message(message.chat.id, message.text.upper())
        bot.send_message(message.chat.id, "\n\n".join(topic_1[:19]))
        if topic_1[19:]:
            bot.send_message(message.chat.id, "\n\n".join(topic_1[19:]))
    else:
        bot.send_message(message.chat.id, 'Нет такой темы')
    menu(message)


bot.infinity_polling(none_stop=True)
