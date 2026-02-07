#!/usr/bin/env python3
"""
Патч для исправления конвертации UUID в строку для SQLite
"""
import os

def create_uuid_fix():
    """Создает файл с исправлением конвертации UUID"""
    
    fix_py = """#!/usr/bin/env python3
\"\"\"
Исправление для работы UUID с SQLite
\"\"\"
import uuid
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class UUIDString(TypeDecorator):
    \"\"\"Кастомный тип для хранения UUID как строки в SQLite\"\"\"
    impl = String(36)
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return str(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value


def apply_uuid_fix():
    \"\"\"Применяет исправление UUID для всех моделей\"\"\"
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Импортируем после добавления пути
    from app.domain.entities.base import BaseEntity
    from app.infra.config import settings
    from sqlalchemy import inspect
    
    # Проверяем, используем ли мы SQLite
    if "sqlite" in settings.DATABASE_URL:
        print("🔧 Применяем исправление UUID для SQLite...")
        
        # Импортируем все модели
        from app.domain.entities import session, upload, task, contract, selection
        
        # Получаем все таблицы
        from app.domain.entities.base import Base
        from sqlalchemy import event
        
        # Создаем обработчик для преобразования UUID перед сохранением
        @event.listens_for(Base.metadata, "before_create")
        def before_create(target, connection, **kw):
            \"\"\"Исправляем типы столбцов перед созданием таблиц\"\"\"
            for table in Base.metadata.tables.values():
                for column in table.columns:
                    if hasattr(column.type, '__visit_name__') and column.type.__visit_name__ == 'UUID':
                        column.type = String(36)
        
        print("✅ Исправление применено")
    else:
        print("ℹ️ Используется PostgreSQL, исправление не требуется")


if __name__ == "__main__":
    apply_uuid_fix()
"""
    
    # Создаем также исправленный main.py с обработкой UUID
    main_py_fixed = """#!/usr/bin/env python3
\"\"\"
Основной файл FastAPI приложения системы НМЦК
\"\"\"
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.infra.database import get_db, engine
from app.domain.entities.base import Base
from app.schemas.session import SessionCreate, SessionResponse
from app.schemas.upload import UploadCreate, UploadResponse
from app.schemas.task import TaskCreate, TaskResponse, TaskListResponse
from app.schemas.contract import ContractResponse
from app.schemas.selection import SelectionUpdate, SelectionResponse
from app.api import session, upload, task, contract, selection, stop

# Импортируем исправление UUID
from app.infra.config import settings
if "sqlite" in settings.DATABASE_URL:
    # Применяем исправление для SQLite
    from sqlalchemy import String, event
    
    # Исправляем типы UUID перед созданием таблиц
    @event.listens_for(Base.metadata, "before_create")
    def before_create(target, connection, **kw):
        for table in Base.metadata.tables.values():
            for column in table.columns:
                if hasattr(column.type, '__visit_name__') and column.type.__visit_name__ == 'UUID':
                    column.type = String(36)
    
    # Также исправляем существующие метаданные
    for table in Base.metadata.tables.values():
        for column in table.columns:
            if hasattr(column.type, '__visit_name__') and column.type.__visit_name__ == 'UUID':
                column.type = String(36)

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Система расчета НМЦК",
    description="Система автоматического поиска и расчета начальной максимальной цены контракта",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем роутеры
app.include_router(session.router, prefix="/api", tags=["Сессии"])
app.include_router(upload.router, prefix="/api", tags=["Загрузка файлов"])
app.include_router(task.router, prefix="/api", tags=["Задачи"])
app.include_router(contract.router, prefix="/api", tags=["Контракты"])
app.include_router(selection.router, prefix="/api", tags=["Выбор контрактов"])
app.include_router(stop.router, prefix="/api", tags=["Остановка задач"])

# WebSocket соединения
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_token: str):
        await websocket.accept()
        self.active_connections[session_token] = websocket

    def disconnect(self, session_token: str):
        if session_token in self.active_connections:
            del self.active_connections[session_token]

    async def send_personal_message(self, message: dict, session_token: str):
        if session_token in self.active_connections:
            websocket = self.active_connections[session_token]
            try:
                await websocket.send_json(message)
            except:
                self.disconnect(session_token)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket, session_token: str):
    await manager.connect(websocket, session_token)
    try:
        while True:
            # Ожидаем сообщения от клиента (ping/pong)
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(session_token)

@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
    
    with open("uuid_fix.py", "w") as f:
        f.write(fix_py)
    
    with open("main_fixed_uuid.py", "w") as f:
        f.write(main_py_fixed)
    
    print("✅ Созданы файлы исправлений:")
    print("   - uuid_fix.py (исправление конвертации UUID)")
    print("   - main_fixed_uuid.py (исправленный main.py)")
    
    print("\n📋 Инструкция для применения:")
    print("1. Подключитесь к серверу: ssh av@192.168.88.170")
    print("2. Перейдите в директорию: cd /home/av/nmck-system")
    print("3. Остановите сервер: pkill -f 'uvicorn app.main:app'")
    print("4. Замените app/main.py: cp main_fixed_uuid.py app/main.py")
    print("5. Удалите БД: rm -f nmck.db")
    print("6. Запустите: source venv/bin/activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    create_uuid_fix()