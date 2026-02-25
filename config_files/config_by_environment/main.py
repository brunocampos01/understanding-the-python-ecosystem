import sys

from bottle import app

from config_files.config_by_environment.config import (
    DevelopmentConfig,
    TestConfig,
    ProductionConfig,
)

if __name__ == '__main__':
    env = sys.argv[1] if len(sys.argv) > 1 else 'dev'

    if env == 'dev':
        app.config = DevelopmentConfig
    elif env == 'test':
        app.config = TestConfig
    elif env == 'prod':
        print('Select: production')
        app.config = ProductionConfig
    else:
        raise ValueError('Invalid environment name')
