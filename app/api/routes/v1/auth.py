from factory import Factory
from core.security import get_password_hash
from fastapi import APIRouter, Depends, status
from schemas.requests import LoginRequest, RegisterRequest, UpdateUserRequest
from schemas.responses import TokenResponse, UserResponse
from services import AuthService, UserService

from deps import get_current_user

from schemas.responses import UserResponse
from models import User

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

@router.get("/me", response_model=UserResponse)
def get_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Retrieve the profile of the currently authenticated user.

    Parameters:
    current_user (User): The user object of the currently authenticated user, 
                         obtained through dependency injection.

    Returns:
    UserResponse: The profile information of the current user.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    update_request: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(Factory().get_user_service)
) -> UserResponse:
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