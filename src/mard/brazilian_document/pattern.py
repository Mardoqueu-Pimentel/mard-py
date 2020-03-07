from typing import AnyStr
import re

digit = r'\d'
spaces = r'\s*'
optional_dot = r'\.?'
optional_hyphen = r'-?'
optional_slash = r'\/?'


def optional(pattern: AnyStr):
	return re.compile(pattern=pattern)
