from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import Field


class CompanyBase(Schema):
    name: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=512)
    description: Optional[str] = Field(min_length=1)
    website: Optional[str] = None
    logo_url: Optional[str] = None


class CompanyCreate(CompanyBase):
    owner_id: UUID


class CompanyUpdate(Schema):
    location: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyOut(CompanyBase):
    id: UUID
    owner_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
