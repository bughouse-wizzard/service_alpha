#!/usr/bin/env python3
"""
Простой патч для исправления UUID в SQLite
"""
import os

def apply_simple_fix():
    """Применяет простое исправление для работы с SQLite"""
    
    # 1. Создаем исправленный main.py
    main_py = """#!/usr/bin/env python3
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

# Создаем таблицы в БД с исправлением UUID для SQLite
from sqlalchemy import String
for table in Base.metadata.tables.values():
    for column in table.columns:
        if hasattr(column.type, '__visit_name__') and column.type.__visit_name__ == 'UUID':
            column.type = String(36)

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
    
    # 2. Создаем исправленный base.py
    base_py = """from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseEntity(Base):
    __abstract__ = True
    
    # Используем String для SQLite вместо UUID
    id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
"""
    
    # Сохраняем файлы
    with open("fixed_main.py", "w") as f:
        f.write(main_py)
    
    with open("fixed_base.py", "w") as f:
        f.write(base_py)
    
    print("✅ Созданы исправленные файлы:")
    print("   - fixed_main.py (исправленный app/main.py)")
    print("   - fixed_base.py (исправленный app/domain/entities/base.py)")
    print("\n📋 Инструкция для применения на сервере:")
    print("1. Подключитесь к серверу: ssh av@192.168.88.170")
    print("2. Перейдите в директорию: cd /home/av/nmck-system")
    print("3. Остановите текущие процессы:")
    print("   pkill -f 'uvicorn app.main:app' || true")
    print("   pkill -f celery || true")
    print("4. Создайте резервные копии:")
    print("   cp app/main.py app/main.py.backup")
    print("   cp app/domain/entities/base.py app/domain/entities/base.py.backup")
    print("5. Замените файлы:")
    print("   cp /path/to/fixed_main.py app/main.py")
    print("   cp /path/to/fixed_base.py app/domain/entities/base.py")
    print("6. Удалите старую БД: rm -f nmck.db")
    print("7. Запустите систему:")
    print("   source venv/bin/activate")
    print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &")
    print("8. Проверьте запуск:")
    print("   sleep 3 && tail -20 server.log")

if __name__ == "__main__":
    apply_simple_fix()