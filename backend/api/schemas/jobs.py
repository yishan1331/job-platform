from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from django.core.exceptions import ValidationError
from django.utils import timezone
from ninja import Schema
from pydantic import Field, model_validator

from api.models.job import JobPosting


class JobPostingBase(Schema):
    title: str = Field(min_length=1, max_length=64)
    description: str = Field(min_length=1)
    location: str = Field(min_length=1, max_length=512)
    min_salary: int = Field(gt=0)
    max_salary: int = Field(gt=0)
    salary_type: str = Field(choices=JobPosting.SALARY_TYPE_CHOICES)
    required_skills: list[str] = Field(min_length=1, min_items=1, min_length_str=1)
    posting_date: datetime = Field(default_factory=timezone.now)
    expiration_date: Optional[datetime] = None
    apply_url: Optional[str] = None
    type: str = Field(choices=JobPosting.JOB_TYPE_CHOICES)
    company_id: UUID
    company_name_cached: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def strip_all_strings(cls, values: dict):
        new_values = {}
        for key in cls.model_fields:
            value = getattr(values, key, None)
            if isinstance(value, str):
                new_values[key] = value.strip()
            else:
                new_values[key] = value
        return new_values

    @model_validator(mode="after")
    @classmethod
    def check_salary_and_dates(cls, model):
        # 檢查薪資範圍
        if model.min_salary > model.max_salary:
            raise ValidationError("Minimum salary cannot be higher than maximum salary")

        # 檢查日期邏輯
        if model.posting_date and model.expiration_date:
            if model.posting_date > model.expiration_date:
                raise ValidationError("Posting date cannot be later than expiration date")

        # 驗證 salary_type
        valid_salary_types = [choice[0] for choice in JobPosting.SALARY_TYPE_CHOICES]
        if model.salary_type not in valid_salary_types:
            raise ValidationError(
                f"Invalid salary_type. Must be one of: {', '.join(valid_salary_types)}"
            )

        # 驗證 type
        valid_job_types = [choice[0] for choice in JobPosting.JOB_TYPE_CHOICES]
        if model.type not in valid_job_types:
            raise ValidationError(f"Invalid job type. Must be one of: {', '.join(valid_job_types)}")

        return model


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingUpdate(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    salary_type: Optional[str] = None
    required_skills: Optional[list[str]] = None
    posting_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    apply_url: Optional[str] = None
    type: Optional[str] = None
    is_active: Optional[bool] = None


class JobPostingOut(JobPostingBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    company_name: str

    class Config:
        from_attributes = True


class JobQueryParams(Schema):
    search: Optional[str] = None
    status: Optional[Literal["Active", "Expired", "Scheduled"]] = None
    location: Optional[str] = None
    salary_type: Optional[Literal["monthly", "hourly", "annual"]] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    company_id: Optional[UUID] = None
    type: Optional[Literal["full-time", "part-time", "internship"]] = None
    order_by: Optional[
        Literal["posting_date", "-posting_date", "expiration_date", "-expiration_date"]
    ] = None
