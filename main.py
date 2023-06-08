import telebot
import os

token = os.getenv('TOKEN')

bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, 'Hey there. To download some track just enter its url.')


bot.infinity_polling()