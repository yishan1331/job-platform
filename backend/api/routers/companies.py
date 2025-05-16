from datetime import datetime
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import PageNumberPagination, paginate

from ..error_handlers import ErrorResponse
from ..models.company import Company
from ..models.user import User
from ..schemas.companies import CompanyCreate, CompanyOut, CompanyUpdate

companies = Router(tags=["Companies"])


@companies.post(
    "",
    response={201: CompanyOut, 422: ErrorResponse, 409: ErrorResponse, 500: ErrorResponse},
    summary="Create a Company",
)
def create_company(request, payload: CompanyCreate):
    owner = get_object_or_404(User, id=payload.owner_id, is_active=True)
    company = Company.objects.create(
        name=payload.name,
        location=payload.location,
        description=payload.description,
        website=payload.website,
        logo_url=payload.logo_url,
        owner=owner,
        created_by=request.user,
        modified_by=request.user,
    )
    return 201, company


@companies.get(
    "",
    response={200: list[CompanyOut], 422: ErrorResponse, 500: ErrorResponse},
    summary="Get Company List",
)
@paginate(PageNumberPagination)
def list_companies(request):
    return Company.objects.filter(is_active=True)


@companies.get(
    "/{company_id}",
    response={200: CompanyOut, 404: ErrorResponse, 500: ErrorResponse},
    summary="Get a Company",
)
def get_company(request, company_id: UUID):
    return get_object_or_404(Company, id=company_id, is_active=True)


@companies.put(
    "/{company_id}",
    response={200: CompanyOut, 400: ErrorResponse, 404: ErrorResponse, 500: ErrorResponse},
    summary="Update a Company",
)
def update_company(request, company_id: UUID, payload: CompanyUpdate):
    company = get_object_or_404(Company, id=company_id, is_active=True)
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(company, key, value)
    company.modified_by = request.user
    company.save()
    return company


@companies.delete(
    "/{company_id}",
    response={204: None, 404: ErrorResponse, 500: ErrorResponse},
    summary="Delete a Company",
)
def delete_company(request, company_id: UUID):
    company = get_object_or_404(Company, id=company_id, is_active=True)
    company.is_active = False
    company.deleted_at = datetime.now()
    company.modified_by = request.user
    company.save()
    return 204, None
