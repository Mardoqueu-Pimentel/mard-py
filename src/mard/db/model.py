from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Model(Base):
	__abstract__ = True

	@classmethod
	def from_dict(cls, obj: dict):
		return cls(**obj)

	def as_dict(self):
		return {
			c.key: getattr(self, c.key)
			for c in inspect(self).mapper.column_attrs
		}

	def __repr__(self):
		return repr({
			'__class__': type(self).__name__,
			**self.as_dict()
		})

	def __str__(self):
		return str(self.as_dict())
