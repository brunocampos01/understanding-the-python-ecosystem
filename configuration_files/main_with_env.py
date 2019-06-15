import os
from myapp import app

secret_key = os.environ.get('SECRET_KEY', None)

if not secret_key:
    raise ValueError('You must have "SECRET_KEY" variable')

app.config['SECRET_KEY'] = secret_key

# The configuration values are not managed as a separate file, so there is less risk of exposure of secret values