from mard.util import try_or_default


def test_try_or_default():
	def f(x):
		if x > 10:
			raise Exception()
		return x

	class Sentinel:
		pass

	for default in (Sentinel, None):
		decorator = try_or_default(default_value=default)
		df = decorator(f)

		assert df(5) == 5
		assert df(42) is default
