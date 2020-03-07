import itertools

from mard.brazilian_document.document_formatter import (
	DocumentFormatter
)
from mard.brazilian_document.document_parser import (
	DocumentParser
)
from mard.brazilian_document.regex import (
	NamedGroup, space, digit, literal
)

cnpj_pattern = NamedGroup('cnpj').content(
	space.zero_or_more().join(
		digit, digit,
		literal('.').optional(),
		digit, digit, digit,
		literal('.').optional(),
		digit, digit, digit,
		literal('/').optional(),
		digit, digit, digit, digit,
		literal('-').optional(),
		digit, digit
	)
).compile()

cnpj_formatter = DocumentFormatter(
	template='{}.{}.{}/{}-{}',
	sizes=(2, 3, 3, 4, 2)
)

cnpj_parser = DocumentParser(
	14,
	list(itertools.chain(range(2, 10), range(2, 7))),
	cnpj_formatter
)
