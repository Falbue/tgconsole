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
def send_welcome(message): # команда /start
    if message.from_user.id == ADMIN:
        bot.send_message(message.chat.id, "Привет!")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этого бота.")

@bot.message_handler(commands=['restart'])
def restart_bot(message): # команда /restart
    if message.from_user.id == ADMIN:
        bot.send_message(message.chat.id, "Перезапуск консоли...")
        time.sleep(1)  # Даем время для отправки сообщения
        # Запускаем новый процесс и завершаем текущий
        subprocess.Popen([sys.executable] + sys.argv)
        os._exit(0)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этого бота.")

@bot.message_handler(commands=['cd'])
def change_directory(message): # команда /cd
    if message.from_user.id == ADMIN:
        global FOLDER
        new_path = message.text[len("/cd "):].strip()
        
        if new_path == "":
            # Переход на уровень выше
            new_path = os.path.dirname(FOLDER)
        else:
            if not os.path.isabs(new_path):
                # Относительный путь
                new_path = os.path.join(FOLDER, new_path)
        
        if os.path.isdir(new_path):
            FOLDER = new_path
            bot.send_message(message.chat.id, f"Текущий путь изменён на: {FOLDER}")
        else:
            bot.send_message(message.chat.id, "Неверный путь. Попробуйте ещё раз.")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этого бота.")

@bot.message_handler(content_types=['document'])
def handle_document(message): # обработка документа
    if message.from_user.id == ADMIN:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            file_path = os.path.join(FOLDER, message.document.file_name)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
                
            bot.send_message(message.chat.id, f"Файл сохранён в: {file_path}")
        except Exception as e:
            bot.send_message(message.chat.id, str(e))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этого бота.")

def send_large_message(chat_id, text, max_length=4096): # Отправляет сообщение большими частями, если оно превышает max_length
    if len(text) <= max_length:
        bot.send_message(chat_id, text)
    else:
        for i in range(0, len(text), max_length):
            bot.send_message(chat_id, text[i:i + max_length])

@bot.message_handler(func=lambda message: True)
def execute_command(message):  # обработка сообщения пользователя
    if message.from_user.id == ADMIN:
        try:
            # Выполнение команды в текущем пути
            result = subprocess.run(message.text, shell=True, capture_output=True, text=True, cwd=FOLDER)
            output = result.stdout + result.stderr
            if not output:
                output = "Команда выполнена, но нет вывода."
            # Отправка результата выполнения
            send_large_message(message.chat.id, output)
        except Exception as e:
            send_large_message(message.chat.id, str(e))
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этого бота.")

print("Консоль доступна...")
bot.send_message(ADMIN, "Консоль доступна...")
bot.polling()