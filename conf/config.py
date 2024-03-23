from decouple import config


class ConfigDatabase(object):
    DB_HOST = config('DB_HOST', default='localhost')
    DB_PORT = config('DB_PORT', default='5555')
    DB_NAME = config('DB_NAME', default='ratetracker')
    DB_USER = config('DB_USER', default='postgres')
    DB_PASSWORD = config('DB_PASSWORD', default='8521946733')
    CONNECT_INFO_FIELD = config('CONNECT_INFO_FIELD', default='trade_info')


class Broker(object):
    BROKER_URL = config('BROKER_URL', default='amqp://guest:guest@localhost//')
