from typing import Literal

from pydantic import BaseModel, EmailStr

from app.application.dto import TokenPair


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    # Public sign-up may only claim the attendee or organizer role; artist and
    # admin are granted through other flows.
    role: Literal["attendee", "organizer"] = "attendee"


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
