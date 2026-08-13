from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.connections import get_db
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

class AuthLogin(BaseModel):
    email: str
    password: str

class AuthRegister(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(credentials: AuthLogin, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Returning a mock token for simplicity; integrating full JWT is out of scope for just connecting DB
    return {
        "token": f"mock_jwt_token_for_{user.user_id}",
        "user": {
            "id": str(user.user_id),
            "email": user.email,
            "role": user.role
        }
    }

@router.post("/register")
def register(credentials: AuthRegister, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, credentials.email, credentials.password)
    db.commit()
    return {
        "message": "User registered successfully",
        "user_id": str(user.user_id)
    }

@router.get("/profile")
def get_profile(db: Session = Depends(get_db)):
    # Mocking profile retrieval; typically depends on JWT extraction
    return {"message": "Profile would be returned here"}
