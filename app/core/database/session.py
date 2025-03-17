from contextvars import ContextVar, Token

from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, scoped_session, sessionmaker
from sqlalchemy.sql.expression import Delete, Insert, Update

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engines = {
    "writer": create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_recycle=3600),
    "reader": create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_recycle=3600),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        if self._flushing or isinstance(clause, Update | Delete | Insert):
            return engines["writer"]
        return engines["reader"]


session_factory = sessionmaker(
    class_=Session,
    expire_on_commit=False,
)

session: Session = scoped_session(
    session_factory=session_factory,
    scopefunc=get_session_context,
)


def get_session():
    """
    Get the database session.
    This can be used for dependency injection.

    :return: The database session.
    """
    try:
        yield session
    finally:
        session.remove()


Base = declarative_base()
