import itertools
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Queue, Process, cpu_count
from typing import Optional, Iterable, Generator, TypeVar, Callable

T1 = TypeVar('T1')
T2 = TypeVar('T2')

logger = logging.getLogger(__file__)


class Sentinel:
	pass


def in_parallel(
		iterable: Iterable[T1],
		f: Callable[[T1], T2],
		queue_size: int,
		max_workers: Optional[int] = None
) -> Generator[T2, None, None]:
	"""

	Args:
		iterable: the input values of the f function
		f: a function
		queue_size: the maximum size of the queue
		max_workers: the maximum number of workers

	Returns:

	"""
	with ProcessPoolExecutor(max_workers=max_workers) as executor:
		iterator = iter(iterable)

		queue = [
			executor.submit(f, x)
			for x in itertools.islice(iterator, queue_size)
		]

		def next_future_completed_result():
			future = next(as_completed(queue))
			queue.remove(future)
			return future.result()

		for x in iterator:
			yield next_future_completed_result()
			queue.append(executor.submit(f, x))

		while queue:
			yield next_future_completed_result()


def worker_producer(f):
	def wrapper(input_queue: Queue, sentinel_count: int):
		try:
			for value in f():
				input_queue.put(value, block=True, timeout=30)
		except Exception as error:
			logger.exception(f'error in the producer function: {error}')

		for _ in range(sentinel_count):
			input_queue.put(Sentinel)

	return wrapper


def worker_mapper(f):
	def wrapper(input_queue: Queue, output_queue: Queue):
		while True:
			value = input_queue.get(block=True, timeout=30)
			if value is Sentinel:
				break

			try:
				result = f(value)
				output_queue.put(result)
			except Exception as error:
				logger.exception(f'error in mapper function: {error}')

		output_queue.put(Sentinel)

	return wrapper


class ProcessManager(object):

	def __init__(self, processes: Iterable[Process]):
		self._processes_generator = processes

	def __enter__(self):
		self._processes = list(self._processes_generator)
		for x in self._processes:
			x.start()

	def __exit__(self, exc_type, exc_val, exc_tb):
		for process in self._processes:
			process.kill()

		for process in self._processes:
			process.join()
			process.close()


def pipeline(
		producer_function: Callable[[], Iterable[T1]],
		mapper_function: Callable[[T1], T2],
		producer_count=1,
		mapper_count=cpu_count(),
		size_factor=100
) -> Generator[T2, None, None]:
	producer_function = worker_producer(producer_function)
	mapper_function = worker_mapper(mapper_function)

	maxsize = mapper_count * size_factor
	input_queue = Queue(maxsize=maxsize)
	output_queue = Queue(maxsize=maxsize)

	assert mapper_count % producer_count == 0
	producer_sentinel_count = mapper_count // producer_count

	ppg = (
		Process(
			target=producer_function,
			args=(input_queue, producer_sentinel_count)
		)
		for _ in range(producer_count)
	)
	mpg = (
		Process(
			target=mapper_function,
			args=(input_queue, output_queue)
		)
		for _ in range(mapper_count)
	)

	with ProcessManager(ppg), ProcessManager(mpg):
		sentinel_count = 0
		while sentinel_count < mapper_count:
			value = output_queue.get()
			if value is Sentinel:
				sentinel_count += 1
			else:
				yield value
