import itertools

from mard.brazilian_document.regex import digit, space, Regex, NamedGroup

br_states_initials = {
	'AC': 'Acre',
	'AL': 'Alagoas',
	'AP': 'Amapá',
	'AM': 'Amazonas',
	'BA': 'Bahia',
	'CE': 'Ceará',
	'DF': 'Distrito Federal',
	'ES': 'Espírito Santo',
	'GO': 'Goiás',
	'MA': 'Maranhão',
	'MT': 'Mato Grosso',
	'MS': 'Mato Grosso do Sul',
	'MG': 'Minas Gerais',
	'PA': 'Pará',
	'PB': 'Paraíba',
	'PR': 'Paraná',
	'PE': 'Pernambuco',
	'PI': 'Piauí',
	'RJ': 'Rio de Janeiro',
	'RN': 'Rio Grande do Norte',
	'RS': 'Rio Grande do Sul',
	'RO': 'Rondônia',
	'RR': 'Roraima',
	'SC': 'Santa Catarina',
	'SP': 'São Paulo',
	'SE': 'Sergipe',
	'TO': 'Tocantins'
}

oab_digits = digit + (space.zero_or_more() + digit).repeat(3, 7)

br_states_initials_literals = map(Regex.literal, br_states_initials)
oab_states = Regex.one_of(*br_states_initials_literals)

oab_initials = space.zero_or_more().join(
	Regex.literal('O'), Regex.literal('A'), Regex.literal('B')
)

permutation_elements = (('I', oab_initials), ('D', oab_digits), ('S', oab_states))
oab_pattern_permutations = (
	NamedGroup(''.join(name for name, arg in args)).content(
		Regex.one_of(*(arg for name, arg in args))
	)
	for args in itertools.permutations(permutation_elements)
)
oab_pattern = Regex.one_of(*oab_pattern_permutations) \
	.compile(ignore_case=True)
