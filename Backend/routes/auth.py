from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from config.database import db
from passlib.context import CryptContext
from auth.jwt_handler import create_access_token  # <-- Add this line

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(user: UserLogin):
    # Find user by email
    existing_user = await db.users.find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not pwd_context.verify(user.password, existing_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate JWT token
    token = create_access_token({"sub": existing_user["email"]})

    return {
        "message": "Login successful",
        "name": existing_user["name"],
        "email": existing_user["email"],
        "token": token  # <-- Return token here
    }
