import configparser

config = configparser.ConfigParser()
config.read('config.ini')

secret_key = config['DEFAULT']['SECRET_KEY']    # 'secret-key-of-myapp'
ci_hook_url = config['CI']['HOOK_URL']  # 'web-hooking-url-from-ci-service'