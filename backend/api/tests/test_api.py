import pytest

pytestmark = pytest.mark.django_db


def test_hello_endpoint(client):
    """測試 hello 端點"""
    response = client.get("/hello")
    assert response.status_code == 401  # 因為需要認證


def test_hello_endpoint_with_auth(client, auth_headers):
    """測試需要認證的 hello 端點"""
    response = client.get("/hello", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_handle_ninja_http_error_invalid_json(client, auth_headers):
    """測試處理無效 JSON 的情況"""
    # 模擬發送無效的 JSON 數據
    response = client.post(
        "/users", data="invalid json", content_type="application/json", headers=auth_headers
    )
    assert response.status_code == 400
    data = response.json()
    assert data["message"] == "Invalid JSON format"
    assert data["code"] == "BAD_REQUEST"
    assert data["details"] is not None
    assert "error" in data["details"]
    assert "message" in data["details"]


def test_get_current_user_with_auth(client, auth_headers, test_user):
    """測試獲取當前用戶信息（已認證）"""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_user.id)
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email
    assert data["role"] == test_user.role


def test_get_current_user_without_auth(client):
    """測試獲取當前用戶信息（未認證）"""
    response = client.get("/auth/me")
    assert response.status_code == 401
    data = response.json()
    assert data["message"] == "Unauthorized"
    assert data["code"] == "UNAUTHORIZED"


def test_handle_validation_error(client, auth_headers):
    """測試處理驗證錯誤的情況"""
    # 模擬發送缺少必要欄位的數據
    response = client.post(
        "/users",
        json={},  # 空數據，應該會觸發驗證錯誤
        content_type="application/json",
        headers=auth_headers,
    )
    assert response.status_code == 422
    data = response.json()
    assert data["message"] == "Validation error"
    assert data["code"] == "VALIDATION_ERROR"
    assert "details" in data
    assert "errors" in data["details"]


def test_handle_404_error(client, auth_headers):
    """測試處理 404 錯誤的情況"""
    # 模擬訪問不存在的資源
    response = client.get("/users/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert response.status_code == 404
    data = response.json()
    assert "message" in data
    assert data["code"] == "NOT_FOUND"
    assert "details" in data
