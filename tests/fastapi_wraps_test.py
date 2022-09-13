from collections.abc import Awaitable, Callable
from typing import Any, ParamSpec, TypeVar

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient

from fastapi_wraps import fastapi_wraps, get_request, get_response

P = ParamSpec("P")
RT = TypeVar("RT")


def test_decorator_with_request(
    app: FastAPI,
    client: TestClient,
) -> None:
    request: Request | None = None

    def set_request(
        endpoint: Callable[P, Awaitable[RT]],
    ) -> Callable[P, Awaitable[RT]]:
        @fastapi_wraps(endpoint)
        async def wrapper(
            *args: Any,
            __request: Request = Depends(get_request),
            **kwargs: Any,
        ) -> RT:
            nonlocal request
            request = __request
            response = await endpoint(*args, **kwargs)
            return response

        return wrapper

    @app.get("/hello", response_class=PlainTextResponse)
    @set_request
    async def hello() -> str:
        return "hello"

    assert client.get("/hello").text == "hello"
    assert request is not None
    assert request.url.path == "/hello"


def test_decorator_with_request_endpoint_with_request(
    app: FastAPI,
    client: TestClient,
) -> None:
    request: Request | None = None

    def set_request(
        endpoint: Callable[P, Awaitable[RT]],
    ) -> Callable[P, Awaitable[RT]]:
        @fastapi_wraps(endpoint)
        async def wrapper(
            *args: Any,
            __request: Request = Depends(get_request),
            **kwargs: Any,
        ) -> RT:
            nonlocal request
            request = __request
            response = await endpoint(*args, **kwargs)
            return response

        return wrapper

    @app.get("/hello", response_class=PlainTextResponse)
    @set_request
    async def hello(request: Request) -> str:  # pylint: disable=unused-argument
        return "hello"

    assert client.get("/hello").text == "hello"
    assert request is not None
    assert request.url.path == "/hello"


def test_decorator_with_more_dependencies(
    app: FastAPI,
    client: TestClient,
) -> None:
    data: tuple[Request, str, Response] | None = None

    def get_user() -> str:
        return "test-user"

    def dummy_decorator(
        endpoint: Callable[P, Awaitable[RT]],
    ) -> Callable[P, Awaitable[RT]]:
        @fastapi_wraps(endpoint)
        async def wrapper(
            *args: Any,
            __request: Request = Depends(get_request),
            __user: str = Depends(get_user),
            __response: Response = Depends(get_response),
            **kwargs: Any,
        ) -> RT:
            nonlocal data
            __response.status_code = 202
            data = (__request, __user, __response)
            response = await endpoint(*args, **kwargs)
            return response

        return wrapper

    @app.get("/hello", response_class=PlainTextResponse)
    @dummy_decorator
    async def hello() -> str:
        return "hello"

    response = client.get("/hello")
    assert response.text == "hello"

    assert data is not None
    request, user, _ = data  # pylint: disable=unpacking-non-sequence
    assert request.url.path == "/hello"
    assert user == "test-user"
    assert response.status_code == 202
