import itertools
from typing import TypeVar, Iterable, Generator, Tuple

T1 = TypeVar('T1')


def as_chunks(
		iterable: Iterable[T1],
		chunk_size: int
) -> Generator[Tuple[T1, ...], None, None]:
	"""
	Generates a sequence of tuples of size equal to chunk_size from elements of
	iterable
	Args:
		iterable: an iterable
		chunk_size: the maximum size of the resulting chunks

	Returns:

	Raises:
		AssertionError: if chunk_size is lower than 2

	"""
	assert chunk_size >= 2

	rest_size = chunk_size - 1

	iterator = iter(iterable)
	while True:
		try:
			chunk_first = next(iterator)
			chunk_rest = itertools.islice(iterator, rest_size)
			yield tuple(itertools.chain((chunk_first,), chunk_rest))
		except StopIteration:
			return
