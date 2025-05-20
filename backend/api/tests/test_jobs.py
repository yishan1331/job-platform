import warnings
from datetime import timedelta
from uuid import UUID

import pytest
from django.utils import timezone

from api.models.job import JobPosting

# 忽略特定的警告
warnings.filterwarnings(
    "ignore", message="DateTimeField .* received a naive datetime", category=RuntimeWarning
)


@pytest.mark.django_db
class TestJobAPI:
    def test_create_job_success(self, client, test_company, test_job_data, auth_headers):
        """Test successful job creation"""
        # Use different title
        test_job_data = test_job_data.copy()
        test_job_data["title"] = "New Job Title"
        test_job_data["company_id"] = str(test_company.id)

        response = client.post("/jobs", json=test_job_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == test_job_data["title"]
        assert data["description"] == test_job_data["description"]
        assert data["location"] == test_job_data["location"]
        assert data["min_salary"] == test_job_data["min_salary"]
        assert data["max_salary"] == test_job_data["max_salary"]
        assert data["salary_type"] == test_job_data["salary_type"]
        assert data["required_skills"] == test_job_data["required_skills"]
        assert data["type"] == test_job_data["type"]
        assert data["company_id"] == str(test_company.id)
        assert data["is_active"] is True

    def test_create_job_permission_denied(
        self, client, test_company, test_job_data, test_user2, auth_headers
    ):
        """測試創建職缺時權限不足的情況"""
        # 創建一個新的公司，但不將當前用戶設為擁有者
        test_job_data = test_job_data.copy()
        test_job_data["company_id"] = str(test_company.id)

        # 確保當前用戶不是公司擁有者
        test_company.owner = test_user2
        test_company.save()

        response = client.post("/jobs", json=test_job_data, headers=auth_headers)
        assert response.status_code == 403
        assert "permission" in response.json()["message"].lower()

    def test_create_job_duplicate_title(self, client, test_company, test_job_data, auth_headers):
        """測試創建重複標題的職缺"""
        # 先創建一個職缺
        test_job_data = test_job_data.copy()
        test_job_data["company_id"] = str(test_company.id)
        response = client.post("/jobs", json=test_job_data, headers=auth_headers)
        assert response.status_code == 201

        # 嘗試創建相同標題的職缺
        response = client.post("/jobs", json=test_job_data, headers=auth_headers)
        assert response.status_code == 409
        assert "already exists" in response.json()["message"].lower()

    def test_job_search(self, client, test_company, auth_headers):
        """測試職缺搜尋功能"""
        # 創建多個職缺用於搜尋測試
        jobs = [
            {
                "title": "Python Developer",
                "description": "Looking for a Python expert",
                "location": "Taipei",
                "min_salary": 50000,
                "max_salary": 70000,
                "salary_type": "annual",
                "required_skills": ["Python", "Django"],
                "type": "full-time",
                "company_id": str(test_company.id),
                "posting_date": timezone.now(),
                "expiration_date": timezone.now() + timezone.timedelta(days=30),
            },
            {
                "title": "Java Developer",
                "description": "Looking for a Java expert",
                "location": "Taipei",
                "min_salary": 50000,
                "max_salary": 70000,
                "salary_type": "annual",
                "required_skills": ["Java", "Spring"],
                "type": "full-time",
                "company_id": str(test_company.id),
                "posting_date": timezone.now(),
                "expiration_date": timezone.now() + timezone.timedelta(days=30),
            },
        ]

        for job_data in jobs:
            response = client.post("/jobs", json=job_data, headers=auth_headers)
            assert response.status_code == 201

        # 測試精確搜尋
        response = client.get("/jobs?search=Python", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Python Developer"

        # 測試模糊搜尋
        response = client.get("/jobs?search=Pythn", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 0

    def test_job_status_filters(self, client, test_company, auth_headers):
        """測試職缺狀態過濾"""
        now = timezone.now()

        # 創建已過期的職缺
        expired_job = {
            "title": "Expired Job",
            "description": "This job has expired",
            "location": "Taipei",
            "min_salary": 50000,
            "max_salary": 70000,
            "salary_type": "annual",
            "required_skills": ["Python"],
            "type": "full-time",
            "company_id": str(test_company.id),
            "posting_date": now - timedelta(days=10),
            "expiration_date": now - timedelta(days=10),
            "is_active": True,
        }

        # 創建預定發布的職缺
        scheduled_job = {
            "title": "Scheduled Job",
            "description": "This job is scheduled",
            "location": "Taipei",
            "min_salary": 50000,
            "max_salary": 70000,
            "salary_type": "annual",
            "required_skills": ["Python"],
            "type": "full-time",
            "company_id": str(test_company.id),
            "posting_date": now + timedelta(days=10),
            "is_active": True,
        }

        # 創建職缺
        response = client.post("/jobs", json=expired_job, headers=auth_headers)
        response = client.post("/jobs", json=scheduled_job, headers=auth_headers)

        # 測試過期職缺過濾
        response = client.get("/jobs", headers=auth_headers)
        data = response.json()
        response = client.get("/jobs?status=Expired", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Expired Job"

        # 測試預定發布職缺過濾
        response = client.get("/jobs?status=Scheduled", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Scheduled Job"

    def test_job_ordering(self, client, test_company, auth_headers):
        """測試職缺排序功能"""
        # 創建多個職缺
        jobs = [
            {
                "title": "Job 1",
                "description": "First job",
                "location": "Taipei",
                "min_salary": 50000,
                "max_salary": 70000,
                "salary_type": "annual",
                "required_skills": ["Python"],
                "type": "full-time",
                "company_id": str(test_company.id),
                "posting_date": timezone.now() - timedelta(days=2),
            },
            {
                "title": "Job 2",
                "description": "Second job",
                "location": "Taipei",
                "min_salary": 50000,
                "max_salary": 70000,
                "salary_type": "annual",
                "required_skills": ["Python"],
                "type": "full-time",
                "company_id": str(test_company.id),
                "posting_date": timezone.now() - timedelta(days=1),
            },
        ]

        for job_data in jobs:
            response = client.post("/jobs", json=job_data, headers=auth_headers)
            assert response.status_code == 201

        # 測試按發布日期升序排序
        response = client.get("/jobs?order_by=posting_date", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 2
        assert data["items"][0]["title"] == "Job 1"

        # 測試按發布日期降序排序
        response = client.get("/jobs?order_by=-posting_date", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 2
        assert data["items"][0]["title"] == "Job 2"

        # 測試無效的排序欄位
        response = client.get("/jobs?order_by=invalid_field", headers=auth_headers)
        assert response.status_code == 422

    def test_job_filters(self, client, test_company, auth_headers):
        """測試職缺過濾功能"""
        # 創建測試職缺
        job_data = {
            "title": "Filter Test Job",
            "description": "Test job for filters",
            "location": "Taipei",
            "min_salary": 50000,
            "max_salary": 70000,
            "salary_type": "annual",
            "required_skills": ["Python"],
            "type": "full-time",
            "company_id": str(test_company.id),
            "posting_date": timezone.now(),
            "expiration_date": timezone.now() + timezone.timedelta(days=30),
        }

        response = client.post("/jobs", json=job_data, headers=auth_headers)
        assert response.status_code == 201

        # 測試位置過濾
        response = client.get("/jobs?location=Taipei", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

        # 測試薪資類型過濾
        response = client.get("/jobs?salary_type=annual", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

        # 測試最低薪資過濾
        response = client.get("/jobs?min_salary=40000", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

        # 測試最高薪資過濾
        response = client.get("/jobs?max_salary=80000", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

        # 測試公司 ID 過濾
        response = client.get(f"/jobs?company_id={test_company.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

        # 測試職缺類型過濾
        response = client.get("/jobs?type=full-time", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

    def test_create_job_without_optional_fields(
        self, client, test_company, test_job_data, auth_headers
    ):
        """Test creating job without optional fields"""
        test_job_data = test_job_data.copy()
        test_job_data["company_id"] = str(test_company.id)

        # 移除所有非必填欄位
        optional_fields = ["expiration_date", "apply_url"]
        for field in optional_fields:
            if field in test_job_data:
                del test_job_data[field]

        response = client.post("/jobs", json=test_job_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == test_job_data["title"]
        assert data["expiration_date"] is None
        assert data["apply_url"] is None

    def test_create_job_with_null_optional_fields(
        self, client, test_company, test_job_data, auth_headers
    ):
        """Test creating job with null optional fields"""
        test_job_data = test_job_data.copy()
        test_job_data["company_id"] = str(test_company.id)

        # 設置非必填欄位為 null
        test_job_data["expiration_date"] = None
        test_job_data["apply_url"] = None

        response = client.post("/jobs", json=test_job_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["expiration_date"] is None
        assert data["apply_url"] is None

    def test_create_job_invalid_data_title(self, client, test_job_data, auth_headers):
        """Test creating job with invalid data"""
        invalid_data = test_job_data.copy()
        del invalid_data["title"]
        response = client.post("/jobs", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_create_job_invalid_data_description(self, client, test_job_data, auth_headers):
        """Test creating job with invalid data"""
        invalid_data = test_job_data.copy()
        del invalid_data["description"]
        response = client.post("/jobs", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_create_job_invalid_data_location(self, client, test_job_data, auth_headers):
        """Test creating job with invalid data"""
        invalid_data = test_job_data.copy()
        del invalid_data["location"]
        response = client.post("/jobs", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_create_job_invalid_data_salary_type(self, client, test_job_data, auth_headers):
        """Test creating job with invalid data"""
        invalid_data = test_job_data.copy()
        invalid_data["salary_type"] = "invalid-type"
        response = client.post("/jobs", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_create_job_invalid_data_required_skills(self, client, test_job_data, auth_headers):
        """Test creating job with invalid data"""
        invalid_data = test_job_data.copy()
        invalid_data["required_skills"] = "invalid-skills"
        response = client.post("/jobs", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_create_job_invalid_expiration_date(
        self, client, test_company, test_job_data, auth_headers
    ):
        """Test creating job with invalid expiration date"""
        test_job_data = test_job_data.copy()
        test_job_data["company_id"] = str(test_company.id)
        test_job_data["expiration_date"] = "invalid-date"

        response = client.post("/jobs", json=test_job_data, headers=auth_headers)
        assert response.status_code == 422

    def test_create_job_invalid_job_type(self, client, test_company, test_job_data, auth_headers):
        """Test creating job with invalid job type"""
        test_job_data = test_job_data.copy()
        test_job_data["company_id"] = str(test_company.id)
        test_job_data["type"] = "invalid-type"

        response = client.post("/jobs", json=test_job_data, headers=auth_headers)
        assert response.status_code == 422

    def test_get_job_list(self, client, test_job, auth_headers):
        """Test getting job list"""
        response = client.get("/jobs", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == test_job.title

    def test_get_job_list_pagination(self, client, test_company, auth_headers):
        """Test job list pagination"""
        # Create multiple jobs
        for i in range(15):
            JobPosting.objects.create(
                title=f"Job {i}",
                description=f"Description {i}",
                location="Test Location",
                min_salary=1000,
                max_salary=2000,
                salary_type="annual",
                type="full-time",
                required_skills=["Python", "Django"],
                posting_date=timezone.now(),
                expiration_date=timezone.now() + timezone.timedelta(days=30),
                company=test_company,
                created_by=test_company.owner,
                modified_by=test_company.owner,
            )

        # Test first page
        response = client.get("/jobs?page=1&page_size=10", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["count"] > 10

        # Test second page
        response = client.get("/jobs?page=2&page_size=10", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

    def test_get_job_list_with_filters(self, client, test_job, auth_headers):
        """Test getting job list with filters"""
        # Test search
        response = client.get(f"/jobs?search={test_job.title}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == test_job.title

        # Test status filter
        response = client.get("/jobs?status=Active", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

        # Test ordering
        response = client.get("/jobs?ordering=posting_date", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

    def test_get_job_detail(self, client, test_job, auth_headers):
        """Test getting job details"""
        response = client.get(f"/jobs/{test_job.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_job.title
        assert data["description"] == test_job.description
        assert data["location"] == test_job.location

    def test_get_nonexistent_job(self, client, auth_headers):
        """Test getting non-existent job"""
        response = client.get(
            f"/jobs/{UUID('00000000-0000-0000-0000-000000000000')}",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_update_job_success(self, client, test_job, auth_headers):
        """Test successful job update"""
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "location": "Updated Location",
        }
        response = client.put(f"/jobs/{test_job.id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["location"] == update_data["location"]

    def test_update_nonexistent_job(self, client, auth_headers):
        """Test updating non-existent job"""
        response = client.put(
            f"/jobs/{UUID('00000000-0000-0000-0000-000000000000')}",
            json={"title": "New Title"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_delete_job_success(self, client, test_job, auth_headers):
        """Test successful job deletion"""
        response = client.delete(f"/jobs/{test_job.id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify job is soft deleted
        job = JobPosting.objects.get(id=test_job.id)
        assert not job.is_active

    def test_delete_nonexistent_job(self, client, auth_headers):
        """Test deleting non-existent job"""
        response = client.delete(
            f"/jobs/{UUID('00000000-0000-0000-0000-000000000000')}",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_job_is_expired(self, test_company, test_user):
        """測試職缺是否過期"""
        # 創建一個已過期的職缺
        expired_job = JobPosting.objects.create(
            title="Expired Job",
            description="This job has expired",
            location="Test Location",
            min_salary=50000,
            max_salary=70000,
            salary_type="annual",
            required_skills=["Python", "Django"],
            posting_date=timezone.now() - timedelta(days=30),
            expiration_date=timezone.now() - timedelta(days=1),  # 昨天過期
            type="full-time",
            company=test_company,
            created_by=test_user,
            modified_by=test_user,
        )
        assert expired_job.is_expired is True

        # 創建一個未過期的職缺
        active_job = JobPosting.objects.create(
            title="Active Job",
            description="This job is still active",
            location="Test Location",
            min_salary=50000,
            max_salary=70000,
            salary_type="annual",
            required_skills=["Python", "Django"],
            posting_date=timezone.now(),
            expiration_date=timezone.now() + timedelta(days=30),  # 30天後過期
            type="full-time",
            company=test_company,
            created_by=test_user,
            modified_by=test_user,
        )
        assert active_job.is_expired is False

        # 創建一個沒有過期日期的職缺
        no_expiry_job = JobPosting.objects.create(
            title="No Expiry Job",
            description="This job has no expiration date",
            location="Test Location",
            min_salary=50000,
            max_salary=70000,
            salary_type="annual",
            required_skills=["Python", "Django"],
            posting_date=timezone.now(),
            expiration_date=None,  # 沒有過期日期
            type="full-time",
            company=test_company,
            created_by=test_user,
            modified_by=test_user,
        )
        assert no_expiry_job.is_expired is False


# 在測試中使用帶時區的 datetime
@pytest.fixture
def job_data():
    return {
        "title": "Test Job",
        "description": "Test Description",
        "location": "Test Location",
        "min_salary": 50000,
        "max_salary": 70000,
        "salary_type": "YEARLY",
        "required_skills": ["Python", "Django"],
        "posting_date": timezone.now(),
        "expiration_date": timezone.now() + timezone.timedelta(days=30),
        "type": "FULL_TIME",
        "company_id": "00000000-0000-0000-0000-000000000000",
    }
