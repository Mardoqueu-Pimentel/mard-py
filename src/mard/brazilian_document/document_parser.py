import itertools
from collections import Counter
from typing import List

from mard.brazilian_document.document_formatter import (
	DocumentFormatter
)


class DocumentParser(object):

	def __init__(
			self,
			document_size: int,
			factors: List[int],
			formatter: DocumentFormatter
	):
		assert document_size == formatter.document_size == len(factors) + 1

		self.document_size = document_size
		self.factors = factors
		self.formatter = formatter

	def _generate_verification_digit(self, numbers):
		summation = sum(i * j for i, j in zip(numbers, self.factors))
		return summation * 10 % 11 % 10

	def parse(self, document: str):
		document = [int(x) for x in reversed(document) if x.isdigit()]
		size = len(document)
		if size > self.document_size:
			return None
		document.extend(itertools.repeat(0, self.document_size - size))

		if len(Counter(document)) == 1:
			return None

		for i in range(2, 0, -1):
			numbers = itertools.islice(document, i, None)
			verification_digit = self._generate_verification_digit(numbers)
			if verification_digit != document[i - 1]:
				return None

		return self.formatter.format(''.join(map(str, reversed(document))))
