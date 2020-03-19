import re

from overload import overload


class Regex(object):

	def __init__(self, pattern: str):
		self._pattern = pattern

	def __str__(self):
		return self._pattern

	def __add__(self, other: 'Regex'):
		return Regex(self._pattern + other._pattern)

	def optional(self):
		content = fr'(?:{self})?'
		return Regex(content)

	def zero_or_more(self):
		content = fr'(?:{self})*'
		return Regex(content)

	def one_or_more(self):
		content = fr'(?:{self})+'
		return Regex(content)

	@overload
	def repeat(self, times: int):
		return Regex(fr'(?:{self}){times}')

	@repeat.add
	def repeat(self, lower_bound: int, upper_bound: int):
		return Regex(fr'(?:{self}){{{lower_bound}, {upper_bound}}}')

	def join(self, *contents: 'Regex'):
		content = self._pattern.join(map(str, contents))
		return Regex(content)

	def compile(self, ignore_case=False):
		flags = re.UNICODE
		if ignore_case:
			flags |= re.IGNORECASE

		return re.compile(self._pattern, flags=flags)

	@staticmethod
	def literal(content: str):
		return Regex(re.escape(content))

	@staticmethod
	def one_of(*contents: 'Regex'):
		content = '|'.join(x._pattern for x in contents)
		return Regex(fr'(?:{content})')


class NamedGroup(object):

	def __init__(self, name: str):
		self._name = re.escape(name)

	def content(self, *contents: Regex) -> Regex:
		content = ''.join(map(str, contents))
		return Regex(fr'(?P<{self._name}>{content})')


def literal(content: str):
	return Regex(re.escape(content))


space = Regex(r'\s')
digit = Regex(r'\d')

