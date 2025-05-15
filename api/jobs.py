from ninja import Router, Query
from typing import List, Optional
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import JobPosting, Company
from .schemas import JobPostingCreate, JobPostingUpdate, JobPostingOut, Error
from ninja.pagination import paginate
from uuid import UUID

jobs = Router(tags=["Jobs"])

@jobs.post("", response={201: JobPostingOut, 400: Error}, summary="Create a Job")
def create_job(request, payload: JobPostingCreate):
    try:
        company = get_object_or_404(Company, id=payload.company_id, is_active=True)
        job = JobPosting.objects.create(
            title=payload.title,
            description=payload.description,
            location=payload.location,
            salary_range=payload.salary_range,
            salary_type=payload.salary_type,
            required_skills=payload.required_skills,
            posting_date=payload.posting_date,
            expiration_date=payload.expiration_date,
            apply_url=payload.apply_url,
            type=payload.type,
            company=company,
            created_by=company.owner,
            modified_by=company.owner
        )
        return 201, job
    except Exception as e:
        return 400, {"message": str(e)}

@jobs.get("", response=List[JobPostingOut], summary="Get Job List")
@paginate
def list_jobs(
    request,
    search: Optional[str] = None,
    status: Optional[str] = None,
    ordering: Optional[str] = None,
):
    queryset = JobPosting.objects.filter(is_active=True)

    if search:
        queryset = queryset.filter(
            title__icontains=search
        ) | queryset.filter(
            description__icontains=search
        ) | queryset.filter(
            company__name__icontains=search
        )

    if status:
        now = datetime.now()
        if status == "active":
            queryset = queryset.filter(
                posting_date__lte=now,
                expiration_date__gt=now
            )
        elif status == "expired":
            queryset = queryset.filter(expiration_date__lte=now)
        elif status == "scheduled":
            queryset = queryset.filter(posting_date__gt=now)

    if ordering:
        if ordering == "posting_date":
            queryset = queryset.order_by("posting_date")
        elif ordering == "expiration_date":
            queryset = queryset.order_by("expiration_date")

    return queryset

@jobs.get("/{job_id}", response={200: JobPostingOut, 404: Error}, summary="Get a Job")
def get_job(request, job_id: UUID):
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)
    return job

@jobs.put("/{job_id}", response={200: JobPostingOut, 400: Error, 404: Error}, summary="Update a Job")
def update_job(request, job_id: UUID, payload: JobPostingUpdate):
    try:
        job = get_object_or_404(JobPosting, id=job_id, is_active=True)
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(job, key, value)
        job.save()
        return job
    except Exception as e:
        return 400, {"message": str(e)}

@jobs.delete("/{job_id}", response={204: None, 404: Error}, summary="Delete a Job")
def delete_job(request, job_id: UUID):
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)
    job.is_active = False
    job.save()
    return 204, None