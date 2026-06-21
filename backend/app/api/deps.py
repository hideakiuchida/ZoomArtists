"""Dependency wiring for the HTTP layer.

Providers build concrete adapters (repositories, services) per request and resolve
the current user. Route handlers inject these and assemble use cases — the only
place that knows about both the abstractions and their implementations.
"""

from __future__ import annotations

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.auth import AuthenticateToken
from app.application.ports import (
    ArtistRepository,
    EventRepository,
    PasswordHasher,
    TokenService,
    UserRepository,
    VenueRepository,
)
from app.domain.entities import User, UserRole
from app.domain.errors import PermissionDeniedError
from app.infrastructure.config import settings
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories import (
    SqlAlchemyArtistRepository,
    SqlAlchemyEventRepository,
    SqlAlchemyUserRepository,
    SqlAlchemyVenueRepository,
)
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.infrastructure.security.token_service import JwtTokenService

# Stateless singletons — no per-request state.
_password_hasher = BcryptPasswordHasher()
_token_service = JwtTokenService(settings)


def get_password_hasher() -> PasswordHasher:
    return _password_hasher


def get_token_service() -> TokenService:
    return _token_service


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return SqlAlchemyUserRepository(db)


def get_artist_repository(db: AsyncSession = Depends(get_db)) -> ArtistRepository:
    return SqlAlchemyArtistRepository(db)


def get_venue_repository(db: AsyncSession = Depends(get_db)) -> VenueRepository:
    return SqlAlchemyVenueRepository(db)


def get_event_repository(db: AsyncSession = Depends(get_db)) -> EventRepository:
    return SqlAlchemyEventRepository(db)


_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    users: UserRepository = Depends(get_user_repository),
    tokens: TokenService = Depends(get_token_service),
) -> User:
    return await AuthenticateToken(users, tokens).execute(credentials.credentials)


def require_role(*roles: UserRole):
    async def checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.has_any_role(*roles):
            raise PermissionDeniedError("Insufficient permissions")
        return current_user

    return checker
