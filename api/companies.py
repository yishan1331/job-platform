from ninja import Router
from ninja.pagination import paginate
from typing import List
from django.shortcuts import get_object_or_404
from .models import Company, User
from .schemas import CompanyCreate, CompanyUpdate, CompanyOut, Error
from uuid import UUID

companies = Router(tags=["Companies"])

@companies.post("", response={201: CompanyOut, 400: Error}, summary="Create a Company")
def create_company(request, payload: CompanyCreate):
    try:
        owner = get_object_or_404(User, id=payload.owner_id, is_active=True)
        company = Company.objects.create(
            name=payload.name,
            location=payload.location,
            description=payload.description,
            website=payload.website,
            logo_url=payload.logo_url,
            owner=owner,
            created_by=owner,
            modified_by=owner
        )
        return 201, company
    except Exception as e:
        return 400, {"message": str(e)}

@companies.get("", response=List[CompanyOut], summary="Get Company List")
@paginate
def list_companies(request):
    return Company.objects.filter(is_active=True)

@companies.get("/{company_id}", response={200: CompanyOut, 404: Error}, summary="Get a Company")
def get_company(request, company_id: UUID):
    company = get_object_or_404(Company, id=company_id, is_active=True)
    return company

@companies.put("/{company_id}", response={200: CompanyOut, 400: Error, 404: Error}, summary="Update a Company")
def update_company(request, company_id: UUID, payload: CompanyUpdate):
    try:
        company = get_object_or_404(Company, id=company_id, is_active=True)
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(company, key, value)
        company.save()
        return company
    except Exception as e:
        return 400, {"message": str(e)}

@companies.delete("/{company_id}", response={204: None, 404: Error}, summary="Delete a Company")
def delete_company(request, company_id: UUID):
    company = get_object_or_404(Company, id=company_id, is_active=True)
    company.is_active = False
    company.save()
    return 204, None