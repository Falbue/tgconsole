API = ''
FOLDER = '/data/data/com.termux/files/home'
ADMIN = 1
# -----------------------------------------------------------
import telebot
import subprocess
import os
import sys
import time

bot = telebot.TeleBot(API)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id == ALLOWED_USER_ID:
        bot.send_message(message.chat.id, "Привет!")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этого бота.")

bot.send_message(ADMIN, "Бот запущен...")
bot.polling()