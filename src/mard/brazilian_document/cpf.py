from mard.brazilian_document.document_formatter import (
	Formatter
)
from mard.brazilian_document.document_validator import (
	DocumentValidator
)
from mard.regex import (
	NamedGroup, space, digit, literal
)


def make_cpf_pattern():
	return NamedGroup('cpf').of(
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


cpf_pattern = make_cpf_pattern()

cpf_formatter = Formatter(
	template='{}.{}.{}-{}',
	sizes=(3, 3, 3, 2)
)

cpf_validator = DocumentValidator(
	11,
	list(range(2, 12)),
	cpf_formatter
)
