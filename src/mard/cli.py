import logging

import click
import mard
from mard.db import get_session, User

logger = logging.getLogger(__name__)


@click.command('mard-py')
@click.version_option(mard.__version__)
def main():
	session = get_session()

	user = session.query(User).first()

	logger.error(user)

	return 0


def run():
	exit(main())


if __name__ == '__main__':
	run()
