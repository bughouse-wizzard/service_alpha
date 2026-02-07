"""
API эндпоинты для аутентификации и управления пользователями.
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.postgres.engine import get_session
from db.postgres.models.user import User

# Конфигурация
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Инициализация
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

router = APIRouter(prefix="/api/auth", tags=["authentication"])


# Модели
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    confirm_password: str


class UserResponse(UserBase):
    id: str
    role: str
    created_at: str
    updated_at: str


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


# Вспомогательные функции
def verify_password(plain_password, hashed_password):
    """Проверка пароля."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Хеширование пароля."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создание access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Создание refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    """Получение текущего пользователя из токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Получение пользователя из базы данных
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise credentials_exception

    return {
        "id": str(user.id),
        "email": user.email,
        "username": user.username,
        "role": "user",  # Default role since User model doesn't have role field
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else "",
        "updated_at": user.updated_at.isoformat() if user.updated_at else ""
    }


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """Проверка активности пользователя."""
    # Здесь можно добавить проверку на активность пользователя
    # Например, проверку is_active или других флагов
    return current_user


def decode_token(token: str):
    """Декодирование токена."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# Эндпоинты
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_session)):
    """Регистрация нового пользователя."""
    # Проверка совпадения паролей
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )
    
    # Проверка существования пользователя
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Хеширование пароля
    hashed_password = get_password_hash(user.password)

    # Создание пользователя
    user_id = uuid.uuid4()
    created_at = datetime.utcnow()
    
    # Генерация уникального username из email
    base_username = user.email.split('@')[0]
    username = base_username
    counter = 1
    
    # Проверка уникальности username
    while True:
        existing_user = db.query(User).filter(User.username == username).first()
        if not existing_user:
            break
        username = f"{base_username}{counter}"
        counter += 1
    
    new_user = User(
        id=user_id,
        email=user.email,
        username=username,
        password_hash=hashed_password,
        is_active=True,
        created_at=created_at,
        updated_at=created_at,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=str(user_id),
        email=user.email,
        role="user",
        created_at=created_at.isoformat(),
        updated_at=created_at.isoformat(),
    )


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_session)):
    """Вход в систему."""
    # Аутентификация пользователя
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создание токенов
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_session)):
    """Обновление access token с помощью refresh token."""
    try:
        payload = decode_token(request.refresh_token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # Проверка существования пользователя
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        # Создание нового access token
        new_access_token = create_access_token(data={"sub": user_id})

        return Token(
            access_token=new_access_token,
            token_type="bearer",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}",
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_active_user)):
    """Получение информации о текущем пользователе."""
    return UserResponse(
        id=current_user.get("id", ""),
        email=current_user.get("email", ""),
        role=current_user.get("role", "user"),
        created_at=current_user.get("created_at", ""),
        updated_at=current_user.get("updated_at", ""),
    )


@router.post("/logout")
async def logout():
    """Выход из системы."""
    # В JWT-based аутентификации logout обычно клиентская операция
    # Сервер может добавить токен в черный список, но для простоты просто возвращаем успех
    return {"message": "Successfully logged out"}


@router.post("/password/reset/request")
async def request_password_reset(request: PasswordResetRequest):
    """Запрос на сброс пароля."""
    # В реальном приложении здесь бы отправлялось письмо со ссылкой для сброса
    # Для демонстрации просто возвращаем сообщение
    return {
        "message": "If a user with this email exists, a password reset link has been sent",
    }


@router.post("/password/reset/confirm")
async def confirm_password_reset(request: PasswordResetConfirm):
    """Подтверждение сброса пароля."""
    # В реальном приложении здесь бы проверялся токен и обновлялся пароль
    # Для демонстрации просто возвращаем сообщение
    return {"message": "Password has been reset successfully"}