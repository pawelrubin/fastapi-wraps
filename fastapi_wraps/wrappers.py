from fastapi import Request, Response


def get_request(request: Request) -> Request:
    return request


def get_response(response: Response) -> Response:
    return response
