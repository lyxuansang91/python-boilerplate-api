from uuid import uuid4

from .session import reset_session_context, session, set_session_context


def standalone_session(func):
    def _standalone_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            func(*args, **kwargs)
        except Exception as exception:
            session.rollback()
            raise exception
        finally:
            session.remove()
            reset_session_context(context=context)

    return _standalone_session
