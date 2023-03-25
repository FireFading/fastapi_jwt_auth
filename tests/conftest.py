from collections.abc import Generator

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from main import app as main_app

from tests.config import test_user


@pytest.fixture
def app() -> Generator:
    yield main_app


@pytest.fixture
def client(app: FastAPI) -> Generator | TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture
def register_user(client: Generator | TestClient) -> None:
    response = client.post(
        "/accounts/signup",
        json={
            "username": test_user.username,
            "password": test_user.password,
            "email": test_user.email,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.fixture
def auth_client(client: Generator | TestClient) -> Generator | TestClient:
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
    access_token = response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client


@pytest.fixture
def auth_refresh_client(client: Generator | TestClient) -> Generator | TestClient:
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
    refresh_token = response.json().get("refresh_token")
    client.headers.update({"Authorization": f"Bearer {refresh_token}"})
    yield client
