import click


@click.command('mard-py')
def main():
	return 0


def run():
	exit(main())


if __name__ == '__main__':
	run()
