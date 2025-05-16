from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema


class JobPostingBase(Schema):
    title: str
    description: str
    location: str
    salary_range: dict
    salary_type: str
    required_skills: list[str]
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
    required_skills: Optional[list[str]] = None
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
    items: list[JobPostingOut]
    total: int
    page: int
    page_size: int
