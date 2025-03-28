from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(_: Session):
    pass


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
