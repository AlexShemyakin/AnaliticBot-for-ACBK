import telebot
from telebot import types
from io_xlsx import excel as ex, excel_news as exnw
from .env import TOKEN
import time
import re

flag = 0
def start_bot():
    bot = telebot.TeleBot(TOKEN)

    # активация командой start
    @bot.message_handler(commands=['start'])
    def command_hello(message):

        bot.reply_to(message, f"\N{Deer} Привет {message.chat.first_name},"
                              f" если вы видите это сообщение, значит бот работает исправно и готов к работе.")
        time.sleep(1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("About")
        btn2 = types.KeyboardButton("News")
        btn3 = types.KeyboardButton("Ads")
        markup.add(btn1, btn2, btn3)

        bot.send_message(message.chat.id,
         "\N{Deer} Чтобы показать назначение бота, кнопок и адрес поддержки, нажмите на кнопку About".format(
                             message.from_user), reply_markup=markup)

        bot.send_message(message.chat.id,
                         "\N{Deer} Для выполнения поиска объявлений нажмите кнопку Ads".format(
                             message.from_user), reply_markup=markup)

        bot.send_message(message.chat.id,
                         "\N{Deer} Для выполнения поиска новостей нажмите кнопку News".format(
                             message.from_user), reply_markup=markup)


    # Получение сообщения от user
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        global start_date
        global flag


        if message.text == 'About':
            bot.send_message(message.chat.id,
                             "\N{Deer} Бот выполняет поиск объявлений о продаже объектов животного мира и их дериватов, "
                             "а также проводит мониторинг интернет-пространства на наличие опубликованных материалов "
                             "по теме контрабанды объектов животного мира и их дериватов.")
            bot.send_message(message.chat.id,
                             "\N{Deer} Для выполнения поиска объявлений нажмите кнопку Ads.")

            bot.send_message(message.chat.id,
                             "\N{Deer} Для выполнения поиска новостей нажмите кнопку News.")

            bot.send_message(message.from_user.id, "\N{Wrench} Если бот перестал работать или есть вопросы, "
                                                   "прошу писать на почту alexander.shemyakin94@gmail.com")

            flag = 0

        elif message.text == 'Ads':
            bot.send_message(message.from_user.id, '\N{Deer} Процесс может занять несколько минут.')
            ex()
            bot.send_message(message.from_user.id, '\N{Deer} Обновленная таблица с объявлениями')
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
            btn1 = types.KeyboardButton("About")
            btn2 = types.KeyboardButton("News")
            btn3 = types.KeyboardButton("Ads")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, 'Процесс может занять несколько минут.'.format(message.from_user),
                             reply_markup=markup)
            exnw('m')
            bot.send_message(message.from_user.id, f'\N{Customs} Обновленная таблица с новостями'.
                             format(message.from_user), reply_markup=markup)

            bot.send_document(message.from_user.id, open('news.xlsx', 'rb'))
            flag = 0

        elif message.text == 'За период':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            bot.send_message(message.from_user.id, "введите дату начала в формате 'ДД.ММ.ГГ'".format(message.from_user),
                             reply_markup=markup)
            flag = 0


        elif re.search('\d\d\D\d\d\D\d\d', message.text) and flag == 0\
                and (int(message.text[:2]) in range(1, 32)) and (int(message.text[3:5]) in range(1, 13)):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)

            day = message.text[:2]
            month = message.text[3:5]
            year = message.text[-2:]
            start_date = f'{month}/{day}/{year}'

            flag = 1
            bot.send_message(message.from_user.id,
                             "Введите конечную дату в формате 'ДД.ММ.ГГ'".format(message.from_user),
                             reply_markup=markup)


        elif re.search('\d\d\D\d\d\D\d\d', message.text) and flag == 1\
                and (int(message.text[:2]) in range(1, 32)) and (int(message.text[3:5]) in range(1, 13)):
            day = message.text[:2]
            month = message.text[3:5]
            year = message.text[-2:]
            end_date = f'{month}/{day}/{year}'

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About")
            btn2 = types.KeyboardButton("News")
            btn3 = types.KeyboardButton("Ads")
            markup.add(btn1, btn2, btn3)
            flag = 0
            bot.send_message(message.from_user.id, 'Процесс может занять несколько минут'.format(message.from_user),
                             reply_markup=markup)
            exnw('p', start_date, end_date)
            bot.send_message(message.from_user.id, f'\N{Customs} Обновленная таблица с новостями'.
                             format(message.from_user), reply_markup=markup)
            bot.send_document(message.from_user.id, open('news.xlsx', 'rb'))


        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About")
            btn2 = types.KeyboardButton("News")
            btn3 = types.KeyboardButton("Ads")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, 'Вы вышли в главное меню.'.format(message.from_user),
                             reply_markup=markup)
            flag = 0


        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About")
            btn2 = types.KeyboardButton("News")
            btn3 = types.KeyboardButton("Ads")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, '\N{Cross Mark} Неизвестная команда. Попробуйте заново.'.
                             format(message.from_user), reply_markup=markup)
            flag = 0

    bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
    start_bot()
    

