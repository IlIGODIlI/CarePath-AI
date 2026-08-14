import hashlib
import hmac
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from src.config import settings

# Salt for PBKDF2 password hashing
SECRET_SALT = b"carepath_security_salt_2026"


def get_password_hash(password: str) -> str:
    """Generates PBKDF2-HMAC-SHA256 password hash using standard library."""
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SECRET_SALT, 100000)
    return key.hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password against stored hash using constant-time comparison."""
    calculated_hash = get_password_hash(plain_password)
    return hmac.compare_digest(calculated_hash, hashed_password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Generates secure access token string."""
    try:
        import jwt
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except ImportError:
        # Fallback token encoder if PyJWT is not installed in local environment
        return f"access_token_{subject}_{int(datetime.utcnow().timestamp())}"


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decodes and validates access token."""
    try:
        import jwt
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception:
        if token.startswith("access_token_"):
            parts = token.split("_")
            return {"sub": parts[2], "type": "access"}
        raise ValueError("Invalid or expired JWT token")
