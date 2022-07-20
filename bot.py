import telebot
from telebot import types
from test_sxls import excel as ex
import sched
import time


def start_bot():
    token = '5592992190:AAHDKnVr3bEq5oDTKbslJcMQiCUygdBc9Os'
    bot = telebot.TeleBot(token)
    flag = 0 #флаг для определения ввода запроса

    # активация командой start
    @bot.message_handler(commands=['start'])
    def command_hello(message):
        bot.reply_to(message, f"Привет {message.chat.first_name}, если вы видите это сообщение, значит бот работает исправно и готов к работе.")
        time.sleep(1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("About Bot")
        #btn2 = types.KeyboardButton("Find")
        btn2 = types.KeyboardButton("Start")
        markup.add(btn1, btn2)

        bot.send_message(message.chat.id,
                         "Чтобы подробнее узнать про данный Бот нажмите на кнопку About bot.".format(
                             message.from_user), reply_markup=markup)

        bot.send_message(message.chat.id,
                         "Для выполнений запроса нажмите кнопку Start".format(
                             message.from_user), reply_markup=markup)


    # Получение сообщения от user
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        global flag
        if message.text == 'About Bot':
            bot.send_message(message.from_user.id, f"В тестовом режиме бот анализирует olx.kz и формирует excel-файл.")

        elif message.text == 'Start':
            ex()
            bot.send_document(message.from_user.id, open('test_xlsx.xlsx', 'rb'))
            #bot.send_message(message.from_user.id, answer)

        # elif message.text == 'Start':
        #    markup = types.ReplyKeyboardRemove()
        #    bot.send_message(message.from_user.id, f"Введите запрос.", reply_markup=markup)
        #    flag = 1

        # elif flag == 1 and message.text:
        #    flag = 0
        #    answer = f'{main()}'
        #    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #    btn1 = types.KeyboardButton("About Bot")
        #    btn2 = types.KeyboardButton("Find")
        #    btn3 = types.KeyboardButton("Enter a request")
        #    markup.add(btn1, btn2, btn3)
        #    bot.send_message(message.from_user.id, answer, reply_markup=markup)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    start_bot()

