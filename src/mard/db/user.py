from typing import List

from mard.db.email import Email
from mard.db.model import Model
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Model):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	name = Column(String(128), nullable=False)
	emails: List[Email] = relationship(Email, backref=__tablename__)
