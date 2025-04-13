from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.schemas.responses import PaginatedResponse
from app.models import User
from app.services import CompanyService
from app.schemas.requests import CompanyInDB
from app.factory import factory_instance

from app.deps import get_current_user

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
        code=code, skip=limit * (page - 1), limit=limit)
    return PaginatedResponse[CompanyInDB](
        items=companies,
        total=count,
        page=page,
        limit=limit,
        size=len(companies),
        pages=count // limit if count % limit == 0 else count // limit + 1,
    )
