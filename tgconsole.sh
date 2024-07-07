#!/bin/bash

# Проверка на наличие параметров
if [ "$#" -ne 2 ]; then
    echo "Использование: tgconsole 'id_пользователя' 'api_bota'"
    exit 1
fi

USER_ID=$1
API_TOKEN=$2

# Обновление конфигурации бота
sed -i "s/^API =.*/API = '$API_TOKEN'/" $PREFIX/share/bot/bot.py
sed -i "s/^ADMIN =.*/ADMIN = $USER_ID/" $PREFIX/share/bot/bot.py

# Запуск бота
python $PREFIX/share/bot/bot.py
