#!/usr/bin/env python3
"""
Патч для исправления UUID в SQLite
"""
import os
import sys

def fix_uuid_for_sqlite():
    """Исправляет файлы для работы с UUID в SQLite"""
    
    # 1. Исправляем app/domain/entities/base.py
    base_file = "app/domain/entities/base.py"
    if os.path.exists(base_file):
        with open(base_file, 'r') as f:
            content = f.read()
        
        # Заменяем SQLUUID на String(36) для SQLite
        new_content = content.replace(
            "from sqlalchemy import DateTime, String, UUID as SQLUUID",
            "from sqlalchemy import DateTime, String\nfrom sqlalchemy.dialects.postgresql import UUID as SQLUUID"
        )
        
        # Добавляем условную логику для SQLite
        new_content = new_content.replace(
            """class BaseEntity(Base):
    __abstract__ = True
    
    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)""",
            """class BaseEntity(Base):
    __abstract__ = True
    
    # Используем String для SQLite, UUID для PostgreSQL
    from app.infra.config import settings
    if "sqlite" in settings.DATABASE_URL:
        id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    else:
        id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)"""
        )
        
        with open(base_file, 'w') as f:
            f.write(new_content)
        print(f"✓ Исправлен {base_file}")
    
    # 2. Создаем исправленный main.py
    main_file = "app/main.py"
    if os.path.exists(main_file):
        with open(main_file, 'r') as f:
            content = f.read()
        
        # Заменяем создание таблиц на умную версию
        new_content = content.replace(
            """from app.infra.database import get_db, engine
from app.domain.entities.base import Base

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)""",
            """from app.infra.database import get_db, engine
from app.domain.entities.base import Base
from sqlalchemy import String

# Создаем таблицы в БД с исправлением UUID для SQLite
from app.infra.config import settings
if "sqlite" in settings.DATABASE_URL:
    # Исправляем типы UUID для SQLite
    for table in Base.metadata.tables.values():
        for column in table.columns:
            if hasattr(column.type, '__visit_name__') and column.type.__visit_name__ == 'UUID':
                column.type = String(36)

Base.metadata.create_all(bind=engine)"""
        )
        
        with open(main_file, 'w') as f:
            f.write(new_content)
        print(f"✓ Исправлен {main_file}")
    
    print("\n✅ Патч применен успешно!")

if __name__ == "__main__":
    fix_uuid_for_sqlite()