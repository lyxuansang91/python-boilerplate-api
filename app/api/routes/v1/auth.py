from factory import Factory
from fastapi import APIRouter, Depends
from schemas.requests import LoginRequest
from schemas.responses import TokenResponse
from services import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login_with_email(
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
