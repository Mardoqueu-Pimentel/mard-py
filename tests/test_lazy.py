import pytest
from mard.lazy import as_chunks


def test_as_chunks():
	assert list(as_chunks(range(0), 2)) == []
	assert list(as_chunks(range(5), 2)) == [(0, 1), (2, 3), (4,)]
	assert list(as_chunks(range(5), 3)) == [(0, 1, 2), (3, 4)]
	assert list(as_chunks(range(5), 4)) == [(0, 1, 2, 3), (4,)]
	assert list(as_chunks(range(5), 5)) == [(0, 1, 2, 3, 4)]
	assert list(as_chunks(range(5), 6)) == [(0, 1, 2, 3, 4)]

	for i in range(-1, 2):
		with pytest.raises(AssertionError):
			list(as_chunks(range(10), i))
