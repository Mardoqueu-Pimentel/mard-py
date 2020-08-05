from typing import List

from sqlalchemy import create_engine, Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.orm.session import Session

Base = declarative_base()


class Model(object):

	def __repr__(self):
		obj = {
			'__type__': type(self).__name__
		}
		obj.update({
			col.name: getattr(self, col.name)
			for col in self.__table__.columns
		})

		return repr(obj)


class Email(Base, Model):
	__tablename__ = "email"

	id = Column(Integer, primary_key=True)
	value = Column(String(128), nullable=False)
	user_id = Column(Integer, ForeignKey("user.id"))


class User(Base, Model):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	name = Column(String(128), nullable=False)
	emails: List[Email] = relationship(Email, backref="user")


class Config(object):
	DB_URI = "sqlite:///mard.db"


engine = create_engine(Config.DB_URI, echo=True)
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
scoped_session_factory = scoped_session(session_factory)


def get_session() -> Session:
	return scoped_session_factory()
