#!/bin/bash

# Установка необходимых пакетов
pkg update -y
pkg install -y python
pkg install -y python-pip

# Установка библиотек Python
pip install pyTelegramBotAPI

# Создание директории для бота и копирование файлов
mkdir -p $PREFIX/share/bot
cp bot.py $PREFIX/share/bot/bot.py

echo "Установка завершена. Для запуска используйте: tgconsole 'id_пользователя' 'api_bota'"
