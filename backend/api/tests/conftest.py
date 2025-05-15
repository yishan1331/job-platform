import pytest
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken
import os

from api.api import api
from api.models.user import User
from api.models.company import Company
from api.models.job import JobPosting

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
        "role": "applicant",
        "full_name": "Test User"
    }

@pytest.fixture
def test_company_data():
    return {
        "name": "Test Company",
        "description": "A test company",
        "website": "https://testcompany.com",
        "location": "Test Location"
    }

@pytest.fixture
def test_job_data():
    return {
        "title": "Test Job",
        "description": "A test job position",
        "requirements": "Test requirements",
        "salary_range": "50k-70k",
        "location": "Test Location",
        "job_type": "full-time"
    }

@pytest.fixture
def test_user(test_user_data):
    return User.objects.create_user(**test_user_data)

@pytest.fixture
def auth_headers(test_user):
    refresh = RefreshToken.for_user(test_user)
    return {"Authorization": f"Bearer {refresh.access_token}"}

@pytest.fixture
def test_company(test_company_data):
    return Company.objects.create(**test_company_data)

@pytest.fixture
def test_job(test_job_data, test_company):
    return JobPosting.objects.create(company=test_company, **test_job_data)