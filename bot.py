import telebot
from telebot import types
from io_xlsx import excel as ex, excel_news as exnw
from settings import TOKEN as TOKEN
import time
import re

flag = 0
def start_bot():
    token = TOKEN
    bot = telebot.TeleBot(token)

    # активация командой start
    @bot.message_handler(commands=['start'])
    def command_hello(message):

        bot.reply_to(message, f"\N{Deer}Привет {message.chat.first_name},"
                              f" если вы видите это сообщение, значит бот работает исправно и готов к работе.")
        time.sleep(1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("About Bot")
        btn2 = types.KeyboardButton("News")
        btn3 = types.KeyboardButton("Ads")
        markup.add(btn1, btn2, btn3)

        bot.send_message(message.chat.id,
                         "\N{Deer}Чтобы подробнее узнать про данный Бот нажмите на кнопку About bot.".format(
                             message.from_user), reply_markup=markup)

        bot.send_message(message.chat.id,
                         "\N{Deer}Для выполнения поиска объявлений нажмите кнопку Ads".format(
                             message.from_user), reply_markup=markup)

        bot.send_message(message.chat.id,
                         "\N{Deer}Для выполнения поиска новостей нажмите кнопку News".format(
                             message.from_user), reply_markup=markup)


    # Получение сообщения от user
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        global start_date
        global flag


        if message.text == 'About Bot':
            bot.send_message(message.from_user.id, "\N{Wrench}Бот разработан для организации 'Казахстанская "
                                                   "ассоциация сохранения биоразнообразия'")
            bot.send_message(message.from_user.id, "\N{Wrench}При возникновении вопросов писать на почту alexander.shemyakin94@gmail.com")
            flag = 0


        elif message.text == 'Ads':
            bot.send_message(message.from_user.id, '\N{Deer}Процесс может занять несколько минут.')
            ex()
            bot.send_message(message.from_user.id, '\N{Deer}Обновленная таблица с объявлениями')
            bot.send_document(message.from_user.id, open('ads.xlsx', 'rb'))
            flag = 0



        elif message.text == 'News':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            btn2 = types.KeyboardButton("За месяц")
            btn3 = types.KeyboardButton("За период")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, 'Выберите за какой период выполнить поиск.'.format(message.from_user),
                             reply_markup=markup)
            flag = 0


        elif message.text == 'За месяц':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About Bot")
            btn2 = types.KeyboardButton("News")
            btn3 = types.KeyboardButton("Start")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, 'Процесс может занять несколько минут.'.format(message.from_user),
                             reply_markup=markup)
            exnw('m')
            bot.send_message(message.from_user.id, f'\N{Customs}Обновленная таблица с новостями за месяц'.
                             format(message.from_user), reply_markup=markup)

            bot.send_document(message.from_user.id, open('news.xlsx', 'rb'))
            flag = 0



        elif message.text == 'За период':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            bot.send_message(message.from_user.id, "введите дату начала в формате 'ММ.ДД.ГГ'".format(message.from_user),
                             reply_markup=markup)
            flag = 0


        elif (re.search('\d\d\D\d\d\D\d\d', message.text) or re.search('\d\D\d\D\d\d', message.text)) and flag == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            start_date = message.text
            flag = 1
            bot.send_message(message.from_user.id,
                             "Введите конечную дату в формате 'ММ.ДД.ГГ'".format(message.from_user),
                             reply_markup=markup)


        elif (re.search('\d\d\D\d\d\D\d\d', message.text) or re.search('\d\D\d\D\d\d', message.text)) and flag == 1:
            end_date = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About Bot")
            btn2 = types.KeyboardButton("Start")
            markup.add(btn1, btn2)
            flag = 0
            bot.send_message(message.from_user.id, 'Процесс может занять несколько минут'.format(message.from_user),
                             reply_markup=markup)
            exnw('p', start_date, end_date)
            bot.send_message(message.from_user.id, f'\N{Customs}Обновленная таблица с новостями за период'.
                             format(message.from_user), reply_markup=markup)
            bot.send_document(message.from_user.id, open('news.xlsx', 'rb'))


        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About Bot")
            btn2 = types.KeyboardButton("News")
            btn3 = types.KeyboardButton("Start")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, '\N{Deer}Вы вышли в главное меню.'.format(message.from_user),
                             reply_markup=markup)
            flag = 0


        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About Bot")
            btn2 = types.KeyboardButton("News")
            btn3 = types.KeyboardButton("Start")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, '\N{Cross Mark}Неизвестная команда. Попробйуте заново.'.format(message.from_user),
                             reply_markup=markup)
            flag = 0



    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    start_bot()

