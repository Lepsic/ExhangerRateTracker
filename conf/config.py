from decouple import config


class ConfigDatabase(object):
    DB_HOST = config('DB_HOST', default='localhost')
    DB_PORT = config('')
    DB_NAME = config('DB_NAME', default='ratetracker')
    DB_USER = config('DB_USER', default='postgres')
    DB_PASSWORD = config('DB_PASSWORD', default='')
