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

from db.postgres.engine import get_session
from db.postgres.models.user import User

router = APIRouter(prefix="/api")
security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
            is_active=True
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