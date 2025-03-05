from fastapi import APIRouter, HTTPException
from src.api.models.user import UserCreate, UserLogin
from src.services.user_service import register_user, login_user

router = APIRouter()

# Skeleton structure, it can be made better or updated if need be


@router.post("/register")
async def register(user_data: UserCreate):
    result = await register_user(user_data)
    if not result:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered successfully"}


@router.post("/login")
async def login(user_data: UserLogin):
    token = await login_user(user_data)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
