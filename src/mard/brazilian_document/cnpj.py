import itertools

from mard.brazilian_document.document_formatter import (
	Formatter
)
from mard.brazilian_document.document_validator import (
	DocumentValidator
)
from mard.regex import (
	NamedGroup, space, digit, literal
)


def make_cnpj_pattern():
	return NamedGroup('cnpj').of(
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


cnpj_pattern = make_cnpj_pattern()

cnpj_formatter = Formatter(
	template='{}.{}.{}/{}-{}',
	sizes=(2, 3, 3, 4, 2)
)

cnpj_validator = DocumentValidator(
	14,
	list(itertools.chain(range(2, 10), range(2, 7))),
	cnpj_formatter
)
