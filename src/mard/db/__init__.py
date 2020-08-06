from mard.config import Config
from mard.db.email import Email
from mard.db.model import Model
from mard.db.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session

engine = create_engine(Config.DB_URI, echo=True)
Model.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
scoped_session_factory = scoped_session(session_factory)


def get_session() -> Session:
	return scoped_session_factory()


__all__ = [
	User, Email, get_session
]
