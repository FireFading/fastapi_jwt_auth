from fastapi import status

from tests.config import test_user


class TestRegister:
    def test_successful_register(self, client):
        response = client.post(
            "/accounts/signup",
            json={
                "username": test_user.username,
                "password": test_user.password,
                "email": test_user.email,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED


class TestLogin:
    def test_login_unregistered_user(self, client):
        response = client.post(
            "/accounts/login",
            json={
                "username": test_user.wrong_username,
                "password": test_user.wrong_password,
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_successful_login(self, client):
        response = client.post(
            "/accounts/login",
            json={
                "username": test_user.username,
                "password": test_user.password,
            },
        )
        assert response.status_code == status.HTTP_200_OK

        result = response.json()
        assert result.get("access_token") is not None
        assert result.get("refresh_token") is not None


class TestJWT:
    def test_get_route_without_auth_headers(self, client):
        response = client.get("/accounts/users")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_successful_get_with_auth_headers(self, auth_client):
        response = auth_client.get("/accounts/users")
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 1
        assert result[0].get("username") == test_user.username
        assert result[0].get("email") == test_user.email

    def test_get_new_access_token(self, auth_refresh_client):
        response = auth_refresh_client.get("/accounts/new_token")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("new_access_token") is not None

    def test_get_current_user(self, auth_client):
        response = auth_client.get("/accounts/protected")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("current_user") == test_user.username
