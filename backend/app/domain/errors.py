"""Domain errors — the vocabulary business rules use to signal failure.

These are framework-agnostic: they know nothing about HTTP status codes. The
interface-adapter layer (api/errors.py) is responsible for translating them into
transport-specific responses.
"""


class DomainError(Exception):
    """Base class for all domain-level errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):
    """A requested entity does not exist."""


class ConflictError(DomainError):
    """An operation conflicts with current state (e.g. a uniqueness violation)."""


class ValidationError(DomainError):
    """Input violates a business rule."""


class AuthenticationError(DomainError):
    """Credentials are missing or invalid."""


class PermissionDeniedError(DomainError):
    """The actor is authenticated but not allowed to perform the operation."""
