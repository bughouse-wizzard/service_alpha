#!/bin/bash
# Скрипт развертывания стабильной системы на сервере

echo "=== Развертывание стабильной системы НМЦК ==="

# 1. Подключение к серверу и остановка текущих процессов
echo "1. Остановка текущих процессов на сервере..."
ssh -o StrictHostKeyChecking=no av@192.168.88.170 << 'EOF'
cd /home/av/nmck-system
echo "Останавливаем все процессы..."
pkill -f "uvicorn app.main:app" || true
pkill -f "celery" || true
sleep 2
EOF

# 2. Копирование исправлений на сервер
echo "2. Копирование исправлений на сервер..."
scp -o StrictHostKeyChecking=no /workspace/fix_uuid_for_sqlite.py av@192.168.88.170:/home/av/nmck-system/

# 3. Применение исправлений и запуск системы
echo "3. Применение исправлений и запуск системы..."
ssh -o StrictHostKeyChecking=no av@192.168.88.170 << 'EOF'
cd /home/av/nmck-system

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Применение патча для UUID..."
python fix_uuid_for_sqlite.py

echo "Удаление старой базы данных..."
rm -f nmck.db

echo "Запуск системы..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

echo "Ожидание запуска..."
sleep 5

echo "Проверка статуса..."
if ps aux | grep uvicorn | grep -v grep; then
    echo "✅ Система успешно запущена!"
    echo "Логи сервера:"
    tail -10 server.log
else
    echo "❌ Ошибка запуска системы"
    echo "Последние логи:"
    tail -50 server.log
fi

echo "Проверка доступности API..."
curl -s http://localhost:8000/health || echo "API недоступен"
EOF

echo "=== Развертывание завершено ==="
echo "Система доступна по адресу: http://192.168.88.170:8000"