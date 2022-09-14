from collections.abc import Awaitable, Callable
from typing import Any, ParamSpec, TypeVar

from fastapi import Depends, FastAPI, Request

from fastapi_wraps import fastapi_wraps, get_request

P = ParamSpec("P")
RT = TypeVar("RT")


def print_request(
    endpoint: Callable[P, Awaitable[RT]],
) -> Callable[P, Awaitable[RT]]:
    @fastapi_wraps(endpoint)
    async def wrapper(
        *args: Any,
        __request: Request = Depends(get_request),
        **kwargs: Any,
    ) -> RT:
        print(__request)
        response = await endpoint(*args, **kwargs)
        return response

    return wrapper


app = FastAPI()


@app.get("/")
@print_request
async def hello() -> str:
    return "hello"
