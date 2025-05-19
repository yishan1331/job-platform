from uuid import UUID

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Query, Router
from ninja.pagination import PageNumberPagination, paginate

from ..error_handlers import ErrorResponse
from ..models.company import Company
from ..models.job import JobPosting
from ..schemas.jobs import JobPostingCreate, JobPostingOut, JobPostingUpdate, JobQueryParams

jobs = Router(tags=["Jobs"])


def get_search_config():
    return "simple"  # 使用簡單的搜尋配置


@jobs.post(
    "",
    response={
        201: JobPostingOut,
        422: ErrorResponse,
        403: ErrorResponse,
        409: ErrorResponse,
        500: ErrorResponse,
    },
    summary="Create a Job",
)
def create_job(request, payload: JobPostingCreate):
    company = get_object_or_404(Company, id=payload.company_id, is_active=True)

    if not company.owner == request.user and not request.user.is_superuser:
        return 403, {"message": "You don't have permission to post jobs for this company"}

    if JobPosting.objects.exists_duplicate_title(company, payload.title):
        return 409, {"message": "A job with this title already exists for this company"}

    # 創建職缺
    job = JobPosting(
        title=payload.title,
        description=payload.description,
        location=payload.location,
        min_salary=payload.min_salary,
        max_salary=payload.max_salary,
        salary_type=payload.salary_type,
        required_skills=payload.required_skills,
        posting_date=payload.posting_date,
        expiration_date=payload.expiration_date,
        apply_url=payload.apply_url,
        type=payload.type,
        company=company,
        company_name_cached=company.name,
        created_by=request.user,
        modified_by=request.user,
    )

    # 先保存基本資料
    job.save()

    try:
        # 更新 search_vector
        search_config = get_search_config()
        job.search_vector = (
            SearchVector("title", weight="A", config=search_config)
            + SearchVector("description", weight="B", config=search_config)
            + SearchVector("company_name_cached", weight="A", config=search_config)
        )
        job.save()
    except Exception as e:
        return 500, {"message": "Failed to create job", "error": str(e)}

    return 201, job


@jobs.get(
    "",
    response={200: list[JobPostingOut], 422: ErrorResponse, 500: ErrorResponse},
    summary="Get Job List",
)
@paginate(PageNumberPagination)
def list_jobs(request, filters: Query[JobQueryParams]):
    queryset = JobPosting.objects.select_related("company").filter(is_active=True)

    # 全文搜尋
    if filters.search:
        search_config = get_search_config()
        search_vector = (
            SearchVector("title", weight="A", config=search_config)
            + SearchVector("description", weight="B", config=search_config)
            + SearchVector("company_name_cached", weight="A", config=search_config)
        )
        search_query = SearchQuery(filters.search, config=search_config)
        qs = (
            queryset.annotate(rank=SearchRank(search_vector, search_query))
            .filter(rank__gte=0.1)
            .order_by("-rank")
        )
        if not qs.exists():
            # fallback to fuzzy search
            qs = queryset.filter(
                Q(title__icontains=filters.search)
                | Q(description__icontains=filters.search)
                | Q(company_name_cached__icontains=filters.search)
            )
        queryset = qs

    # 狀態過濾
    now = timezone.now()
    if filters.status == "Active":
        queryset = queryset.filter(is_active=True, expiration_date__gt=now)
    elif filters.status == "Expired":
        queryset = queryset.filter(expiration_date__lte=now)
    elif filters.status == "Scheduled":
        queryset = queryset.filter(posting_date__gt=now)

    if filters.location:
        queryset = queryset.filter(location__icontains=filters.location)

    if filters.salary_type:
        queryset = queryset.filter(salary_type=filters.salary_type)

    if filters.min_salary:
        queryset = queryset.filter(min_salary__gte=filters.min_salary)

    if filters.max_salary:
        queryset = queryset.filter(max_salary__lte=filters.max_salary)

    if filters.company_id:
        queryset = queryset.filter(company_id=filters.company_id)

    if filters.type:
        queryset = queryset.filter(type=filters.type)

    # 排序，支援前綴 + 或 -
    if filters.order_by:
        valid_fields = ["posting_date", "expiration_date"]
        # 支援帶 + 或 - 符號
        field = filters.order_by.lstrip("+-")
        if field not in valid_fields:
            return 422, {"message": "Invalid ordering value"}
        queryset = queryset.order_by(filters.order_by)
    else:
        queryset = queryset.order_by("-posting_date")

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
    job = get_object_or_404(JobPosting, id=job_id)
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(job, key, value)
    job.modified_by = request.user
    job.save()

    # 更新 search_vector
    try:
        search_config = get_search_config()
        job.search_vector = (
            SearchVector("title", weight="A", config=search_config)
            + SearchVector("description", weight="B", config=search_config)
            + SearchVector("company_name_cached", weight="A", config=search_config)
        )
        job.save()
    except Exception as e:
        return 500, {"message": "Failed to update job", "error": str(e)}

    return job


@jobs.delete(
    "/{job_id}",
    response={204: None, 404: ErrorResponse, 500: ErrorResponse},
    summary="Delete a Job",
)
def delete_job(request, job_id: UUID):
    job = get_object_or_404(JobPosting, id=job_id)
    job.is_active = False
    job.deleted_at = timezone.now()
    job.modified_by = request.user
    job.save()
    return 204, None
