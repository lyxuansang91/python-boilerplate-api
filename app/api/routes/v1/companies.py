from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.deps import get_current_user
from app.factory import factory_instance
from app.models import User
from app.schemas.requests import CompanyInDB
from app.schemas.responses import PaginatedResponse
from app.services import CompanyService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[CompanyInDB])
def list_companies(
    code: str | None = Query(None, description="Search term for code"),
    page: int = Query(1, ge=1, description="Number of items to page"),
    limit: int = Query(10, ge=1, le=1000, description="Number of items to return"),
    current_user: User = Depends(get_current_user),
    company_service: CompanyService = Depends(factory_instance.get_company_service),
) -> PaginatedResponse[CompanyInDB]:
    """
    Retrieve companies by code.
    """
    companies, count = company_service.get_companies_by_code(
        code=code, skip=limit * (page - 1), limit=limit
    )
    return PaginatedResponse[CompanyInDB](
        items=companies,
        total=count,
        page=page,
        limit=limit,
        size=len(companies),
        pages=count // limit if count % limit == 0 else count // limit + 1,
    )


@router.get("/{company_id}", response_model=CompanyInDB)
def get_company_detail(
    company_id: int,
    current_user: User = Depends(get_current_user),
    company_service: CompanyService = Depends(factory_instance.get_company_service),
) -> CompanyInDB:
    """
    Retrieve detailed information about a specific company by ID.

    Parameters:
    - company_id: The ID of the company to retrieve
    - current_user: The currently authenticated user
    - company_service: The company service instance

    Returns:
    - CompanyDetailResponse: Detailed information about the company

    Raises:
    - HTTPException: If the company is not found
    """
    company = company_service.get_by_id(company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with ID {company_id} not found",
        )
    return company
