import itertools
from typing import Tuple


class DocumentFormatter(object):

	def __init__(self, template: str, sizes: Tuple[int, ...]):
		self._template = template
		self._document_size = sum(sizes)
		self._sizes = [
			(i - j, i)
			for i, j in zip(itertools.accumulate(sizes), sizes)
		]

	@property
	def document_size(self):
		return self._document_size

	def format(self, document: str):
		assert len(document) == self._document_size

		return self._template.format(
			*(document[i:j] for i, j in self._sizes)
		)
