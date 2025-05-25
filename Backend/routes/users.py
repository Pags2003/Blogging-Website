from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from config.database import db  # your MongoDB connection
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

@router.post("/signup")
async def signup(user: UserSignup):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Create user document
    user_doc = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_password
    }

    # Insert into DB
    result = await db.users.insert_one(user_doc)

    return {"message": "User created successfully", "user_id": str(result.inserted_id)}
