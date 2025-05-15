from typing import List, Optional, Literal
from ninja import Schema
from pydantic import EmailStr
from datetime import datetime
from uuid import UUID
from .common import PaginatedResponse

class UserBase(Schema):
    email: EmailStr
    username: str
    role: Literal["applicant", "recruiter"]
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
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 用戶列表分頁用
class UserListResponse(PaginatedResponse):
    items: List[UserOut]