# Импорты
import telebot
import speech_recognition as sr
import os
import ffmpeg
import pyttsx3
from pydub import AudioSegment
from config import *
from logic import *
# Запуск и хэндлеры
bot = telebot.TeleBot(bot)
language = 'ru'
# Команда /start с клавиатурой других команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if language == 'ru':
        welcome_text = "Привет♥! Для помощи введи /help"
    else:
        welcome_text = "Hello♥! Type /help for assistance"
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_keyboard())
# Команда /help с клавитурой для других команд
@bot.message_handler(commands=['help'])
def send_help(message):
    if language == 'ru':
        help_text = "Вот список моих команд:♦\n/start - приветствие\n/help - все команды\n/lang - смена языка\n/text - ответ только текстом\n/image - ответ только картинкой\n/prof - опишите что любите делать\n/voice - озвучка сообщения голосом бота\n/feedback - обратная связь, отзыв\nОтправь любое голосовое сообщение и я отвечу на него!\nНапиши любое сообщение и я отвечу на него!"
    else:
        help_text = "Here is a list of my commands:♦\n/start - greeting\n/help - all commands\n/lang - change language\n/text - answer only text\n/image - answer only image\n/prof - describe what you can do\n/voice - convert text in bot voice\n/feedback - feedback about this project\nSend me any voice message and I will respond to it!\nSend me any message and I will respond to it!"
    bot.send_message(message.chat.id, help_text, reply_markup=create_keyboard())
# Команда для смены языка
@bot.message_handler(commands=['lang'])
def set_language(message):
    try:
        global language
        if len(message.text.split()) > 1:
            lang = message.text.split()[1].lower()
            if lang in ['ru', 'en']:
                language = lang
                if language == 'ru':
                    bot.send_message(message.chat.id, "Язык установлен на Русский☻.")
                else:
                    bot.send_message(message.chat.id, "Language set to English☺.")
            else:
                bot.send_message(message.chat.id, "Пожалуйста, выберите язык♣: /lang ru/en")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, укажите язык♣: /lang ru/en\nPlease, enter language♣: /lang ru/en")
    except Exception:
        if language == "ru":
            bot.send_message(message.chat.id, "Что-то пошло не так•")
        else:
            bot.send_message(message.chat.id, "Something went wrong•")
# Генерация текста
@bot.message_handler(commands=['text'])
def send_text(message):
    try:
        text = message.text
        gen = generate(f"{text}")
        save_request_response(message.from_user.id, text, gen)
        bot.send_message(message.chat.id, f"{gen}")
    except Exception:
        if language == "ru":
            bot.send_message(message.chat.id, "Что-то пошло не так•")
        else:
            bot.send_message(message.chat.id, "Something went wrong•")
# Генерация картинок
@bot.message_handler(commands=['image'])
def send_img(message):
    try:
        text = message.text
        api = Text2ImageAPI(fus, ap, secret)
        api.conv(text)
        img = open('decoded.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
    except Exception:
        if language == "ru":
            bot.send_message(message.chat.id, "Что-то пошло не так•")
        else:
            bot.send_message(message.chat.id, "Something went wrong•")
# Выбор профессии, просто перечислите что нравится
@bot.message_handler(commands=['prof'])
def send_text(message):
    try:
        text = message.text
        gen = generate(f"Какая профессия мне подходит? Я занимаюсь {text}!")
        save_request_response(message.from_user.id, text, gen)
        bot.send_message(message.chat.id, f"{gen}")
    except Exception:
        if language == "ru":
            bot.send_message(message.chat.id, "Что-то пошло не так•")
        else:
            bot.send_message(message.chat.id, "Something went wrong•")
# Обработчик всех голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    temp_voice_file = 'voice.ogg'
    with open(temp_voice_file, 'wb') as f:
        f.write(downloaded_file)
    recognizer = sr.Recognizer()
    result = ""
    os.system(f'ffmpeg -i {temp_voice_file} voice.wav')
    with sr.AudioFile('voice.wav') as source:
        audio = recognizer.record(source)
        if language == 'ru':
            try:
                result = recognizer.recognize_google(audio, language='ru-RU')
                bot.send_message(message.chat.id, result)
                text = result
                gen = generate(f"{text}")
                save_request_response(message.from_user.id, text, gen)
                bot.send_message(message.chat.id, f"{gen}")
            except sr.UnknownValueError:
                bot.reply_to(message, "Не удалось распознать аудио◘.")
            except sr.RequestError:
                bot.reply_to(message, "Ошибка соединения с сервисом•.")
        else:
            try:
                result = recognizer.recognize_google(audio, language='en-US')
                bot.send_message(message.chat.id, result)
                text = result
                gen = generate(f"{text}")
                save_request_response(message.from_user.id, text, gen)
                bot.send_message(message.chat.id, f"{gen}")
            except sr.UnknownValueError:
                bot.reply_to(message, "Unknown value•")
            except sr.RequestError:
                bot.reply_to(message, "Request error•")
    if os.path.isfile(temp_voice_file):
        os.remove(temp_voice_file)
    if os.path.isfile('voice.wav'):
        os.remove('voice.wav')
# Озвучка текста голосом бота и ответ ИИ
@bot.message_handler(commands=['voice'])
def send_voice(message):
    if language == 'ru':
        try:
            text = message.text.split(' ', 1)[1]
            if len(text) <= 500:
                engine = pyttsx3.init()
                engine.save_to_file(text, 'voice_message.mp3')
                engine.runAndWait()
                with open('voice_message.mp3', 'rb') as voice:
                    bot.send_audio(message.chat.id, voice)
                gen = generate(f"{text}")
                save_request_response(message.from_user.id, text, gen)
                bot.send_message(message.chat.id, f"{gen}")
                os.remove('voice_message.mp3')
            else:
                bot.send_message(message.chat.id, "Ваш текст слишком большой♠!")
        except Exception as e:
            if language == "ru":
                bot.send_message(message.chat.id, "Что-то пошло не так•")
            else:
                bot.send_message(message.chat.id, "Something went wrong•")
    else:
        try:
            text = message.text.split(' ', 1)[1]
            if len(text) <= 500:
                engine = pyttsx3.init()
                engine.save_to_file(text, 'voice_message.mp3')
                engine.runAndWait()
                with open('voice_message.mp3', 'rb') as voice:
                    bot.send_audio(message.chat.id, voice)
                gen = generate(f"{text}")
                save_request_response(message.from_user.id, text, gen)
                bot.send_message(message.chat.id, f"{gen}")
                os.remove('voice_message.mp3')
            else:
                bot.send_message(message.chat.id, "Your text >= 500!◘")
        except Exception as e:
            if language == "ru":
                bot.send_message(message.chat.id, "Что-то пошло не так•")
            else:
                bot.send_message(message.chat.id, "Something went wrong•")
# Обратная связь
@bot.message_handler(commands=['feedback'])
def feedback(message):
    try:
        feedback_text = message.text.split(' ', 1)[1]
        user_id = message.chat.id
        save_feedback(user_id, feedback_text)
        if language == "ru":
            bot.send_message(chat_id=message.chat.id, text="Ваш отзыв был успешно добавлен в базу данных♥.")
        else:
            bot.send_message(chat_id=message.chat.id, text="Your feedback added in DB♥.")
    except Exception:
        if language == "ru":
            bot.send_message(message.chat.id, "Что-то пошло не так•")
        else:
            bot.send_message(message.chat.id, "Something went wrong•")
# Ответ на все текстовые сообщения
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        text = message.text
        gen = generate(f"{text}")
        save_request_response(message.from_user.id, text, gen)
        bot.send_message(message.chat.id, f"{gen}")
        api = Text2ImageAPI(fus, ap, secret)
        api.conv(text)
        img = open('decoded.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
    except Exception:
        if language == "ru":
            bot.send_message(message.chat.id, "Что-то пошло не так•")
        else:
            bot.send_message(message.chat.id, "Something went wrong•")
bot.infinity_polling()
