from typing import Optional
from uuid import UUID

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Router
from ninja.pagination import PageNumberPagination, paginate

from ..error_handlers import ErrorResponse
from ..models.company import Company
from ..models.job import JobPosting
from ..schemas.jobs import JobPostingCreate, JobPostingOut, JobPostingUpdate

jobs = Router(tags=["Jobs"])


@jobs.post(
    "",
    response={201: JobPostingOut, 422: ErrorResponse, 409: ErrorResponse, 500: ErrorResponse},
    summary="Create a Job",
)
def create_job(request, payload: JobPostingCreate):
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
        created_by=request.user,
        modified_by=request.user,
    )
    return 201, job


@jobs.get(
    "",
    response={200: list[JobPostingOut], 422: ErrorResponse, 500: ErrorResponse},
    summary="Get Job List",
)
@paginate(PageNumberPagination)
def list_jobs(
    request,
    search: Optional[str] = None,
    status: Optional[str] = None,
    ordering: Optional[str] = None,
):
    queryset = JobPosting.objects.all()

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(company__name__icontains=search)
        )

    if status:
        now = timezone.now()
        if status == "active":
            queryset = queryset.filter(is_active=True)
        elif status == "inactive":
            queryset = queryset.filter(is_active=False)
        elif status == "expired":
            queryset = queryset.filter(expiration_date__lte=now)
        elif status == "scheduled":
            queryset = queryset.filter(posting_date__gt=now)

    if ordering:
        valid_ordering = ["posting_date", "expiration_date"]
        if ordering not in valid_ordering:
            return 422, {"message": "Invalid ordering value"}
        queryset = queryset.order_by(ordering)

    return queryset


@jobs.get(
    "/{job_id}",
    response={200: JobPostingOut, 404: ErrorResponse, 500: ErrorResponse},
    summary="Get a Job",
)
def get_job(request, job_id: UUID):
    return get_object_or_404(JobPosting, id=job_id, is_active=True)


@jobs.put(
    "/{job_id}",
    response={200: JobPostingOut, 400: ErrorResponse, 404: ErrorResponse, 500: ErrorResponse},
    summary="Update a Job",
)
def update_job(request, job_id: UUID, payload: JobPostingUpdate):
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(job, key, value)
    job.modified_by = request.user
    job.save()
    return job


@jobs.delete(
    "/{job_id}",
    response={204: None, 404: ErrorResponse, 500: ErrorResponse},
    summary="Delete a Job",
)
def delete_job(request, job_id: UUID):
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)
    job.is_active = False
    job.deleted_at = timezone.now()
    job.modified_by = request.user
    job.save()
    return 204, None
