from factory import Factory
from fastapi import APIRouter, Depends, status
from schemas.requests import LoginRequest, RegisterRequest
from schemas.responses import TokenResponse, UserResponse
from services import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login_with_email(
    login_request: LoginRequest,
    auth_service: AuthService = Depends(Factory().get_auth_service),
) -> TokenResponse:
    token_response = auth_service.login(
        email=login_request.email, password=login_request.password
    )

    return TokenResponse(
        access_token=token_response.access_token,
        refresh_token=token_response.refresh_token,
        token_type="bearer",
    )


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_with_email(
    login_request: RegisterRequest,
    auth_service: AuthService = Depends(Factory().get_auth_service),
) -> UserResponse:
    user = auth_service.register(
        email=login_request.email,
        password=login_request.password,
    )

    return UserResponse(
        email=user.email,
        id=user.id,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
