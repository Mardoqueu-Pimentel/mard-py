import logging
from functools import wraps
from typing import Callable, TypeVar, Union

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')

Function = Callable[[T1], T2]
DecoratedFunction = Callable[[T1], Union[T2, T3]]
Decorator = Callable[[Function], DecoratedFunction]


def try_or_default(default_value: T3 = None) -> Decorator:
	def decorator(f: Function) -> DecoratedFunction:
		logger_name = f'{__name__}.{try_or_default.__name__}'
		logger = logging.getLogger(logger_name)

		@wraps(f)
		def wrapper(*args, **kwargs):
			value = default_value
			try:
				value = f(*args, **kwargs)
			except Exception as error:
				logger.exception(f'error while calling f: {error}')
			return value

		return wrapper

	return decorator
