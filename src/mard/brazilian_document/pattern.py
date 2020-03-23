import re
from typing import AnyStr

digit = r'\d'
spaces = r'\s*'
optional_dot = r'\.?'
optional_hyphen = r'-?'
optional_slash = r'\/?'


def optional(pattern: AnyStr):
	return re.compile(pattern=pattern)
