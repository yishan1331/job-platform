from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr


class UserBase(Schema):
    email: EmailStr
    username: str
    role: Literal["applicant", "recruiter", "admin"]
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(Schema):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: UUID
    is_active: bool
    username: str
    role: Optional[Literal["applicant", "recruiter", "admin"]] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
