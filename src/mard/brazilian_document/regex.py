import re


class Regex(object):

	def __init__(self, pattern: str):
		self._pattern = pattern

	def __str__(self):
		return self._pattern

	def optional(self):
		content = fr'(?:{self})?'
		return Regex(content)

	def zero_or_more(self):
		content = fr'(?:{self})*'
		return Regex(content)

	def one_or_more(self):
		content = fr'(?:{self})+'
		return Regex(content)

	def join(self, *contents: 'Regex'):
		content = self._pattern.join(map(str, contents))
		return Regex(content)

	def compile(self):
		return re.compile(self._pattern)


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


