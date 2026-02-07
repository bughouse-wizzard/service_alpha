"""
Роутер для работы с сессиями
"""
import uuid
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.domain.entities.session import SessionEntity
from app.schemas.session import SessionCreate, SessionResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/session", response_model=SessionResponse)
async def get_or_create_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Получить или создать сессию.

    Если в куках есть session_token, возвращает существующую сессию.
    Если нет - создает новую сессию и устанавливает куку.
    """
    # Проверяем наличие session_token в куках
    session_token = request.cookies.get("session_token")

    if session_token:
        # Ищем существующую сессию
        try:
            session_uuid = uuid.UUID(session_token)
            # Для SQLite ищем по строковому представлению
            from app.infra.config import settings
            if "sqlite" in settings.DATABASE_URL:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == str(session_uuid)
                ).first()
            else:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == session_uuid
                ).first()
        except ValueError:
            session_entity = None

        if session_entity:
            # Обновляем время последнего визита
            session_entity.last_seen_at = datetime.utcnow()
            db.commit()

            # Отладка
            logger.error(f"DEBUG: session_entity.id = {session_entity.id}, type = {type(session_entity.id)}")

            return SessionResponse(
                id=str(session_entity.id),
                created_at=session_entity.created_at,
                last_seen_at=session_entity.last_seen_at,
                token=str(session_entity.id)  # Добавляем токен для совместимости с фронтендом
            )

    # Создаем новую сессию
    session_uuid = uuid.uuid4()
    session_uuid_str = str(session_uuid)
    logger.error(f"DEBUG: Creating session with uuid = {session_uuid_str}, type = {type(session_uuid_str)}")
    
    # Для SQLite используем строковое представление UUID
    from app.infra.config import settings
    if "sqlite" in settings.DATABASE_URL:
        session_entity = SessionEntity(
            id=session_uuid_str,  # Используем строку для SQLite
            token=session_uuid_str,
            created_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow()
        )
    else:
        session_entity = SessionEntity(
            id=session_uuid,  # Используем UUID объект для PostgreSQL
            token=session_uuid_str,
            created_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow()
        )
    
    logger.error(f"DEBUG: session_entity created, id = {session_entity.id}, type = {type(session_entity.id)}")

    db.add(session_entity)
    db.commit()

    # Устанавливаем куку
    response.set_cookie(
        key="session_token",
        value=session_uuid_str,
        httponly=True,
        max_age=86400 * 30,  # 30 дней
        samesite="lax"
    )

    # Отладка
    logger.error(f"DEBUG: session_id_str = {session_uuid_str}, type = {type(session_uuid_str)}")
    logger.error(f"DEBUG: session_entity.id = {session_entity.id}, type = {type(session_entity.id)}")
    logger.error(f"DEBUG: session_entity.created_at = {session_entity.created_at}, type = {type(session_entity.created_at)}")
    logger.error(f"DEBUG: session_entity.last_seen_at = {session_entity.last_seen_at}, type = {type(session_entity.last_seen_at)}")

    return SessionResponse(
        id=session_uuid_str,
        created_at=session_entity.created_at,
        last_seen_at=session_entity.last_seen_at,
        token=session_uuid_str  # Добавляем токен для совместимости с фронтендом
    )

@router.delete("/session")
async def delete_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Удалить сессию (выход из системы).
    """
    session_token = request.cookies.get("session_token")
    
    if session_token:
        try:
            session_uuid = uuid.UUID(session_token)
            # Для SQLite ищем по строковому представлению
            from app.infra.config import settings
            if "sqlite" in settings.DATABASE_URL:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == str(session_uuid)
                ).first()
            else:
                session_entity = db.query(SessionEntity).filter(
                    SessionEntity.id == session_uuid
                ).first()
            
            if session_entity:
                db.delete(session_entity)
                db.commit()
        except ValueError:
            pass
    
    # Удаляем куку
    response.delete_cookie(key="session_token")
    
    return {"message": "Сессия удалена"}
