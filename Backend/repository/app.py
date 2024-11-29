from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from repository.user_repository import UserRepository
from repository.utils import hash_password

app = FastAPI()

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

@app.post("/api/register", status_code=201)
async def register_user(request: RegisterRequest):
    repo = UserRepository()
    
    # проверяем занятость мэйла
    existing_user = repo.get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use")
    
    # Hash на пароль
    hashed_password = hash_password(request.password)
    
    # создаем user
    user = repo.create_user(request.email, hashed_password, username=request.username)
    if not user:
        raise HTTPException(status_code=400, detail="Failed to create user")
    
    return {"message": "User registered successfully"}

    