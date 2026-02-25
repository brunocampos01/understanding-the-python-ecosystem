import os


class Config:
    APP_NAME = 'myapp'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
    ADMIN_NAME = 'administrator'

    AWS_DEFAULT_REGION = 'ap-northeast-2'

    STATIC_PREFIX_PATH = 'static'


class DevelopmentConfig(Config):
    DEBUG = True

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_S3_BUCKET_NAME = 'aws-s3-bucket-name-for-dev'


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_S3_BUCKET_NAME = 'aws-s3-bucket-name-for-test'


class ProductionConfig(Config):
    DEBUG = False

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME', '')
