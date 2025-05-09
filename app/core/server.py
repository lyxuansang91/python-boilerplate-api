from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.exceptions import CustomException
from app.core.fastapi.dependencies import Logging
from app.core.fastapi.middlewares import (
    ResponseLoggerMiddleware,
)


def init_routers(app_: FastAPI) -> None:
    app_.include_router(api_router)


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(_: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(ResponseLoggerMiddleware),
    ]
    return middleware


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        description="FastAPI Boilerplate API",
        generate_unique_id_function=custom_generate_unique_id,
        version="1.0.0",
        docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_
