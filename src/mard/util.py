import logging
from collections import defaultdict
from functools import wraps
from os import getpid
from typing import Callable, TypeVar, Union, Dict

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


class Singleton(object):

	def __init__(self, factory: Callable[[], T1]):
		self._instances: Dict[int, T1] = defaultdict(factory)

	def get_instance(self) -> T1:
		return self._instances[getpid()]
