import telebot
from telebot import types
from test_sxls import excel as ex, excel_news as exnw
# import sched
import time


def start_bot():
    token = '5592992190:AAHDKnVr3bEq5oDTKbslJcMQiCUygdBc9Os'
    bot = telebot.TeleBot(token)

    # активация командой start
    @bot.message_handler(commands=['start'])
    def command_hello(message):
        bot.reply_to(message, f"Привет {message.chat.first_name},"
                              f" если вы видите это сообщение, значит бот работает исправно и готов к работе.")
        time.sleep(1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("About Bot")
        btn2 = types.KeyboardButton("News")
        btn3 = types.KeyboardButton("Ads")
        markup.add(btn1, btn2, btn3)

        bot.send_message(message.chat.id,
                         "Чтобы подробнее узнать про данный Бот нажмите на кнопку About bot.".format(
                             message.from_user), reply_markup=markup)

        bot.send_message(message.chat.id,
                         "Для выполнений запроса нажмите кнопку Start".format(
                             message.from_user), reply_markup=markup)


    # Получение сообщения от user
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        global start_date

        if message.text == 'About Bot':
            bot.send_message(message.from_user.id, "В тестовом режиме бот анализирует olx.kz и формирует excel-файл.")


        elif message.text == 'Ads':
            bot.send_message(message.from_user.id, 'Процесс может занять несколько минут.')
            ex()
            bot.send_document(message.from_user.id, open('ads.xlsx', 'rb'))


        elif message.text == 'News':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            btn2 = types.KeyboardButton("За месяц")
            btn3 = types.KeyboardButton("За период")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, 'Выберите за какой период выполнить поиск.'.format(message.from_user),
                             reply_markup=markup)


        elif message.text == 'За месяц':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About Bot")
            btn2 = types.KeyboardButton("News")
            btn3 = types.KeyboardButton("Start")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, 'Процесс может занять несколько минут.'.format(message.from_user),
                             reply_markup=markup)
            exnw('m')
            bot.send_document(message.from_user.id, open('news.xlsx', 'rb'))


        elif message.text == 'За период':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            bot.send_message(message.from_user.id, "введите дату начала в формате 'ММ.ДД.ГГ'".format(message.from_user),
                             reply_markup=markup)


        elif message.text.isdigit() and message.text.find('.') != -1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Назад")
            markup.add(btn1)
            start_date = message.text
            bot.send_message(message.from_user.id,
                             "Введите конечную дату в формате 'ММ.ДД.ГГ'".format(message.from_user),
                             reply_markup=markup)



        elif message.text.isdigit() and message.text.find:
            end_date = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About Bot")
            btn2 = types.KeyboardButton("Start")
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, 'Процесс может занять несколько минут'.format(message.from_user),
                             reply_markup=markup)
            exnw('p', start_date, end_date)
            bot.send_document(message.from_user.id, open('news.xlsx', 'rb'))


        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("About Bot")
            btn2 = types.KeyboardButton("News")
            btn3 = types.KeyboardButton("Start")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, 'Вы вышли в главное меню.'.format(message.from_user),
                             reply_markup=markup)

        else:
            pass



    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    start_bot()

