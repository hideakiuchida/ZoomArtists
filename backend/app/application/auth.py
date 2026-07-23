"""Authentication use cases."""

from __future__ import annotations

from uuid import uuid4

from app.application.dto import LoginCommand, RegisterCommand, TokenPair
from app.application.ports import PasswordHasher, TokenService, UserRepository
from app.domain.entities import User
from app.domain.errors import AuthenticationError, ConflictError


def _issue_tokens(tokens: TokenService, user_id: str) -> TokenPair:
    return TokenPair(
        access_token=tokens.create_access_token(user_id),
        refresh_token=tokens.create_refresh_token(user_id),
    )


class RegisterUser:
    def __init__(self, users: UserRepository, hasher: PasswordHasher, tokens: TokenService) -> None:
        self._users = users
        self._hasher = hasher
        self._tokens = tokens

    async def execute(self, cmd: RegisterCommand) -> TokenPair:
        if await self._users.get_by_email(cmd.email):
            raise ConflictError("Email already registered")

        user = User(
            id=str(uuid4()),
            email=cmd.email,
            name=cmd.name,
            role=cmd.role,
            hashed_password=self._hasher.hash(cmd.password),
        )
        user = await self._users.add(user)
        return _issue_tokens(self._tokens, user.id)


class LoginUser:
    def __init__(self, users: UserRepository, hasher: PasswordHasher, tokens: TokenService) -> None:
        self._users = users
        self._hasher = hasher
        self._tokens = tokens

    async def execute(self, cmd: LoginCommand) -> TokenPair:
        user = await self._users.get_by_email(cmd.email)
        if not user or not self._hasher.verify(cmd.password, user.hashed_password or ""):
            raise AuthenticationError("Invalid credentials")
        return _issue_tokens(self._tokens, user.id)


class RefreshTokens:
    def __init__(self, users: UserRepository, tokens: TokenService) -> None:
        self._users = users
        self._tokens = tokens

    async def execute(self, refresh_token: str) -> TokenPair:
        user_id = self._tokens.decode(refresh_token)
        if not user_id:
            raise AuthenticationError("Invalid refresh token")

        user = await self._users.get_by_id(user_id)
        if not user or not user.is_active:
            raise AuthenticationError("User not found")
        return _issue_tokens(self._tokens, user.id)


class AuthenticateToken:
    """Resolve a bearer access token to the active user behind it."""

    def __init__(self, users: UserRepository, tokens: TokenService) -> None:
        self._users = users
        self._tokens = tokens

    async def execute(self, access_token: str) -> User:
        user_id = self._tokens.decode(access_token)
        if not user_id:
            raise AuthenticationError("Invalid token")

        user = await self._users.get_by_id(user_id)
        if not user or not user.is_active:
            raise AuthenticationError("User not found")
        return user
