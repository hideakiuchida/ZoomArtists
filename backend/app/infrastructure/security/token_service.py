"""JWT implementation of the TokenService port."""

from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.application.ports import TokenService
from app.infrastructure.config import Settings

ALGORITHM = "HS256"


class JwtTokenService(TokenService):
    def __init__(self, settings: Settings) -> None:
        self._secret = settings.SECRET_KEY
        self._access_ttl = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self._refresh_ttl = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    def _encode(self, subject: str, ttl: timedelta, token_type: str) -> str:
        payload = {"sub": subject, "exp": datetime.now(UTC) + ttl, "type": token_type}
        return jwt.encode(payload, self._secret, ALGORITHM)

    def create_access_token(self, subject: str) -> str:
        return self._encode(subject, self._access_ttl, "access")

    def create_refresh_token(self, subject: str) -> str:
        return self._encode(subject, self._refresh_ttl, "refresh")

    def decode(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[ALGORITHM])
            return payload.get("sub")
        except JWTError:
            return None
