#!/bin/bash
# Скрипт запуска стабильной системы

echo "Остановка всех процессов..."
pkill -f "uvicorn app.main:app" || true
pkill -f "celery" || true

echo "Очистка базы данных..."
cd /home/av/nmck-system
rm -f nmck.db

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Создание таблиц с исправлением UUID..."
python -c "
import sys
sys.path.insert(0, '.')
from sqlalchemy import String
from app.infra.database import Base, engine

# Исправляем типы UUID
for table in Base.metadata.tables.values():
    for column in table.columns:
        if hasattr(column.type, '__visit_name__') and column.type.__visit_name__ == 'UUID':
            column.type = String(36)

Base.metadata.create_all(bind=engine)
print('Таблицы созданы успешно')
"

echo "Запуск сервера..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

echo "Проверка запуска..."
sleep 3
if ps aux | grep uvicorn | grep -v grep; then
    echo "Сервер успешно запущен!"
    echo "Логи: tail -f server.log"
else
    echo "Ошибка запуска сервера"
    tail -50 server.log
fi
