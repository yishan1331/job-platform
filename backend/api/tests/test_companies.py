from uuid import UUID

import pytest

from api.models.company import Company


@pytest.mark.django_db
class TestCompanyAPI:
    def test_create_company_success(self, client, test_company_data, test_user, auth_headers):
        """Test successful company creation"""
        # Use different name
        test_company_data = test_company_data.copy()
        test_company_data["name"] = "New Company"
        test_company_data["owner_id"] = str(test_user.id)

        response = client.post("/companies", json=test_company_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == test_company_data["name"]
        assert data["location"] == test_company_data["location"]
        assert data["description"] == test_company_data["description"]
        assert data["website"] == test_company_data["website"]
        assert data["owner_id"] == str(test_user.id)

    def test_create_company_duplicate_name(
        self, client, test_company, test_company_data, test_user, auth_headers
    ):
        """Test creating company with duplicate name"""
        test_company_data["owner_id"] = str(test_user.id)
        response = client.post("/companies", json=test_company_data, headers=auth_headers)
        assert response.status_code == 409
        assert "name" in response.json()["message"].lower()

    def test_create_company_invalid_data(self, client, auth_headers):
        """Test creating company with invalid data"""
        invalid_data = {
            "name": "Test Company",  # Missing required fields
            "location": "Test Location",
            "website": "invalid-url",  # Invalid URL format
        }
        response = client.post("/companies", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_get_company_list(self, client, test_company, auth_headers):
        """Test getting company list"""
        response = client.get("/companies", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == test_company.name

    def test_get_company_list_pagination(self, client, test_user, auth_headers):
        """Test company list pagination"""
        # Create multiple companies
        for i in range(15):
            Company.objects.create(
                name=f"Company {i}",
                location=f"Location {i}",
                description=f"Description {i}",
                website=f"https://company{i}.com",
                owner=test_user,
                created_by=test_user,
                modified_by=test_user,
            )

        # Test first page
        response = client.get("/companies?page=1&page_size=10", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["count"] > 10

        # Test second page
        response = client.get("/companies?page=2&page_size=10", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

    def test_get_company_detail(self, client, test_company, auth_headers):
        """Test getting company details"""
        response = client.get(f"/companies/{test_company.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_company.name
        assert data["location"] == test_company.location
        assert data["description"] == test_company.description
        assert data["website"] == test_company.website

    def test_get_nonexistent_company(self, client, auth_headers):
        """Test getting non-existent company"""
        response = client.get(
            f"/companies/{UUID('00000000-0000-0000-0000-000000000000')}",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_update_company_success(self, client, test_company, auth_headers):
        """Test successful company update"""
        update_data = {
            "location": "Updated Location",
            "description": "Updated Description",
            "website": "https://updated.com",
        }
        response = client.put(
            f"/companies/{test_company.id}", json=update_data, headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["location"] == update_data["location"]
        assert data["description"] == update_data["description"]
        assert data["website"] == update_data["website"]

    def test_update_nonexistent_company(self, client, auth_headers):
        """Test updating non-existent company"""
        response = client.put(
            f"/companies/{UUID('00000000-0000-0000-0000-000000000000')}",
            json={"location": "New Location"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_delete_company_success(self, client, test_company, auth_headers):
        """Test successful company deletion"""
        response = client.delete(f"/companies/{test_company.id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify company is soft deleted
        company = Company.objects.get(id=test_company.id)
        assert not company.is_active

    def test_delete_nonexistent_company(self, client, auth_headers):
        """Test deleting non-existent company"""
        response = client.delete(
            f"/companies/{UUID('00000000-0000-0000-0000-000000000000')}",
            headers=auth_headers,
        )
        assert response.status_code == 404
