# from core.security import get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from app.deps import get_current_user
from app.factory import Factory
from app.models import User
from app.schemas.requests import (
    ChangePasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    UpdateUserRequest,
)
from app.schemas.responses import TokenResponse, UserResponse, UserResponseWithRole
from app.services import AuthService, UserService

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
    try:
        email = login_request.email
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format"
        )

    user = auth_service.register(
        email=email,
        password=login_request.password,
    )

    return UserResponse(
        email=user.email,
        id=user.id,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.get("/me", response_model=UserResponseWithRole)
def get_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponseWithRole:
    """
    Retrieve the profile of the currently authenticated user.

    Parameters:
    current_user (User): The user object of the currently authenticated user,
                         obtained through dependency injection.

    Returns:
    UserResponseWithRole: The profile information of the current user.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    update_request: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(Factory().get_user_service),
) -> UserResponseWithRole:
    """
    Update the profile of the currently authenticated user.

    Parameters:
    update_request (UpdateUserRequest): The data to update the user profile with
    current_user (User): The currently authenticated user
    auth_service (AuthService): The authentication service

    Returns:
    UserResponse: The updated user profile
    """
    update_dict = update_request.model_dump(exclude_unset=True)
    updated_user = user_service.update_user(current_user, update_dict)

    return updated_user


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    change_password_request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(Factory().get_user_service),
) -> dict:
    try:
        user_service.update_password(
            current_user,
            change_password_request.old_password,
            change_password_request.new_password,
        )
        return {"message": "Password changed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(Factory().get_auth_service),
) -> TokenResponse:
    """
    Generate a new access token using refresh token

    Parameters:
    refresh_request (RefreshTokenRequest): Contains the refresh token

    Returns:
    TokenResponse: New access token and refresh token
    """
    try:
        token_response = auth_service.refresh_token(refresh_request.refresh_token)
        return TokenResponse(
            access_token=token_response.access_token,
            # refresh_token=token_response.refresh_token,
            token_type="bearer",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
