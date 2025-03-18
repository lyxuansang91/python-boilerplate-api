from sqlmodel import Session, create_engine

from core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(_: Session):
    print("init_db")
