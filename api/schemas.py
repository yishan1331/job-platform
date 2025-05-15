from typing import List, Optional
from ninja import Schema
from datetime import datetime
from uuid import UUID

class JobPostingBase(Schema):
    title: str
    description: str
    location: str
    salary_range: dict
    salary_type: str
    required_skills: List[str]
    posting_date: datetime
    expiration_date: Optional[datetime] = None
    apply_url: Optional[str] = None
    type: Optional[str] = None
    company_id: UUID

class JobPostingCreate(JobPostingBase):
    pass

class JobPostingUpdate(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[dict] = None
    salary_type: Optional[str] = None
    required_skills: Optional[List[str]] = None
    posting_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    apply_url: Optional[str] = None
    type: Optional[str] = None

class JobPostingOut(JobPostingBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    company_name: str

    class Config:
        from_attributes = True

class JobPostingList(Schema):
    items: List[JobPostingOut]
    total: int
    page: int
    page_size: int

class Error(Schema):
    message: str

class UserBase(Schema):
    email: str
    username: str
    role: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(Schema):
    email: Optional[str] = None
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

class CompanyBase(Schema):
    name: str
    location: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None

class CompanyCreate(CompanyBase):
    owner_id: UUID

class CompanyUpdate(Schema):
    location: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None

class CompanyOut(CompanyBase):
    id: UUID
    owner_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True