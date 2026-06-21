"""Translate domain errors into HTTP responses.

This is the one place where the framework-agnostic error vocabulary of the inner
circles meets HTTP status codes. Business rules raise DomainError subclasses; the
delivery mechanism decides how to render them.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.errors import (
    AuthenticationError,
    ConflictError,
    DomainError,
    NotFoundError,
    PermissionDeniedError,
    ValidationError,
)

_STATUS_BY_ERROR: list[tuple[type[DomainError], int]] = [
    (NotFoundError, 404),
    (ConflictError, 400),
    (ValidationError, 400),
    (AuthenticationError, 401),
    (PermissionDeniedError, 403),
]


def _status_for(exc: DomainError) -> int:
    for error_type, status_code in _STATUS_BY_ERROR:
        if isinstance(exc, error_type):
            return status_code
    return 400


def add_exception_handlers(app: FastAPI) -> None:
    async def handle_domain_error(_: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(status_code=_status_for(exc), content={"detail": exc.message})

    app.add_exception_handler(DomainError, handle_domain_error)
