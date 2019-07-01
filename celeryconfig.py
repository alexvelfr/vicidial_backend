from celery import Celery

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = '3'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/' + REDIS_DB
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/' + REDIS_DB

app_celery = Celery('backend', broker=CELERY_BROKER_URL, timezone='Europe/Kiev')
