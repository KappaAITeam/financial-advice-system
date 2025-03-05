from beanie import Document
from pydantic import BaseModel, EmailStr


class User(Document):
    email: EmailStr
    username: str
    password_hash: str

    class Settings:
        collection = "users"


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
