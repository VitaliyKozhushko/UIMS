#!/bin/bash

echo "Объединение .env файлов..."
python3 create_common_env.py

if [ $? -eq 0 ]; then
    echo "Файлы .env успешно объединены."
else
    echo "Ошибка при объединении .env файлов. Запуск Docker Compose остановлен."
    exit 1
fi

echo "Запуск Docker Compose..."
docker compose down -v
#docker compose up --build -d
docker compose up --build