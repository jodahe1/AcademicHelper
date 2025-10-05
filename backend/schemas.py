from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    student_id: str

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
