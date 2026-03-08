from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database import User
import bcrypt
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "meritmind2025secretkey")

def register_user(name: str, email: str, password: str, db: Session):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    user = User(
        name=name,
        email=email,
        password=hashed.decode('utf-8')
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Account created successfully", "name": user.name}

def login_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")
    
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Wrong password")
    
    token = jwt.encode({
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")
    
    return {
        "token": token,
        "name": user.name,
        "email": user.email
    }