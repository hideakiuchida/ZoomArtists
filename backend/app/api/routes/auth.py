from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user,
    get_password_hasher,
    get_token_service,
    get_user_repository,
)
from app.api.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.api.schemas.user import UserResponse
from app.application.auth import LoginUser, RefreshTokens, RegisterUser
from app.application.dto import LoginCommand, RegisterCommand
from app.application.ports import PasswordHasher, TokenService, UserRepository
from app.domain.entities import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    users: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    tokens: TokenService = Depends(get_token_service),
):
    pair = await RegisterUser(users, hasher, tokens).execute(
        RegisterCommand(email=body.email, name=body.name, password=body.password)
    )
    return TokenResponse.from_pair(pair)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    users: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    tokens: TokenService = Depends(get_token_service),
):
    pair = await LoginUser(users, hasher, tokens).execute(
        LoginCommand(email=body.email, password=body.password)
    )
    return TokenResponse.from_pair(pair)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    body: RefreshRequest,
    users: UserRepository = Depends(get_user_repository),
    tokens: TokenService = Depends(get_token_service),
):
    pair = await RefreshTokens(users, tokens).execute(body.refresh_token)
    return TokenResponse.from_pair(pair)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return UserResponse.from_entity(current_user)
