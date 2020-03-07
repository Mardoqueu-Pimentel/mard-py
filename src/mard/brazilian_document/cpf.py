from mard.brazilian_document.document_formatter import (
	DocumentFormatter
)
from mard.brazilian_document.document_parser import (
	DocumentParser
)
from mard.brazilian_document.regex import (
	NamedGroup, space, digit, literal
)

cpf_pattern = NamedGroup('cpf').content(
	space.zero_or_more().join(
		digit, digit, digit,
		literal('.').optional(),
		digit, digit, digit,
		literal('.').optional(),
		digit, digit, digit,
		literal('-').optional(),
		digit, digit
	)
).compile()

cpf_formatter = DocumentFormatter(
	template='{}.{}.{}-{}',
	sizes=(3, 3, 3, 2)
)

cpf_parser = DocumentParser(
	11,
	list(range(2, 12)),
	cpf_formatter
)
