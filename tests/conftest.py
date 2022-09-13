import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    return FastAPI()


@pytest.fixture
def client(app: FastAPI) -> TestClient:  # pylint: disable=redefined-outer-name
    return TestClient(app)
