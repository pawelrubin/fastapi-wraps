from fastapi import Request, Response


def get_request(request: Request) -> Request:
    """
    Request object provider to be used in FastAPI dependencies
    in endpoints decorators.

    ## Example usage
    ```python
    def decorator(endpoint):
        @fastapi_wraps(endpoint)
        async def wrapper(
            *args,
            __request: Request = Depends(get_request),
            **kwargs,
        ) -> RT:
            ...

        return wrapper
    ```
    """
    return request


def get_response(response: Response) -> Response:
    """
    Response object provider to be used in FastAPI dependencies
    in endpoints decorators.

    ## Example usage
    ```python
    def decorator(endpoint):
        @fastapi_wraps(endpoint)
        async def wrapper(
            *args,
            __request: Response = Depends(get_response),
            **kwargs,
        ) -> RT:
            ...

        return wrapper
    ```
    """
    return response
