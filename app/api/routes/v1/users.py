from app.deps import get_current_active_admin, get_current_user
from app.factory import Factory
from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from app.models import User
from app.schemas.requests import CreateUserRequest, ForgotPasswordRequest, ResetPasswordRequest, VerifyResetTokenRequest
from app.schemas.responses import PaginatedResponse, UserResponse
from app.services import UserService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserResponse])
def list_users(
    search: str | None = Query(None, description="Search term for email or full name"),
    page: int = Query(1, ge=1, description="Number of items to page"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    current_user: User = Depends(get_current_active_admin),  # No default value
    user_service: UserService = Depends(Factory().get_user_service),
) -> PaginatedResponse[UserResponse]:
    """
    Retrieve a list of users.

    Returns:
    list: A list of dictionaries, each containing the username of a user.
    """
    users, total = user_service.get_users(
        search=search, skip=limit * (page - 1), limit=limit
    )
    return PaginatedResponse[UserResponse](
        items=users,
        total=total,
        page=page,
        limit=limit,
        size=len(users),
        pages=total // limit if total % limit == 0 else total // limit + 1,
    )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    create_request: CreateUserRequest,
    current_user: User = Depends(get_current_active_admin),  # No default value
    user_service: UserService = Depends(Factory().get_user_service),
) -> UserResponse:
    """
    Create a new user (Admin only).

    Parameters:
    - create_request: The data for the new user.
    - current_user: The currently authenticated admin user.

    Returns:
    - The created user.
    """
    # Check if the email already exists
    existing_user = user_service.get_by_email(create_request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    # Create the new user
    new_user = user_service.create_user(
        {
            "email": create_request.email,
            "password": create_request.password,
            "role": create_request.role,
        }
    )

    return new_user


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(
    request: ForgotPasswordRequest,
    user_service: UserService = Depends(Factory().get_user_service),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> dict:
    """
    Handle forgot password requests.

    Parameters:
    - request: The request containing the email of the user requesting a password reset.

    Returns:
    - A message indicating the password reset process has started.
    """
    # Check if the user exists
    user = user_service.get_by_email(request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist.",
        )

    # Trigger password reset process (e.g., send email with reset link), temporary solution
    background_tasks.add_task(user_service.trigger_password_reset, user)
    return {"message": "Password reset instructions have been sent to your email."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(
    request: ResetPasswordRequest,
    # current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(Factory().get_user_service),
) -> dict:
    """
    Handle password reset requests.

    Parameters:
    - token: The password reset token.
    - new_password: The new password.

    Returns:
    - A message indicating the password has been reset.
    """
    # Reset the password
    try:
    
        user_service.reset_password(request.token, request.new_password)
        return {"message": "Password has been reset."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/verify-reset-token", status_code=status.HTTP_200_OK)
def verify_reset_token(
    request: VerifyResetTokenRequest,
    user_service: UserService = Depends(Factory().get_user_service),
) -> dict:
    is_verifed = user_service.verify_reset_token(request.token)
    return {"is_verified": is_verifed}
