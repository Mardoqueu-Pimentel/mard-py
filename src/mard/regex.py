import re
from collections import defaultdict
from typing import Dict, Callable, TypeVar, Any

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
		return Regex(fr'(?:{self}){{{lower_bound},{upper_bound}}}')

	def join(self, *contents: 'Regex'):
		content = self._pattern.join(map(str, contents))
		return Regex(content)

	def compile(self, ignore_case=False):
		flags = re.UNICODE
		if ignore_case:
			flags |= re.IGNORECASE

		return re.compile(self._pattern, flags=flags)


class NamedGroup(object):

	def __init__(self, name: str):
		self._name = re.escape(name)

	def of(self, *contents: Regex) -> Regex:
		content = ''.join(map(str, contents))
		return Regex(fr'(?P<{self._name}>{content})')


def literal(content: str):
	return Regex(re.escape(content))


def choice(*contents: Regex):
	content = '|'.join(map(str, contents))
	return Regex(fr'(?:{content})')


def combine(*contents: Regex):
	content = ''.join(map(str, contents))
	return Regex(content)


space = Regex(r'\s')
digit = Regex(r'\d')
not_digit = Regex(r'\D')

T1 = TypeVar('T1')


class RegexParser(object):

	def __init__(
			self,
			*components: Regex,
			formatters: Dict[str, Callable[[Any], str]],
			ignore_case=True
	):
		self._pattern = choice(*components).compile(ignore_case=ignore_case)
		self._formatters = formatters

	def parse(self, string: str):
		for match in self._pattern.finditer(string):
			formatter_arguments = defaultdict(dict)
			for group_name, group_match in match.groupdict().items():
				if group_match is not None:
					for formatter_name in self._formatters:
						if group_name.startswith(formatter_name):
							suffix = group_name[len(formatter_name):]
							formatter_arguments[formatter_name][suffix] = group_match

			for formatter_name, arguments in formatter_arguments.items():
				yield self._formatters[formatter_name](**arguments)
