from os import environ


class Config(object):
	DB_URI = environ.get('DB_URI', 'sqlite:///:memory:')
