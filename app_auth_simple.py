import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

# Импортируем только необходимые компоненты
from db.postgres.engine import get_session
# Импортируем модель User напрямую, чтобы избежать циклических импортов
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, UUID, DateTime
from sqlalchemy.sql import func
import uuid as uuid_lib

# Создаем временную модель User для аутентификации
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "orkestrator"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid_lib.uuid4)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

router = APIRouter(prefix="/api")
security = HTTPBearer()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    password: str
    name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    name: str
    role: str

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str) -> str:
    # Ограничиваем пароль 72 байтами для bcrypt
    if len(password.encode('utf-8')) > 72:
        password = password[:50]  # Безопасное ограничение
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/auth/login", response_model=TokenResponse)
async def login(user: UserLogin):
    """User login endpoint"""
    session_gen = get_session()
    session = next(session_gen)
    try:
        stmt = select(User).where(User.email == user.email)
        db_user = session.execute(stmt).scalar_one_or_none()
        
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not verify_password(user.password, db_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Convert UUID to integer for backward compatibility
        user_id_int = int(db_user.id.int) if hasattr(db_user.id, 'int') else 1
        
        access_token = create_access_token(
            data={"sub": str(db_user.id), "user_id": user_id_int}
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user_id_int,
            email=db_user.email,
            name=db_user.username,
            role="user"  # Default role for now
        )
    finally:
        try:
            next(session_gen)
        except StopIteration:
            pass

@router.post("/auth/register", response_model=TokenResponse)
async def register(user: UserRegister):
    """User registration endpoint"""
    session_gen = get_session()
    session = next(session_gen)
    try:
        # Check if user already exists
        stmt = select(User).where(User.email == user.email)
        existing_user = session.execute(stmt).scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create new user
        new_user = User(
            email=user.email,
            username=user.name,  # Use name as username
            password_hash=get_password_hash(user.password),
            is_active=True,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        # Convert UUID to integer for backward compatibility
        user_id_int = int(new_user.id.int) if hasattr(new_user.id, 'int') else 1
        
        access_token = create_access_token(
            data={"sub": str(new_user.id), "user_id": user_id_int}
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user_id_int,
            email=new_user.email,
            name=new_user.username,
            role="user"  # Default role for now
        )
    finally:
        try:
            next(session_gen)
        except StopIteration:
            pass