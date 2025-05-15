from ninja import Router, Query
from typing import List, Optional
from datetime import datetime
from .models import JobPosting, Company
from .schemas import JobPostingCreate, JobPostingUpdate, JobPostingOut, Error
from ninja.pagination import paginate
from django.shortcuts import get_object_or_404
from uuid import UUID

jobs = Router()

@jobs.post("", response={201: JobPostingOut, 400: Error})
def create_job(request, payload: JobPostingCreate):
    try:
        company = get_object_or_404(Company, id=payload.company_id)
        job = JobPosting.objects.create(
            **payload.dict(),
            company=company,
            created_by=request.auth,
            modified_by=request.auth
        )
        return 201, job
    except Exception as e:
        return 400, {"message": str(e)}

@jobs.get("", response=List[JobPostingOut])
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

@jobs.get("/{job_id}", response={200: JobPostingOut, 404: Error})
def get_job(request, job_id: UUID):
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)
    return job

@jobs.put("/{job_id}", response={200: JobPostingOut, 400: Error, 404: Error})
def update_job(request, job_id: UUID, payload: JobPostingUpdate):
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)

    if job.created_by != request.auth:
        return 400, {"message": "You don't have permission to update this job"}

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(job, attr, value)

    job.modified_by = request.auth
    job.save()
    return job

@jobs.delete("/{job_id}", response={204: None, 400: Error, 404: Error})
def delete_job(request, job_id: UUID):
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)

    if job.created_by != request.auth:
        return 400, {"message": "You don't have permission to delete this job"}

    job.is_active = False
    job.save()
    return 204, None