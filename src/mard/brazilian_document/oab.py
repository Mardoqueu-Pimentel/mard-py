import itertools

from mard.brazilian_document.info import brazilian_states
from mard.brazilian_document.regex import digit, space, NamedGroup, choice, literal, not_digit, Regex


def make_oab_components():
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


def make_oab_pattern():
	oab_literal, oab_state_literal, oab_digits = make_oab_components()

	oab_digits_prefix = not_digit + (space.zero_or_more() + not_digit).repeat(0, 9)
	oab_digits = oab_digits_prefix.optional() + oab_digits

	oab_space = choice(space, literal('.'), literal('/'))
	return NamedGroup('OAB').content(
		oab_space.zero_or_more().join(
			oab_literal, oab_state_literal, oab_digits
		)
	).compile(ignore_case=True)


def make_complex_oab_pattern():
	oab_literal, oab_state_literal, oab_digits = make_oab_components()

	elem = Regex('(?!OAB)') + not_digit
	oab_digits_prefix = elem + (space.zero_or_more() + elem).repeat(0, 9)
	oab_digits = oab_digits_prefix.optional() + oab_digits

	permutations = itertools.permutations((
		('L', oab_literal),
		('S', oab_state_literal),
		('D', oab_digits)
	))

	oab_space = choice(space, literal('.'), literal('/'))
	options = (
		NamedGroup(f'OAB_{nx}{ny}{nz}').content(
			oab_space.zero_or_more().join(
				x, y, z
			)
		)
		for (nx, x), (ny, y), (nz, z) in permutations
	)

	return choice(*options).compile(ignore_case=True)


oab_pattern = make_oab_pattern()
oab_pattern_complex = make_complex_oab_pattern()
