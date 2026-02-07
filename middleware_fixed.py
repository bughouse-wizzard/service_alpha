import os
import jwt
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Dict, Any

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Public paths that don't require authentication
        self.excluded_paths = [
            "/",
            "/health",
            "/api/auth/login",
            "/api/auth/register",
            "/api/auth/refresh",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/assets/",
            "/static/",
        ]

    async def dispatch(self, request: Request, call_next):
        # Check if path is excluded
        path = request.url.path.rstrip("/")
        for excluded in self.excluded_paths:
            excluded_stripped = excluded.rstrip("/")
            if path == excluded_stripped or path.startswith(excluded_stripped + "/"):
                return await call_next(request)

        # Get authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication credentials"}
            )

        token = auth_header.split(" ")[1]

        try:
            # Decode token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Extract user information from token
            # Handle both formats: sub as email or sub as user_id
            user_id = payload.get("sub")
            if isinstance(user_id, str) and "@" in user_id:
                # sub is email, extract user_id from payload
                user_id = payload.get("user_id")
            
            if not user_id:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token payload"}
                )

            # Add user info to request state
            request.state.user_id = user_id
            request.state.user_email = payload.get("email", "")
            request.state.user_role = payload.get("role", "user")

            return await call_next(request)

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token has expired"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"}
            )
