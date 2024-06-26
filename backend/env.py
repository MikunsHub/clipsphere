from os import environ

LOCAL = environ.get('LOCAL')
LOCALSTACK_ENDPOINT_URL = environ.get('LOCALSTACK_ENDPOINT_URL')

PG_USER = environ['PG_USER']
PG_PASSWORD = environ['PG_PASSWORD']
PG_HOST = environ['PG_HOST']
PG_NAME = environ['PG_NAME']
PG_PORT = environ['PG_PORT']

SECRET_KEY = environ['SECRET_KEY']  # use makefile to fill this at runtime
ALGORITHM = environ['ALGORITHM']  # use makefile to fill this at runtime

AWS_S3_RAW_VIDEOS_BUCKET_NAME = environ['AWS_S3_RAW_VIDEOS_BUCKET_NAME']

TOKEN_URL = environ['TOKEN_URL']
