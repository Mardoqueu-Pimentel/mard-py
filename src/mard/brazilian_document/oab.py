from mard.brazilian_document.info import brazilian_states
from mard.regex import (
	digit, space, choice, literal, RegexParser, NamedGroup, not_digit, Regex)


def make_oab_pattern_components():
	oab_literal = space.zero_or_more().join(
		literal('O'), literal('A'), literal('B')
	)

	oab_state_literal = (
		space.zero_or_more().join(*(literal(x) for x in state))
		for state in brazilian_states
	)
	oab_state_literal = choice(*oab_state_literal)

	oab_digit_space = choice(space, literal('.'))
	oab_digits = digit + (oab_digit_space.zero_or_more() + digit).repeat(3, 7)

	return oab_literal, oab_state_literal, oab_digits


def make_oab_pattern(not_digits_before_digits=10):
	"""
	OAB pattern maker
	Args:
		not_digits_before_digits: to match patterns like 'OAB/XX Nº XX.XXX',
		'OAB/XX número XX.XXX', 'OAB/XX n XX.XXX'; The pattern supports n non
		numerical characters before the digits
	Returns: the OAB pattern
	"""
	oab_literal, oab_state_literal, oab_digits = make_oab_pattern_components()

	oab_digits_prefix = not_digit + (space.zero_or_more() + not_digit).repeat(
		0, not_digits_before_digits
	)
	oab_digits = oab_digits_prefix.optional() + oab_digits

	oab_space = choice(space, literal('.'), literal('/'))

	return oab_space.zero_or_more().join(
		oab_literal, choice(
			oab_space.zero_or_more().join(
				NamedGroup('oab123_state').of(oab_state_literal),
				NamedGroup('oab123_digits').of(oab_digits)
			),
			oab_space.zero_or_more().join(
				NamedGroup('oab132_digits').of(oab_digits),
				NamedGroup('oab132_state').of(oab_state_literal),
			)
		)
	).compile(ignore_case=True)


oab_pattern = make_oab_pattern()


def oab_formatter(state: str, digits: str) -> str:
	digits = ''.join(c for c in digits if c.isdigit())
	state = ''.join(c.upper() for c in state if c.isalpha())
	return f'{digits}/{state}'


oab_parser = RegexParser(
	Regex(oab_pattern.pattern),
	formatters={
		'oab123_': oab_formatter,
		'oab132_': oab_formatter
	},
	ignore_case=True
)
