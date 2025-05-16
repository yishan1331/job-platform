from datetime import datetime, timedelta
from uuid import UUID

import pytest

from api.models.job import JobPosting


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
        assert data["salary_range"] == test_job_data["salary_range"]
        assert data["salary_type"] == test_job_data["salary_type"]
        assert data["required_skills"] == test_job_data["required_skills"]

    def test_create_job_invalid_data(self, client, auth_headers):
        """Test creating job with invalid data"""
        invalid_data = {
            "title": "Test Job",  # Missing required fields
            "description": "Test Description",
            "location": "Test Location",
            "salary_range": {"min": 1000, "max": 2000},
            "salary_type": "invalid-type",  # Invalid salary type
        }
        response = client.post("/jobs", json=invalid_data, headers=auth_headers)
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
                salary_range={"min": 1000, "max": 2000},
                salary_type="annual",
                required_skills=["Python", "Django"],
                posting_date=datetime.now(),
                expiration_date=datetime.now() + timedelta(days=30),
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
        response = client.get("/jobs?status=active", headers=auth_headers)
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
        response = client.put(
            f"/jobs/{test_job.id}", json=update_data, headers=auth_headers
        )
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
