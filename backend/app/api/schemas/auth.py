from pydantic import BaseModel, EmailStr

from app.application.dto import TokenPair


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    @classmethod
    def from_pair(cls, pair: TokenPair) -> "TokenResponse":
        return cls(access_token=pair.access_token, refresh_token=pair.refresh_token)
