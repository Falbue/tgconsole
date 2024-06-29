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

@bot.message_handler(func=lambda message: True)
def execute_command(message):
    if message.from_user.id == ALLOWED_USER_ID:
        try:
            # Выполнение команды в текущем пути
            result = subprocess.run(message.text, shell=True, capture_output=True, text=True, cwd=current_path)
            output = result.stdout + result.stderr
            if not output:
                output = "Команда выполнена, но нет вывода."
            # Отправка результата выполнения
            bot.send_message(message.chat.id, output)
        except Exception as e:
            bot.send_message(message.chat.id, str(e))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этого бота.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.from_user.id == ALLOWED_USER_ID:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            file_path = os.path.join(current_path, message.document.file_name)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
                
            bot.send_message(message.chat.id, f"Файл сохранён в: {file_path}")
        except Exception as e:
            bot.send_message(message.chat.id, str(e))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этого бота.")

@bot.message_handler(commands=['restart'])
def restart_bot(message):
    if message.from_user.id == ALLOWED_USER_ID:
        bot.send_message(message.chat.id, "Перезапуск бота...")
        time.sleep(1)  # Даем время для отправки сообщения
        # Запускаем новый процесс и завершаем текущий
        subprocess.Popen([sys.executable] + sys.argv)
        os._exit(0)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этого бота.")


bot.send_message(ADMIN, "Бот запущен...")
bot.polling()