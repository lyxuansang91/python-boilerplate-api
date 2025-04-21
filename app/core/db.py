from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_size=5,
    pool_pre_ping=True,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=settings.ENVIRONMENT == "local",
)


def init_db(_: Session):
    pass


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
