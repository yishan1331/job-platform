import os
from datetime import timedelta

import pytest
from django.utils import timezone
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken

from api.api import api
from api.models.company import Company
from api.models.job import JobPosting
from api.models.user import User

# 設置環境變量以避免命名空間衝突
os.environ["NINJA_SKIP_REGISTRY"] = "true"


@pytest.fixture
def client():
    return TestClient(api)


@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "role": "recruiter",
        "full_name": "Test User",
    }


@pytest.fixture
def test_user(test_user_data):
    return User.objects.create_user(**test_user_data)


@pytest.fixture
def auth_headers(test_user):
    refresh = RefreshToken.for_user(test_user)
    return {"Authorization": f"Bearer {refresh.access_token}"}


@pytest.fixture
def test_company_data():
    return {
        "name": "Test Company",
        "description": "A test company",
        "website": "https://testcompany.com",
        "location": "Test Location",
    }


@pytest.fixture
def test_company(test_company_data, test_user):
    return Company.objects.create(
        **test_company_data,
        owner=test_user,
        created_by=test_user,
        modified_by=test_user,
    )


@pytest.fixture
def test_job_data():
    now = timezone.now()
    return {
        "title": "Test Job",
        "description": "A test job position",
        "location": "Test Location",
        "min_salary": 50000,
        "max_salary": 70000,
        "salary_type": "annual",
        "required_skills": ["Python", "Django"],
        "posting_date": now,
        "expiration_date": now + timedelta(days=30),
        "type": "full-time",
    }


@pytest.fixture
def test_job(test_job_data, test_company):
    return JobPosting.objects.create(
        **test_job_data,
        company=test_company,
        company_name_cached=test_company.name,
        created_by=test_company.owner,
        modified_by=test_company.owner,
    )
