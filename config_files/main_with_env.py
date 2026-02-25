import os

secret_key = os.environ.get('SECRET_KEY', None)

if not secret_key:
    raise ValueError('You must set the "SECRET_KEY" environment variable')

# Example usage with a web framework:
# from myapp import app
# app.config['SECRET_KEY'] = secret_key
print(f"SECRET_KEY loaded successfully (length={len(secret_key)})")
