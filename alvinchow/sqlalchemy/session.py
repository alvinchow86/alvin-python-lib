from alvinchow.sqlalchemy.exceptions import DatabaseError


from sqlalchemy.exc import SQLAlchemyError


def commit_session_or_raise(session, exception=DatabaseError):
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        if exception:
            raise exception(str(e))
        else:
            print(exception)
            raise
