# fastapi-wraps

[![Python 3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![codecov](https://codecov.io/gh/pawelrubin/fastapi-wraps/branch/main/graph/badge.svg)](https://codecov.io/gh/pawelrubin/fastapi-wraps)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/pawelrubin/fastapi-wraps/blob/main/LICENSE)

`functools.wraps` for endpoints decorators in FastAPI.

It updates the signature of the wrapped function
with parameters defined in the decorator's wrapper function.
All parameters of the wrapper function should have defaults assigned.

It's advised to name the parameter with some prefix, for example `__`,
to avoid any name conflicts in decorated functions.

To use the Request object in the decorator's wrapper function
use `__request: Request = Depends(get_request)`

## Installation

```shell
pip install fastapi-wraps
```

## Example

```python
def save_request(
    endpoint: Callable[P, Awaitable[RT]],
) -> Callable[P, Awaitable[RT]]:
    @fastapi_wraps(endpoint)
    async def wrapper(
        *args: Any,
        __request: Request = Depends(get_request),
        __db: Db = Depends(get_db),
        **kwargs: Any,
    ) -> RT:
        __db.save(__request)
        response = await endpoint(*args, **kwargs)
        return response

    return wrapper


app = FastAPI()


@app.get("/")
@save_request
async def hello() -> str:
    return "hello"
```

## Why?

To use dependencies provided by FastAPI's DI framework all dependencies have to be declared in the signature of the endpoint.
Hence, the decorator cannot simply use `functools.wraps`, as `functools.wraps` maintains the signature of the wrapped function. The `fastapi_wraps` decorator takes updates the resulting signature by merging parameters from the `wrapper` and the `wrapped` function.
