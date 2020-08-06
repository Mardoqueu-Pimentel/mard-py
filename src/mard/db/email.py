from mard.db.model import Model
from sqlalchemy import Column, Integer, String, ForeignKey


class Email(Model):
	__tablename__ = "email"

	id = Column(Integer, primary_key=True)
	value = Column(String(128), nullable=False)
	user_id = Column(Integer, ForeignKey("user.id"))