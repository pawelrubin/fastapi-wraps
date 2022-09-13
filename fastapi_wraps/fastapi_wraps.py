from collections.abc import Callable
from functools import partial, wraps
from inspect import Parameter, signature
from typing import Any, ParamSpec, TypeVar, cast

P = ParamSpec("P")
RT = TypeVar("RT")


def _fastapi_update_wrapper(
    wrapper: Callable[..., Any], wrapped: Callable[P, RT]
) -> Callable[P, RT]:
    wrapped_signature = signature(wrapped)
    wrapped_parameters = list(signature(wrapped).parameters.values())
    wrapper_parameters = [
        param
        # omit *args and **kwargs
        for param in signature(wrapper).parameters.values()
        if param.kind not in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD)
    ]
    combined_parameters = wrapped_parameters + wrapper_parameters

    wrapper = wraps(wrapped)(wrapper)

    wrapper.__signature__ = wrapped_signature.replace(  # type: ignore
        parameters=combined_parameters,
    )

    return cast(Callable[P, RT], wrapper)


def fastapi_wraps(
    wrapped: Callable[P, RT]
) -> Callable[[Callable[..., Any]], Callable[P, RT]]:
    """
    functools.wraps for fastapi endpoints.

    It updates the signature of the wrapped function
    with parameters defined in the decorator.
    All parameters of the wrapper function should have defaults assigned.

    It's advised to name the parameter with some prefix, for example `__`,
    to avoid any name conflicts in decorated functions.

    To use the Request object in the decorator
    use `__request: Request = Depends(get_request)`

    ## Example usage
    ```python
    def print_request(
        endpoint: Callable[P, Awaitable[RT]],
    ) -> Callable[P, Awaitable[RT]]:
        @fastapi_wraps(endpoint)
        async def wrapper(
            __request: Request = Depends(get_request),
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> RT:
            print(__request)
            response = await endpoint(*args, **kwargs)
            return response

        return wrapper

    @app.get("/")
    @print_request
    async def hello():
        return "hello"
    ```
    """
    return partial(_fastapi_update_wrapper, wrapped=wrapped)  # type: ignore
