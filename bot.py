import telebot
from config import *
from logic import *
bot = telebot.TeleBot(bot)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Для помощи введи /help")
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Вот список моих команд:\n/start - приветствие\n/help - все команды\nНапиши любое сообщение с запросом что хочешь увидеть в изображении!")
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text = message.text
    gen = generate(text)
    bot.reply_to(message, f"{gen}")
bot.infinity_polling()